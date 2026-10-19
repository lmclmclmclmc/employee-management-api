import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi.testclient import TestClient

import database
from main_db import app
from security import create_access_token


class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = TemporaryDirectory()

        database.DATABASE_NAME = str(Path(self.temporary_directory.name) / "test.db")
        database.initialize_database()
        self.client = TestClient(app)
        self.client.post(
            "/register",
            json={
                "username": "admin",
                "password": "development-password",
            },
        )

    def tearDown(self):
        self.temporary_directory.cleanup()

    def login(self):
        return self.client.post(
            "/login",
            data={
                "username": "admin",
                "password": "development-password",
            },
        )

    def test_me_rejects_token_for_unknown_user(self):
        token = create_access_token("unknown-user")

        response = self.client.get(
            "/me",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        self.assertEqual(response.status_code, 401)

    def test_register_success(self):
        response = self.client.post(
            "/register",
            json={
                "username": "alice",
                "password": "password123",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["username"], "alice")
        self.assertIn("id", response.json())
        self.assertNotIn("password", response.json())
        self.assertNotIn("password_hash", response.json())

    def test_register_duplicate_username(self):
        response = self.client.post(
            "/register",
            json={
                "username": "admin",
                "password": "another-password",
            },
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response.json()["detail"],
            "Username already exists",
        )

    def test_register_rejects_short_password(self):
        response = self.client.post(
            "/register",
            json={
                "username": "alice",
                "password": "short",
            },
        )

        self.assertEqual(response.status_code, 422)

    def test_login_unknown_user(self):
        response = self.client.post(
            "/login",
            data={
                "username": "nobody",
                "password": "password123",
            },
        )

        self.assertEqual(response.status_code, 401)

    def test_login_success(self):
        response = self.login()

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertEqual(
            response.json()["token_type"],
            "bearer",
        )

    def test_login_wrong_password(self):
        response = self.client.post(
            "/login",
            data={
                "username": "admin",
                "password": "wrong-password",
            },
        )

        self.assertEqual(response.status_code, 401)

    def test_me_requires_token(self):
        response = self.client.get("/me")
        self.assertEqual(response.status_code, 401)

    def test_me_with_valid_token(self):
        token = self.login().json()["access_token"]

        response = self.client.get(
            "/me",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"username": "admin"},
        )

    def test_me_rejects_invalid_token(self):
        response = self.client.get(
            "/me",
            headers={
                "Authorization": "Bearer invalid-token",
            },
        )

        self.assertEqual(response.status_code, 401)

    def test_all_write_routes_require_token(self):
        responses = [
            self.client.post(
                "/employees",
                json={"name": "wang", "salary": 8000},
            ),
            self.client.put(
                "/employees/1",
                json={"name": "wang", "salary": 9000},
            ),
            self.client.patch(
                "/employees/1",
                json={"salary": 9000},
            ),
            self.client.delete("/employees/1"),
        ]

        for response in responses:
            with self.subTest(status=response.status_code):
                self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi.testclient import TestClient

import database 
from main_db import app

class TestDatabaseEmployeeAPI(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = TemporaryDirectory()

        database.DATABASE_NAME = str(
            Path(self.temporary_directory.name) / "test.db"
        )

        database.initialize_database()

        self.client = TestClient(app)
        self.client.post(
    "/register",
    json={
        "username": "admin",
        "password": "development-password",
    },
)
        login_response = self.client.post(
            "/login",
            data={
                "username": "admin",
                "password": "development-password",
            },
        )

        token = login_response.json()["access_token"]

        self.client.headers.update({
            "Authorization": f"Bearer {token}"
        })

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_write_requires_token(self):
        unauthorized_client = TestClient(app)

        response = unauthorized_client.post(
            "/employees",
            json={"name": "wang", "salary": 8000}
        )

        self.assertEqual(response.status_code, 401)

    def test_create_and_list_employees(self):
        create_response = self.client.post(
            "/employees",
            json={"name": "wang", "salary": 8000}
        )

        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(create_response.json()["id"], 1)

        list_response = self.client.get("/employees")

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.json()), 1)
        self.assertEqual(list_response.json()[0]["name"], "wang")

    def test_update_and_delete_employee(self):
        self.client.post(
            "/employees",
            json={"name": "li", "salary": 8000}
        )

        update_response = self.client.put(
            "/employees/1",
            json={"name": "li", "salary": 10000}

        )

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()["salary"], 10000)

        delete_response = self.client.delete("/employees/1")
        self.assertEqual(delete_response.status_code, 200)

        get_response = self.client.get("/employees/1")
        self.assertEqual(get_response.status_code, 404)


if __name__ == "__main__":
    unittest.main()

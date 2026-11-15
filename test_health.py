import unittest
from unittest.mock import Mock

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from db_session import get_db
from main_db import app


class TestHealthCheck(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
        )

        def override_get_db():
            with Session(self.engine) as session:
                yield session

        app.dependency_overrides[get_db] = override_get_db
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()
        app.dependency_overrides.clear()
        self.engine.dispose()

    def test_health_check(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "status": "ok",
                "database": "connected",
            },
        )

    def test_health_check_database_unavailable(self):
        unavailable_session = Mock(spec=Session)
        unavailable_session.execute.side_effect = OperationalError(
            "SELECT 1",
            {},
            Exception("database offline"),
        )

        def override_unavailable_db():
            yield unavailable_session

        app.dependency_overrides[get_db] = override_unavailable_db

        response = self.client.get("/health")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json(),
            {"detail": "Database unavailable"},
        )


if __name__ == "__main__":
    unittest.main()

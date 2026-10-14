import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi.testclient import TestClient

import database
from main_db import app

class TestHealthCheck(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = TemporaryDirectory()

        database.DATABASE_NAME = str(
            Path(self.temporary_directory.name) / "test.db"
        )

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_health_check(self):
        with TestClient(app) as client:
            response = client.get("/health")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json(),
                {
                    "status": "ok",
                    "database": "connected",
                },
            )

if __name__ == "__main__":
    unittest.main()
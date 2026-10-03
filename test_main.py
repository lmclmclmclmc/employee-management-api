import unittest

from fastapi.testclient import TestClient

from main import app, employees

class TestEmployeeAPI(unittest.TestCase):
    def setUp(self):
        employees.clear()
        self.client = TestClient(app)

    def test_create_employee(self):
        response = self.client.post(
            "/employees",
            json={"name": "wang", "salary": 8000}
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["id"], 1)
        self.assertEqual(response.json()["name"], "wang")

    def test_invalid_employee(self):
        response = self.client.post(
            "/employees",
            json={"name": "", "salary": -100}
        )

        self.assertEqual(response.status_code, 422)

    def test_get_missing_employee(self):
        response = self.client.get("/employees/999")

        self.assertEqual(response.status_code, 404)

    def test_update_and_delete_employee(self):
        self.client.post(
            "/employees",
            json={"name": "li", "salary": 8000}
        )

        update_response = self.client.put(
            "/employees/1",
            json={"name": "li", "salary": 9000}
        )

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()["salary"], 9000)

        delete_response = self.client.delete("/employees/1")
        self.assertEqual(delete_response.status_code, 200)

        get_response = self.client.get("/employees/1")
        self.assertEqual(get_response.status_code, 404)


if __name__ == "__main__":
    unittest.main()

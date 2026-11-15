import unittest

from models import Base


class TestModels(unittest.TestCase):
    def test_expected_table_are_registered(self):
        self.assertEqual(
            set(Base.metadata.tables),
            {"employees", "users"},
        )

    def test_employee_has_department_column(self):

        employee_table = Base.metadata.tables["employees"]

        self.assertIn(
            "department",
            employee_table.columns,
        )

        self.assertFalse(
            employee_table.columns["department"].nullable,
        )


if __name__ == "__main__":
    unittest.main()

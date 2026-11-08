import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from employee_repository import (
    create_employee,
    delete_employee,
    get_employee_by_id,
    list_employees,
    update_employee,
)
from models import Base, Employee


class TestEmployeeRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        self.engine.dispose()

    def test_get_existing_employee(self):
        with Session(self.engine) as session:
            employee = Employee(
                name="Alice",
                department="Finance",
                salary=12000,
            )

            session.add(employee)
            session.commit()

            employee_id = employee.id
            result = get_employee_by_id(session, employee_id)

            self.assertIsNotNone(result)
            self.assertEqual(result.name, "Alice")
            self.assertEqual(result.department, "Finance")
            self.assertEqual(result.salary, 12000)

    def test_get_missing_employee(self):
        with Session(self.engine) as session:
            result = get_employee_by_id(session, 999)

            self.assertIsNone(result)

    def test_list_employees_with_pagination(self):
        with Session(self.engine) as session:
            session.add_all(
                [
                    Employee(
                        name="Alice",
                        department="Finance",
                        salary=12000,
                    ),
                    Employee(
                        name="Bob",
                        department="Engineering",
                        salary=15000,
                    ),
                    Employee(
                        name="Charlie",
                        department="Sales",
                        salary=10000,
                    ),
                ]
            )
            session.commit()

            result = list_employees(
                session,
                limit=1,
                offset=1,
            )

            self.assertEqual(len(result), 1)
            self.assertEqual(result[0].name, "Bob")

    def test_search_employees_by_partial_name(self):
        with Session(self.engine) as session:
            session.add_all(
                [
                    Employee(
                        name="Alice",
                        department="Finance",
                        salary=12000,
                    ),
                    Employee(
                        name="Bob",
                        department="Engineering",
                        salary=15000,
                    ),
                ]
            )
            session.commit()

            result = list_employees(
                session,
                name="ALI",
            )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Alice")

    def test_create_employee(self):
        with Session(self.engine) as session:
            employee = create_employee(
                session,
                name="David",
                department="Engineering",
                salary=18000,
            )

            self.assertIsNotNone(employee.id)
            self.assertEqual(employee.name, "David")
            employee_id = employee.id

        with Session(self.engine) as session:
            saved_employee = get_employee_by_id(
                session,
                employee_id,
            )

            self.assertIsNotNone(saved_employee)
            self.assertEqual(
                saved_employee.department,
                "Engineering",
            )

    def test_update_employee(self):
        with Session(self.engine) as session:
            employee = create_employee(
                session,
                name="Eva",
                department="Sales",
                salary=10000,
            )

            result = update_employee(
                session,
                employee.id,
                name="Eva Chen",
                department="Finance",
                salary=13000,
            )

            self.assertIsNotNone(result)
            self.assertEqual(result.name, "Eva Chen")
            self.assertEqual(result.department, "Finance")
            self.assertEqual(result.salary, 13000)

            missing_result = update_employee(
                session,
                999,
                name="Missing",
                department="General",
                salary=1000,
            )

            self.assertIsNone(missing_result)

    def test_delete_employee(self):
        with Session(self.engine) as session:
            employee = create_employee(
                session,
                name="Frank",
                department="Support",
                salary=9000,
            )
            employee_id = employee.id

            deleted_employee = delete_employee(
                session,
                employee_id,
            )

            self.assertIsNotNone(deleted_employee)
            self.assertEqual(deleted_employee.name, "Frank")
            self.assertIsNone(get_employee_by_id(session, employee_id))
            self.assertIsNone(delete_employee(session, 999))


if __name__ == "__main__":
    unittest.main()

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Base
from user_repository import (
    create_user,
    get_user_by_username,
)


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        self.engine.dispose()

    def test_create_and_get_user(self):
        with Session(self.engine) as session:
            created_user = create_user(
                session,
                username="alice",
                password_hash="hashed-password",
            )

            self.assertIsNotNone(created_user)
            self.assertIsNotNone(created_user.id)

            found_user = get_user_by_username(
                session,
                "alice",
            )

            self.assertIsNotNone(found_user)
            self.assertEqual(found_user.username, "alice")
            self.assertEqual(
                found_user.password_hash,
                "hashed-password",
            )

    def test_get_missing_user(self):
        with Session(self.engine) as session:
            result = get_user_by_username(
                session,
                "unknown",
            )

            self.assertIsNone(result)

    def test_duplicate_username_rolls_back_session(self):
        with Session(self.engine) as session:
            first_user = create_user(
                session,
                username="alice",
                password_hash="first-hash",
            )
            duplicate_user = create_user(
                session,
                username="alice",
                password_hash="second-hash",
            )

            self.assertIsNotNone(first_user)
            self.assertIsNone(duplicate_user)

            existing_user = get_user_by_username(
                session,
                "alice",
            )

            self.assertIsNotNone(existing_user)
            self.assertEqual(
                existing_user.password_hash,
                "first-hash",
            )


if __name__ == "__main__":
    unittest.main()

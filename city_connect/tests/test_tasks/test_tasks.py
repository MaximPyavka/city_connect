import unittest

from city_connect.app import db
from city_connect.models.task import Task
from city_connect.models.user import User
from city_connect.tests.tests_config import BaseTestCase


class TestTaskModel(BaseTestCase):

    def test_relationship(self):
        t = self._create_task()
        u = User.query.get(t.user_id)
        self.assertNotEqual(t, None)
        self.assertEqual(t.user_id, 1)
        self.assertNotEqual(u, None)
        self.assertEqual(u.id, 1)

    def _create_task(self):
        u = User(phone_number='09311114444')
        db.session.add(u)
        db.session.commit()

        t = Task(
            title="test_title",
            user_id=u.id,
            description="These is test escription"
        )
        db.session.add(t)
        db.session.commit()
        return t


if __name__ == '__main__':
    unittest.main()

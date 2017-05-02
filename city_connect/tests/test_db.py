import sys
import os

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             '../..'))

from flask_testing import TestCase

from city_connect.app import db, app
from city_connect.tests.tests_config import TestConfig


class TestDataBase(TestConfig):
    def test_save(self):
        pass

if __name__ == '__main__':
    import unittest
    unittest.main()

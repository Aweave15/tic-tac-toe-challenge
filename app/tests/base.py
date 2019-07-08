import unittest
from core.app_config import create_app



class BaseTest(unittest.TestCase):

    def setUp(self):
        app = create_app(testing=True)
        self.client = app.test_client()

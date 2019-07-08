from tests.base import BaseTest
from core.app_config import create_app

class HealthCheckTestCase(BaseTest):

    def test_health_check(self):
        response = self.client.get('/healthcheck/')
        self.assertEqual(response.status_code, 200)
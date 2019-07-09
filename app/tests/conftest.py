import pytest
from core.app_config import create_app


@pytest.fixture
def client():
    app = create_app(testing=True)
    return app.test_client()

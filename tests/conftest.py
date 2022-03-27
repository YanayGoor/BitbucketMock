import pytest
from starlette.testclient import TestClient

from bitbucketmock import BitbucketMock


@pytest.fixture
def client() -> TestClient:
    return BitbucketMock().get_test_client()

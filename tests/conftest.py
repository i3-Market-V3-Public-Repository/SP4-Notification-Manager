import os

import pytest
from loguru import logger

from src.main import application


@pytest.fixture
def client():
    # Prepare before your test
    application.config["TESTING"] = True
    with application.test_client() as client:
        # Give control to your test
        yield client


@pytest.fixture(autouse=True, scope='session')
def disable_logger():
    logger.disable("")
    yield


@pytest.fixture(autouse=True, scope='function')
def clear_database():
    yield


@pytest.fixture(autouse=True, scope='session')
def remove_dummy_storage():
    yield
    os.remove(os.path.join(os.path.dirname(__file__), 'files', 'dummy_storage_tests.json'))

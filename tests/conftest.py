import os
from unittest.mock import patch

import pytest
from loguru import logger

from src.alert_subscription.storage.dummy_subscriptions_storage import DummySubscriptionsStorage
from src.main import application, subscriptions_storage_filepath


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


@pytest.fixture(autouse=True, scope='function')
def remove_json_storage():
    yield
    if os.path.exists(subscriptions_storage_filepath):
        os.remove(subscriptions_storage_filepath)

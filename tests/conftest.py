import json
import os

import pytest
from loguru import logger

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
def remove_json_storage():
    if not os.path.exists(subscriptions_storage_filepath):
        with open(subscriptions_storage_filepath, 'w') as file:
            json.dump({}, file, indent=2)
    yield None
    if os.path.exists(subscriptions_storage_filepath):
        os.remove(subscriptions_storage_filepath)

#!/bin/bash

# pytest -vv
# pytest -vv --disable-warnings tests/functional/test_notifications.py
# pytest -vv --disable-warnings tests/functional/test_queues.py
# pytest -vv --disable-warnings tests/functional/test_subscriptions.py
# pytest -vv --disable-warnings tests/functional/test_version.py
# pytest -vv --disable-warnings
pytest --disable-warnings
echo Pytest exited $?
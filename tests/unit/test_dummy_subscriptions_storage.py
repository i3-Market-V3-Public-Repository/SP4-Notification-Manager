import os

from src.alert_subscription.storage.dummy_subscriptions_storage import DummySubscriptionsStorage

tests_path = os.path.dirname(os.path.dirname(__file__))
dummy_storage_test_path = os.path.join(tests_path, 'files', 'dummy_storage_tests.json')
dummy_storage = DummySubscriptionsStorage(dummy_storage_test_path)

subscriptions = [
    {
        "id": "YYY-YYYYYY",
        "category": "cat1",
        "query": "query-string",
        "enabled": True
    },
    {
        "id": "ZZZ-ZZZZZZ",
        "category": "cat2",
        "query": "query-string",
        "enabled": False
    }
]


def test_create_first_subscription_for_an_user():
    stored_user = dummy_storage.create_user_subscription(user_id='1', subscription=subscriptions[0])

    assert stored_user == subscriptions[0]


def test_create_duplicate_subscription_for_an_user():
    stored_user = dummy_storage.create_user_subscription(user_id='1', subscription=subscriptions[0])

    assert stored_user is None


def test_second_subscription_for_an_user():
    stored_user = dummy_storage.create_user_subscription(user_id='1', subscription=subscriptions[1])

    assert stored_user == subscriptions[1]


def test_retrieve_all_subscriptions_for_an_user():
    stored_user = dummy_storage.retrieve_all_user_subscriptions(user_id='1')

    assert len(stored_user) == 2
    assert stored_user == subscriptions


def test_retrieve_subscription_by_id_for_an_user():
    stored_user = dummy_storage.retrieve_user_subscription(user_id='1', subscription_id=subscriptions[1].get('id'))

    assert stored_user == subscriptions[1]


def test_update_subscription_by_id_for_an_user():
    subscriptions[1]["enabled"] = True
    stored_user = dummy_storage.update_user_subscription(user_id='1', subscription_id=subscriptions[1].get('id'),
                                                         subscription=subscriptions[1])

    assert stored_user == subscriptions[1]


def test_update_missing_subscription_by_id_for_an_user():
    stored_user = dummy_storage.update_user_subscription(user_id='1', subscription_id='non-existing',
                                                         subscription=subscriptions[1])

    assert stored_user is None


def test_remove_subscription_by_id_for_an_user():
    stored_user = dummy_storage.delete_user_subscription(user_id='1', subscription_id=subscriptions[1].get('id'))

    assert stored_user == subscriptions[1]


def test_remove_missing_subscription_by_id_for_an_user():
    stored_user = dummy_storage.delete_user_subscription(user_id='1', subscription_id='non-existing')

    assert stored_user is None



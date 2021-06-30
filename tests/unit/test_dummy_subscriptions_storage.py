import os
import uuid

from src.alert_subscription.storage.dummy_subscriptions_storage import DummySubscriptionsStorage

tests_path = os.path.dirname(os.path.dirname(__file__))
dummy_storage_test_path = os.path.join(tests_path, 'files', 'dummy_storage_tests.json')
dummy_storage = DummySubscriptionsStorage(dummy_storage_test_path)

subscriptions = [
    {
        "id": uuid.uuid4().__str__(),
        "category": "category1",
    },
    {
        "id": uuid.uuid4().__str__(),
        "category": "category2",
    }
]


def test_search_missing_subscription_for_an_user():
    stored_subscription = dummy_storage.search_user_subscription(user_id='1', data=subscriptions[0])

    assert stored_subscription is None


def test_create_first_subscription_for_an_user():
    stored_subscription = dummy_storage.insert_user_subscription(user_id='1', subscription=subscriptions[0])

    assert stored_subscription == subscriptions[0]


def test_search_subscription_for_an_user():
    stored_subscription = dummy_storage.search_user_subscription(user_id='1', data=subscriptions[0])

    assert stored_subscription == subscriptions[0]


def test_second_subscription_for_an_user():
    stored_subscription = dummy_storage.insert_user_subscription(user_id='1', subscription=subscriptions[1])

    assert stored_subscription == subscriptions[1]


def test_retrieve_all_subscriptions_for_an_user():
    stored_subscription = dummy_storage.retrieve_all_user_subscriptions(user_id='1')

    assert len(stored_subscription) == 2
    assert stored_subscription == subscriptions


def test_retrieve_subscription_by_id_for_an_user():
    stored_subscription = dummy_storage.retrieve_user_subscription(user_id='1',
                                                                   subscription_id=subscriptions[1].get('id'))

    assert stored_subscription == subscriptions[1]


def test_update_subscription_by_id_for_an_user():
    subscriptions[1]["active"] = True

    stored_subscription = dummy_storage.update_user_subscription(user_id='1',
                                                                 subscription_id=subscriptions[1].get('id'),
                                                                 data=subscriptions[1])

    assert stored_subscription == subscriptions[1]


def test_update_missing_subscription_by_id_for_an_user():
    stored_subscription = dummy_storage.update_user_subscription(user_id='1', subscription_id='non-existing',
                                                                 data=subscriptions[1])

    assert stored_subscription is None


def test_remove_subscription_by_id_for_an_user():
    stored_subscription = dummy_storage.delete_user_subscription(user_id='1',
                                                                 subscription_id=subscriptions[1].get('id'))

    assert stored_subscription == subscriptions[1]


def test_remove_missing_subscription_by_id_for_an_user():
    stored_subscription = dummy_storage.delete_user_subscription(user_id='1', subscription_id='non-existing')

    assert stored_subscription is None

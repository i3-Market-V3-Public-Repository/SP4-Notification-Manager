import uuid

from src.main import subscriptions_storage as storage

users = {
    '1': [
        {
            "id": uuid.uuid4().__str__(),
            "category": "category1",
            "active": True
        },
        {
            "id": uuid.uuid4().__str__(),
            "category": "category2",
            "active": False
        }
    ]
}


def test_retrieve_all_missing_subscriptions_return_empty_dict():
    assert storage.retrieve_all() == []


def test_search_missing_subscription_for_an_user():
    user_id = '1'
    subscription_data = users.get('1')[0]
    assert storage.search_user_subscription(user_id, subscription_data) is None


def test_create_first_subscription_for_an_user():
    user_id = '1'
    subscription_data = users.get('1')[0]
    assert storage.insert_user_subscription(user_id, subscription_data) == subscription_data


def test_search_non_existing_subscription_for_an_user():
    user_id = '1'
    subscription_data = users.get('1')[1]
    assert storage.search_user_subscription(user_id, subscription_data) is None


def test_search_subscription_for_an_non_existing_user():
    user_id = '2'
    subscription_data = users.get('1')[1]
    assert storage.retrieve_user_subscription(user_id, uuid.uuid4().__str__()) is None


def test_retrieve_all_subscriptions():
    user_id = '1'
    copy = storage.retrieve_all()
    del copy[0]['subscriptions'][0]['id']
    # assert storage.retrieve_all() == [{"user_id": '1', "subscriptions": [subscription_data]}]
    assert copy == [{"user_id": '1', "subscriptions": [users.get('1')[0]]}]


def test_search_subscription_for_an_user():
    user_id = '1'
    subscription_data = users.get('1')[0]
    assert storage.search_user_subscription(user_id, subscription_data) == subscription_data


def test_second_subscription_for_an_user():
    user_id = '1'
    subscription_data_2 = users.get('1')[1]
    storage.insert_user_subscription(user_id, subscription_data_2)
    assert storage.search_user_subscription(user_id, subscription_data_2) == subscription_data_2


def test_retrieve_all_subscriptions_for_an_user():
    user_id = '1'
    subscription_data_1 = users.get('1')[0]
    subscription_data_2 = users.get('1')[1]
    stored_subscription = storage.retrieve_all_user_subscriptions(user_id)
    assert len(stored_subscription) == 2
    assert stored_subscription == [subscription_data_1, subscription_data_2]


def test_retrieve_subscription_by_id_for_an_user():
    user_id = '1'
    subscription_data = users.get('1')[0]
    storage.insert_user_subscription(user_id, subscription_data)
    assert storage.retrieve_user_subscription(user_id, subscription_data.get('id')) == subscription_data


def test_update_missing_subscription_by_id_for_an_user():
    user_id = '1'
    subscription_data = users.get('1')[0]
    assert storage.update_user_subscription(user_id, 'non-existing', subscription_data) is None


def test_update_subscription_missing_user_id():
    user_id = '2'
    subscription_data = users.get('1')[0]
    assert storage.update_user_subscription(user_id, 'non-existing', subscription_data) is None


def test_update_subscription_by_id_for_an_user():
    user_id = '1'
    subscription_data = users.get('1')[0]
    storage.insert_user_subscription(user_id, subscription_data)
    subscription_data["active"] = True
    assert storage.update_user_subscription(
        user_id, subscription_data.get('id'), subscription_data) == subscription_data


def test_remove_missing_subscription_by_id_for_an_user():
    assert storage.delete_user_subscription('1', 'non-existing') is None


def test_remove_subscription_by_non_existing_id_for_an_user():
    assert storage.delete_user_subscription('2', 'non-existing') is None


def test_remove_subscription_by_id_for_an_user():
    user_id = '1'
    subscription_data = users.get('1')[0]
    storage.insert_user_subscription(user_id, subscription_data)
    stored_subscription = storage.delete_user_subscription(user_id, subscription_id=subscription_data.get('id'))
    assert stored_subscription == subscription_data


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

## TODO Testeado con postman, pendiente arreglar los tests. En teoria estos siguen funcionando


def test_retrieve_all_missing_subscriptions():
    stored_subscription = storage.retrieve_all()

    assert stored_subscription == {}


def test_search_missing_subscription_for_an_user():
    stored_subscription = storage.search_user_subscription(user_id='1', data=users.get('1')[0])

    assert stored_subscription is None


def test_create_first_subscription_for_an_user():
    stored_subscription = storage.insert_user_subscription(user_id='1', subscription=users.get('1')[0])

    assert stored_subscription == users.get('1')[0]


def test_retrieve_all_subscriptions():
    stored_subscription = storage.retrieve_all()

    assert stored_subscription == {'1': [users.get('1')[0]]}


def test_search_subscription_for_an_user():
    stored_subscription = storage.search_user_subscription(user_id='1', data=users.get('1')[0])

    assert stored_subscription == users.get('1')[0]


def test_second_subscription_for_an_user():
    stored_subscription = storage.insert_user_subscription(user_id='1', subscription=users.get('1')[1])

    assert stored_subscription == users.get('1')[1]


def test_retrieve_all_subscriptions_for_an_user():
    stored_subscription = storage.retrieve_all_user_subscriptions(user_id='1')

    assert len(stored_subscription) == 2
    assert stored_subscription == users.get('1')


def test_retrieve_subscription_by_id_for_an_user():
    stored_subscription = storage.retrieve_user_subscription(user_id='1', subscription_id=users.get('1')[1].get('id'))

    assert stored_subscription == users.get('1')[1]


def test_update_subscription_by_id_for_an_user():
    users.get('1')[1]["active"] = True

    stored_subscription = storage.update_user_subscription(user_id='1', subscription_id=users.get('1')[1].get('id'),
                                                           data=users.get('1')[1])

    assert stored_subscription == users.get('1')[1]


def test_update_missing_subscription_by_id_for_an_user():
    stored_subscription = storage.update_user_subscription(user_id='1', subscription_id='non-existing',
                                                           data=users.get('1')[1])

    assert stored_subscription is None


def test_remove_subscription_by_id_for_an_user():
    stored_subscription = storage.delete_user_subscription(user_id='1', subscription_id=users.get('1')[1].get('id'))

    assert stored_subscription == users.get('1')[1]


def test_remove_missing_subscription_by_id_for_an_user():
    stored_subscription = storage.delete_user_subscription(user_id='1', subscription_id='non-existing')

    assert stored_subscription is None

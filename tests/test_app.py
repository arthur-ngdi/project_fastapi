from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root_should_return_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World!'}


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_all_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_all_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'password': 'test12344',
            'username': 'testNEWusername',
            'email': 'testnew.email@test.com',
            'id': 1,
        },
    )

    # Validar o status code
    assert response.status_code == HTTPStatus.OK

    # Validar UserPublic
    assert response.json() == {
        'username': 'testNEWusername',
        'email': 'testnew.email@test.com',
        'id': 1,
    }


""" def test_fail_to_update_user(client, user):
    response = client.put(
        '/users/6',
        json={
            'password': 'test12344',
            'username': 'testNEWusername',
            'email': 'testnew.email@test.com',
            'id': 1,
        },
    )

    # Validar o status code
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'} """


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_user_already_exist(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    # Verifica se o status é 400 e se a mensagem é a correta
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_with_existing_email(client, user):
    # Tenta criar um usuário com o mesmo email que o `existing_user`
    response = client.post(
        '/users/',
        json={
            'username': 'alice2',
            'email': user.email,
            'password': 'secret',
        },
    )
    # Verifica se o status é 400 e se a mensagem é a correta
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_get_user_should_return_not_found(client):
    response = client.get('/users/666')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_user(client, user):
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }

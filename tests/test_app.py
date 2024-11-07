from http import HTTPStatus


def test_read_root_should_return_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'email': 'test.email@test.com',
            'password': 'test123',
        },
    )

    # Validar o status code
    assert response.status_code == HTTPStatus.CREATED

    # Validar UserPublic
    assert response.json() == {
        'username': 'testusername',
        'email': 'test.email@test.com',
        'id': 1,
    }


def test_read_all_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'testusername',
                'email': 'test.email@test.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
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


def test_fail_to_update_user(client):
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
    assert response.json() == {'detail': 'User Not Found'}

from http import HTTPStatus


def test_read_root_deve_retornar_ok(client):
    response = client.get('/')  # Act (ação)

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'olá mundo!'}  # Assert


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testeusername',
            'email': 'test@test.com',
            'password': 'password',
        },
    )

    # Voltou o status code correto?
    assert response.status_code == HTTPStatus.CREATED
    # Validar UserPublic
    assert response.json() == {
        'id': 1,
        'username': 'testeusername',
        'email': 'test@test.com',
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'testeusername',
                'email': 'test@test.com',
            }
        ]
    }


def test_get_user_from_id(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'testeusername',
        'email': 'test@test.com',
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'teste_atualizado',
            'email': 'update@test.com',
            'password': 'up123',
        },
    )

    assert response.json() == {
        'username': 'teste_atualizado',
        'email': 'update@test.com',
        'id': 1,
    }


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted.'}

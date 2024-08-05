from http import HTTPStatus


def test_read_root_deve_retornar_ok(client):
    response = client.get('/')  # Act (ação)

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'olá mundo!'}  # Assert

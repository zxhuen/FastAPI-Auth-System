

def test_get_user(client):
    response = client.get(
        "/Admin"
    )

    assert response.status_code == 200

def test_get_roles(client, seed_roles):
    response = client.get(
        "/Admin/getRoles"
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200

def test_delete_user(client, add_user):
    id = add_user

    response = client.delete(
        f"/Admin/{id}"
    )

    assert response.status_code == 200

def test_find_user_id(client, add_user):
    id = add_user

    response = client.get(
        f"/Admin/{id}"
    )

    assert response.status_code == 200
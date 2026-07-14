

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

def test_delete_user(client, add_user_for_delete):
    id = add_user_for_delete

    response = client.delete(
        f"/Admin/{id}"
    )

    assert response.status_code == 200
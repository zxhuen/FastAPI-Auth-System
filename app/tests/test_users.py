from app.services.auth_services import create_access_token, decode_access_token

def test_user_pagination(client, add_user):
    response = client.get(
        "User/pagination?skip=0&limit=1"
    )

    assert response.status_code == 200

def test_get_current_user(client, add_user):
    user_id = add_user

    token_data = {
        "sub": str(user_id)
    }

    token = create_access_token(token_data)

    response = client.get(
        f"User/getCurretnUser?token={token}"
    )

    assert response.status_code == 200

def test_edit_user(client, add_user):
    user_id = add_user

    response = client.put(
        f"User/{user_id}",
        json={
            "username": "qFLyBXskFf0KULC2RwOk"
        }
    )

    assert response.status_code == 200

def test_searh_user(client, add_user):
    response = client.get(
        "User/DeleteMe"
    )

    assert response.status_code == 200




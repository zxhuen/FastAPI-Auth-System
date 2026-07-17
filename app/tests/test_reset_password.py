
def test_verify_token(client, add_reset_password_token):
    token = add_reset_password_token

    response = client.get(
        f"/forget-password/verify-token?token={token}"
    )
    print(response.status_code)
    print(response.json())
    assert response.status_code == 200

def test_reset_password(client, add_reset_password_token):
    token = add_reset_password_token    

    response = client.post(
        f"/forget-password/validate-token?token={token}",
        json={
            "password": "password123"
        }
    )

    assert response.status_code == 200








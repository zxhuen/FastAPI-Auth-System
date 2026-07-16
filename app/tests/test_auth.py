from app.services.email_verification import generate_verification_token

"""
def test_register(client):
    response = client.post(
        "/Register",
        json={
            "username": "ZxhuenZxhuen",
            "email": "zxhuen324@gmail.com",
            "hashed_password": "ZxhuenZxhuen"
        }
    )

    assert response.status_code == 201




def test_login(client):

    response = client.post(
        "/Login/Login",
        json={
            "username": "ZxhuenZxhuen",
            "password": "ZxhuenZxhuen"
        }
    )

    assert response.status_code == 200

    print(response.status_code)
    print(response.json())

    resp = response.json()

    assert "access_token" in resp
    assert resp["token_type"] == "bearer"
    
"""

def test_verify_email(client, add_user):
    user_id = add_user

    token = generate_verification_token(user_id)

    response = client.get(
        f"auth/verify-email?token={token}"
    )

    assert response.status_code == 200
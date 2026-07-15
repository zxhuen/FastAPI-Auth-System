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


def test_refresh_token(client, add_refresh_token):
    token = add_refresh_token
    client.cookies.set("refresh_token", token)
    print(client.cookies)
    response = client.post(
        "/Refresh"
    )
    print(response.json())
    assert response.status_code == 200
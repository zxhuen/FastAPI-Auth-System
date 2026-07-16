def test_refresh_token(client, add_refresh_token):
    token = add_refresh_token

    response = client.post(
        f"Refresh?refresh_token={token}"
    )

    assert response.status_code == 200
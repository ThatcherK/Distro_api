import json

def test_encode_token(test_app, test_database):
    test_token = test_database[1]
    assert isinstance(test_token, str)

def test_invite_user(test_app, test_database):
    test_token = test_database[1]
    client = test_app.test_client()
    resp = client.post(
        "/invited_users",
        data=json.dumps({"email": "momo@mail.com", "role_id": 2}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert "momo@mail.com" in data["invitedUser"].get("email")

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

def test_get_invited_users(test_app, test_database):
    test_token = test_database[1]
    client = test_app.test_client()
    client.post(
        "/invited_users",
        data=json.dumps({"email": "moma@mail.com", "role_id": 2}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    resp = client.get("/invited_users", headers={"Authorization": f"Bearer {test_token}"})
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "moma@mail.com" in data.get("invited_users")[0].get("email")
    assert len(data.get("invited_users")) == 1

def test_invite_user_no_authToken(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/invited_users",
        data=json.dumps({"email": "man@mail.com", "role_id": 2}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    print(data)
    assert resp.status_code == 401
    assert "Provide valid auth Token" in data.get("message")

def test_invite_user_invalid_fields(test_app, test_database):
    test_token = test_database[1]
    client = test_app.test_client()
    resp = client.post(
        "/invited_users",
        data=json.dumps({}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Invalid payload" in data["message"]

def test_invite_user_missing_fields(test_app, test_database):
    test_token = test_database[1]
    client = test_app.test_client()
    resp = client.post(
        "/invited_users",
        data=json.dumps({ "role_id": 3}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Invalid payload" in data["message"]

def test_register_user(test_app, test_database):
    test_token = test_database[1]
    client = test_app.test_client()
    resp1 = client.post(
        "/invited_users",
        data=json.dumps({ "email": "paul@mail.io", "role_id": 2}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    data1 = json.loads(resp1.data.decode())
    invite_code = data1["invitedUser"].get("invite_code")
    resp2 = client.post(
        "/register",
        data=json.dumps(
            {
                "username": "Pal",
                "password": "password890",
                "invite_code": invite_code,
            }
        ),
        content_type="application/json",
    )
    data2 = json.loads(resp2.data.decode())
    assert resp2.status_code == 201
    assert "Pal" in data2.get("user").get("username")

def test_signup_duplicate_username(test_app, test_database):

    test_token = test_database[1]
    client = test_app.test_client()
    resp1 = client.post(
        "/invited_users",
        data=json.dumps({"email": "my@mail.io", "role_id": 2}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    data1 = json.loads(resp1.data.decode())
    invite_code = data1["invitedUser"].get("invite_code")
    client.post(
        "/register",
        data=json.dumps(
            {
                "username": "my",
                "password": "password600",
                "invite_code": invite_code,
            }
        ),
        content_type="application/json",
    )
    resp2 = client.post(
        "/register",
        data=json.dumps(
            {
                "username": "my",
                "password": "password600",
                "invite_code": invite_code,
            }
        ),
        content_type="application/json",
    )

    data2 = json.loads(resp2.data.decode())
    assert resp2.status_code == 400
    assert "This user already exists" in data2.get("message")

def test_login(test_app, test_database):
    test_token = test_database[1]
    client = test_app.test_client()
    resp1 = client.post(
        "/invited_users",
        data=json.dumps({"email": "myself@mail.io", "role_id": 1}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    data1 = json.loads(resp1.data.decode())
    invite_code = data1["invitedUser"].get("invite_code")
    client.post(
        "/register",
        data=json.dumps(
            {
                "username": "myself",
                "password": "password900",
                "invite_code": invite_code,
            }
        ),
        content_type="application/json",
    )
    resp2 = client.post(
        "/login",
        data=json.dumps({"username": "myself", "password": "password900"}),
        content_type="application/json",
    )
    data2 = json.loads(resp2.data.decode())
    assert resp2.status_code == 200
    assert "Success" in data2.get("status")

def test_login_invalid_password_or_username(test_app, test_database):
    test_token = test_database[1]
    client = test_app.test_client()
    resp1 = client.post(
        "/invited_users",
        data=json.dumps({"email": "moself@mail.io", "role_id": 3}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    data1 = json.loads(resp1.data.decode())
    invite_code = data1["invitedUser"].get("invite_code")
    client.post(
        "/register",
        data=json.dumps(
            {
                "username": "moself",
                "password": "password900",
                "invite_code": invite_code,
            }
        ),
        content_type="application/json",
    )
    resp2 = client.post(
        "/login",
        data=json.dumps({"username": "moself", "password": "password00"}),
        content_type="application/json",
    )
    data2 = json.loads(resp2.data.decode())
    assert resp2.status_code == 401
    assert "Invalid username or password" in data2.get("message")

def test_login_invalid_json(test_app, test_database):
    test_token = test_database[1]
    client = test_app.test_client()
    resp1 = client.post(
        "/invited_users",
        data=json.dumps({"email": "muself@mail.io", "role_id": 3}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    data1 = json.loads(resp1.data.decode())
    invite_code = data1["invitedUser"].get("invite_code")
    client.post(
        "/register",
        data=json.dumps(
            {
                "username": "muself",
                "password": "password900",
                "invite_code": invite_code,
            }
        ),
        content_type="application/json",
    )
    resp2 = client.post(
        "/login",
        data=json.dumps({}),
        content_type="application/json",
    )
    data2 = json.loads(resp2.data.decode())
    assert resp2.status_code == 400
    assert "Invalid payload" in data2.get("message")
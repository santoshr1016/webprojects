import json
from project.api.models import User


# from project import db

# # POST Route Test Cases
def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"username": "test123", "email": "test123@example.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "test123@example.com was added!" in data["message"]


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post("/users", data=json.dumps({}), content_type="application/json", )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"email": "john@example.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        "/users",
        data=json.dumps({"username": "test123", "email": "test123@example.com"}),
        content_type="application/json",
    )
    resp = client.post(
        "/users",
        data=json.dumps({"username": "test123", "email": "test123@example.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That email already exists." in data["message"]


"""
def test_single_user(test_app, test_database):
    user = User(username='user1', email='user1@example.com')
    db.session.add(user)
    db.session.commit()
    client = test_app.test_client()
    resp = client.get(f'/users/{user.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'user1' in data['username']
    assert 'user1@example.com' in data['email']
"""


# GET Route Test Cases
def test_single_user(test_app, test_database, add_user):
    user = add_user("user1", "user1@example.com")
    client = test_app.test_client()
    resp = client.get(f"/users/{user.id}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "user1" in data["username"]
    assert "user1@example.com" in data["email"]


def test_single_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


# def test_all_users(test_app, test_database, add_user):
#     add_user('test123', 'test123@gmail.com')
#     add_user('fletcher', 'fletcher@notreal.com')
#     client = test_app.test_client()
#     resp = client.get('/users')
#     data = json.loads(resp.data.decode())
#     assert resp.status_code == 200
#     # assert len(data) == 2
#     assert len(data) == 4
#     assert 'test123' in data[2]['username']
#     assert 'test123@gmail.com' in data[2]['email']
#     assert 'fletcher' in data[3]['username']
#     assert 'fletcher@notreal.com' in data[3]['email']


def test_all_users(test_app, test_database, add_user):
    test_database.session.query(User).delete()  # new
    add_user("test123", "test123@gmail.com")
    add_user("fletcher", "fletcher@notreal.com")
    client = test_app.test_client()
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert "test123" in data[0]["username"]
    assert "test123@gmail.com" in data[0]["email"]
    assert "fletcher" in data[1]["username"]
    assert "fletcher@notreal.com" in data[1]["email"]


# DELETE Route Test Cases
def test_remove_user(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    user = add_user("user-to-be-removed", "remove-me@gmail.com")
    client = test_app.test_client()
    resp_one = client.get("/users")
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data) == 1
    resp_two = client.delete(f"/users/{user.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert 'remove-me@gmail.com was removed!' in data['message']
    resp_three = client.get("/users")
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    assert len(data) == 0


def test_remove_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


# PUT Route Test Cases
def test_update_user(test_app, test_database, add_user):
    user = add_user("user-to-be-updated", "update-me@fake.io")
    client = test_app.test_client()
    resp_one = client.put(
        f"/users/{user.id}",
        data=json.dumps({"username": "me", "email": "me@fake.io"}),
        content_type="application/json",
    )
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert f"{user.id} was updated!" in data["message"]
    resp_two = client.get(f"/users/{user.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert "me" in data["username"]
    assert "me@fake.io" in data["email"]


def test_update_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(
        "/users/1",
        data=json.dumps({}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_update_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(
        "/users/1",
        data=json.dumps({"email": "me@cool.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_update_user_does_not_exist(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(
        "/users/999",
        data=json.dumps({"username": "me", "email": "me@fake.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]

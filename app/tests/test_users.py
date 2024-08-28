from http import HTTPStatus
import requests
from app.tests.test_functions import create_user_payload, create_contest_payload, ENDPOINT


def test_user_create():
    payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.CREATED

    user_data = create_response.json()
    assert user_data["first_name"] == payload["first_name"]
    assert user_data["last_name"] == payload["last_name"]
    assert user_data["email"] == payload["email"]

    user_id = user_data["id"]
    get_response = requests.get(f"{ENDPOINT}/users/{user_id}")
    assert get_response.json()["first_name"] == payload["first_name"]
    assert get_response.json()["last_name"] == payload["last_name"]
    assert get_response.json()["email"] == payload["email"]

    delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()["first_name"] == payload["first_name"]
    assert delete_response.json()["last_name"] == payload["last_name"]
    assert delete_response.json()["email"] == payload["email"]
    assert delete_response.json()["status"] == "deleted"


def test_user_create_wrong_email():
    payload = create_user_payload()
    payload["email"] = "Ivantest.ru"
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST


def test_show_contests():
    payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
    assert create_response.status_code == HTTPStatus.CREATED

    user_data = create_response.json()
    user_id = user_data["id"]
    payload = create_contest_payload([user_id])
    create_response = requests.post(f"{ENDPOINT}/contests/create", json=payload)
    contest_id = create_response.json()["id"]
    assert create_response.status_code == HTTPStatus.CREATED

    get_response = requests.get(f"{ENDPOINT}/users/{user_id}/contests")
    assert isinstance(get_response.json()["contests"], list)
    assert len(get_response.json()["contests"]) == 1
    assert get_response.json()["contests"][0]["id"] == create_response.json()["id"]
    assert get_response.json()["contests"][0]["name"] == create_response.json()["name"]
    assert get_response.json()["contests"][0]["sport"] == create_response.json()["sport"]
    assert get_response.json()["contests"][0]["status"] == create_response.json()["status"]
    assert get_response.json()["contests"][0]["participants"] == create_response.json()["participants"]
    assert get_response.json()["contests"][0]["winner"] == create_response.json()["winner"]

    delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK

    delete_response = requests.delete(f"{ENDPOINT}/contests/{contest_id}")
    assert delete_response.status_code == HTTPStatus.OK


def test_get_users_leaderboard():
    n = 3
    users = []
    for _ in range(n):
        payload = create_user_payload()
        create_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
        assert create_response.status_code == HTTPStatus.CREATED
        users.append(create_response.json()["id"])
    payload_list = {"type": "list", "sort": "asc"}
    get_response = requests.get(f"{ENDPOINT}/users/leaderboard", json=payload_list)
    leaderboard = get_response.json()["users"]
    assert isinstance(leaderboard, list)
    assert len(leaderboard) == n

    payload_graph = {"type": "graph"}
    get_response = requests.get(f"{ENDPOINT}/users/leaderboard", json=payload_graph)
    assert get_response.text == '<img src= "/static/users_leaderboard.png">'

    for user_id in users:
        delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
        assert delete_response.status_code == HTTPStatus.OK

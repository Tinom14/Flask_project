from http import HTTPStatus
import requests
from app.tests.test_functions import create_user_payload, create_contest_payload, ENDPOINT


def test_contest_create():
    n = 3
    users = []
    for _ in range(n):
        payload_user = create_user_payload()
        create_response = requests.post(f"{ENDPOINT}/users/create", json=payload_user)
        assert create_response.status_code == HTTPStatus.CREATED
        users.append(create_response.json()["id"])
    payload = create_contest_payload(users)
    create_response = requests.post(f"{ENDPOINT}/contests/create", json=payload)
    assert create_response.status_code == HTTPStatus.CREATED

    contest_data = create_response.json()
    assert contest_data["name"] == payload["name"]
    assert contest_data["sport"] == payload["sport"]
    assert contest_data["participants"] == payload["participants"]
    assert contest_data["status"] == "STARTED"
    assert contest_data["winner"] == "null"

    contest_id = contest_data["id"]
    get_response = requests.get(f"{ENDPOINT}/contests/{contest_id}")
    assert get_response.json()["name"] == payload["name"]
    assert get_response.json()["sport"] == payload["sport"]
    assert get_response.json()["participants"] == payload["participants"]
    assert get_response.json()["status"] == "STARTED"
    assert get_response.json()["winner"] == "null"

    delete_response = requests.delete(f"{ENDPOINT}/contests/{contest_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()["name"] == payload["name"]
    assert delete_response.json()["sport"] == payload["sport"]
    assert delete_response.json()["participants"] == payload["participants"]
    assert delete_response.json()["status_del"] == "deleted"

    for user_id in users:
        delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
        assert delete_response.status_code == HTTPStatus.OK


def test_contest_create_wrong_data():
    payload_user = create_user_payload()
    payload_user["sport"] = "box"
    create_user_response = requests.post(f"{ENDPOINT}/users/create", json=payload_user)
    payload = create_contest_payload([create_user_response.json()["id"]])
    create_response = requests.post(f"{ENDPOINT}/contests/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST
    delete_response = requests.delete(f"{ENDPOINT}/users/{create_user_response.json()["id"]}")

    payload = create_contest_payload([-1])
    create_response = requests.post(f"{ENDPOINT}/contests/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST


def test_contest_finish():
    n = 2
    users = []
    for _ in range(n):
        payload = create_user_payload()
        create_user_response = requests.post(f"{ENDPOINT}/users/create", json=payload)
        users.append(create_user_response.json()["id"])

    payload = create_contest_payload(users)
    create_response = requests.post(f"{ENDPOINT}/contests/create", json=payload)

    contest_id = create_response.json()["id"]
    payload = {"winner" : users[0]}
    post_response = requests.post(f"{ENDPOINT}/contests/{contest_id}/finish", json=payload)
    assert post_response.status_code == HTTPStatus.OK
    assert post_response.json()["status"] == "FINISHED"
    assert post_response.json()["winner"] == users[0]

    delete_response = requests.delete(f"{ENDPOINT}/contests/{contest_id}")
    assert delete_response.status_code == HTTPStatus.OK

    for user_id in users:
        delete_response = requests.delete(f"{ENDPOINT}/users/{user_id}")
        assert delete_response.status_code == HTTPStatus.OK



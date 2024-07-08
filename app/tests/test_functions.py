from uuid import uuid4

ENDPOINT = "http://127.0.0.1:5000"


def create_user_payload():
    return {
        "first_name": "Ivan" + str(uuid4()),
        "last_name": "Ivanov" + str(uuid4()),
        "email": "Ivan@test.ru",
        "sport": "chess"
    }


def create_contest_payload(participants):
    return {
        "name": "tour" + str(uuid4()),
        "sport": "chess",
        "participants": participants
    }

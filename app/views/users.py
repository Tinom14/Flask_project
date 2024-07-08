from app import app, USERS, CONTESTS, models
from flask import request, Response, url_for
import json
from http import HTTPStatus
import matplotlib.pyplot as plt

@app.post('/users/create')
def user_create():
    data = request.get_json()
    id = len(USERS)
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    sport = data['sport']
    if not models.User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST, response='Введен некорректный email')
    user = models.User(id, first_name, last_name, email, sport)
    USERS.append(user)
    return Response(
        json.dumps(user.to_dict()),
        status=HTTPStatus.CREATED,
        mimetype="application/json"
    )


@app.get('/users/<int:user_id>')
def get_user(user_id):
    if not models.User.is_valid_id(user_id):
        return Response(response='Пользователя с данным id не существует', status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    return Response(
        json.dumps(user.to_dict()),
        HTTPStatus.OK,
        mimetype="application/json"
    )


@app.get('/users/<int:user_id>/contests')
def show_contests(user_id):
    if not models.User.is_valid_id(user_id):
        return Response(response='Пользователя с таким номером не существует', status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    contests = []
    for id_cont in user.contests:
        contest = CONTESTS[id_cont]
        contests.append(contest.to_dict())
    return Response(
        json.dumps({
            'contests': contests
        }),
        HTTPStatus.OK,
        mimetype="application/json"
    )


@app.get('/users/leaderboard')
def get_users_leaderboard():
    data = request.get_json()
    leaderboard_type = data['type']
    if leaderboard_type == 'list':
        sorting_direction = data['sort']
        if sorting_direction == 'asc':
            leaderboard = models.User.get_leaderboard()
        elif sorting_direction == 'desc':
            leaderboard = models.User.get_leaderboard(True)
        else:
            return Response(response='Выберите вид сортировки asc/desc', status=HTTPStatus.BAD_REQUEST)
        return Response(
            json.dumps({'users': leaderboard}),
            HTTPStatus.OK,
            mimetype="application/json"
        )
    elif leaderboard_type == 'graph':
        leaderboard = models.User.get_leaderboard()
        fig, ax = plt.subplots()
        user_names = [f'{user['first_name']} {user['last_name']} ({user['id']})' for user in leaderboard]
        amount_contests = [len(user['contests']) for user in leaderboard]
        ax.bar(user_names, amount_contests)
        ax.set_ylabel('amount_contests')
        ax.set_title('User leaderboard by contests')
        plt.savefig("app/static/users_leaderboard.png")
        return Response(
            f"""<img src= "{url_for('static', filename='users_leaderboard.png')}">""",
            status=HTTPStatus.OK,
            mimetype="text/html"
        )
    else:
        return Response(response='Выберите вид сортировки list/graph', status=HTTPStatus.BAD_REQUEST)


@app.delete('/users/<int:user_id>')
def delete_user(user_id):
    if not models.User.is_valid_id(user_id):
        return Response(response='Пользователя с данным id не существует', status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    user.status = "deleted"
    del_user = user.to_dict()
    del_user["status"] = user.status
    return Response(
        json.dumps(del_user),
        HTTPStatus.OK,
        mimetype="application/json"
    )
from app import app, USERS, CONTESTS, models
from flask import request, Response, url_for
import json
from http import HTTPStatus
import matplotlib.pyplot as plt


@app.route('/')
def index():
    return "Hello world"


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



@app.post('/contests/create')
def contest_create():
    data = request.get_json()
    id = len(CONTESTS)
    name = data['name']
    sport = data['sport']
    participiants = data['participants']
    for user_id in participiants:
        if models.User.is_valid_id(user_id):
            user = USERS[user_id]
            if user.sport != sport:
                return Response(response='В списке участников пользователь из другого вида спорта',
                                status=HTTPStatus.BAD_REQUEST)
        else:
            return Response(response='В списке участников несуществующий user', status=HTTPStatus.BAD_REQUEST)
    for user_id in participiants:
        user = USERS[user_id]
        user.contests.append(id)
    contest = models.Contest(id, name, sport, participiants)
    CONTESTS.append(contest)
    return Response(
        json.dumps(contest.to_dict()),
        status=HTTPStatus.CREATED,
        mimetype="application/json"
    )



@app.get('/contests/<int:contest_id>')
def get_contest(contest_id):
    if not models.Contest.is_valid_id(contest_id):
        return Response(response='Соревнования с таким номером не существует',status=HTTPStatus.NOT_FOUND)
    contest = CONTESTS[contest_id]
    return Response(
        json.dumps(contest.to_dict()),
        HTTPStatus.OK,
        mimetype="application/json"
    )



@app.post('/contests/<int:contest_id>/finish')
def contest_finish(contest_id):
    if not models.Contest.is_valid_id(contest_id):
        return Response(response='Соревнования с таким номером не существует', status=HTTPStatus.NOT_FOUND)
    contest = CONTESTS[contest_id]
    if contest.status == 'FINISHED':
        return Response(response='Соревнование уже завершено', status=HTTPStatus.BAD_REQUEST)
    winner = request.get_json()['winner']
    if winner in contest.participiants:
        contest.winner = winner
    else:
        return Response(response='Победитель не участвовал в соревновании', status=HTTPStatus.BAD_REQUEST)
    contest.status = 'FINISHED'
    return Response(
        json.dumps(contest.to_dict()),
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

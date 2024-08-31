from app import app, USERS, CONTESTS, models
from flask import request, Response
import json
from http import HTTPStatus


@app.post('/contests/create')
def contest_create():
    data = request.get_json()
    id = len(CONTESTS)
    name = data['name']
    sport = data['sport']
    participants = data['participants']
    for user_id in participants:
        if models.User.is_valid_id(user_id):
            user = USERS[user_id]
            if user.sport != sport:
                return Response(response='В списке участников пользователь из другого вида спорта',
                                status=HTTPStatus.BAD_REQUEST)
        else:
            return Response(response='В списке участников несуществующий user', status=HTTPStatus.BAD_REQUEST)
    for user_id in participants:
        user = USERS[user_id]
        user.contests.append(id)
    contest = models.Contest(id, name, sport, participants)
    CONTESTS.append(contest)
    return Response(
        json.dumps(contest.to_dict()),
        status=HTTPStatus.CREATED,
        mimetype="application/json"
    )


@app.get('/contests/<int:contest_id>')
def get_contest(contest_id):
    if not models.Contest.is_valid_id(contest_id):
        return Response(response='Соревнования с таким номером не существует', status=HTTPStatus.NOT_FOUND)
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
    if winner in contest.participants:
        contest.winner = winner
    else:
        return Response(response='Победитель не участвовал в соревновании', status=HTTPStatus.BAD_REQUEST)
    contest.status = 'FINISHED'
    return Response(
        json.dumps(contest.to_dict()),
        HTTPStatus.OK,
        mimetype="application/json"
    )


@app.delete('/contests/<int:contest_id>')
def delete_contest(contest_id):
    if not models.Contest.is_valid_id(contest_id):
        return Response(response='Соревнования с таким номером не существует', status=HTTPStatus.NOT_FOUND)
    contest = CONTESTS[contest_id]
    contest.status_del = "deleted"
    del_contest = contest.to_dict()
    del_contest["status_del"] = contest.status_del
    return Response(
        json.dumps(del_contest),
        HTTPStatus.OK,
        mimetype="application/json"
    )

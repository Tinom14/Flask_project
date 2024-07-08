from app import app, USERS, CONTESTS


@app.route('/')
def index():
    response = (
        f'<h1>hello</h1>'
        f"USERS:<br>{'<br>'.join([user.repr() for user in USERS])}<br>"
        f"CONTESTS:<br>{'<br>'.join([contest.repr() for contest in CONTESTS])}<br>"
    )
    return response




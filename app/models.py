from app import app, USERS, CONTESTS
import re


class User:
    def __init__(self, id, first_name, last_name, email, sport):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.sport = sport
        self.contests = []
        self.status = "created"

    @staticmethod
    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    @staticmethod
    def is_valid_id(user_id):
        return 0 <= user_id < len(USERS) and USERS[user_id].status != "deleted"

    def repr(self):
        if self.status == "created":
            return f'{self.id} {self.first_name} {self.last_name}'
        else:
            return "User deleted"

    def __lt__(self, other):
        return len(self.contests) < len(other.contests)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "contests": self.contests
        }

    @staticmethod
    def get_leaderboard(rev=False):
        return [user.to_dict() for user in sorted(USERS, reverse=rev) if User.is_valid_id(user.id)]


class Contest:
    def __init__(self, id, name, sport, participants=[], status="STARTED", winner='null'):
        self.id = id
        self.name = name
        self.sport = sport
        self.participants = participants
        self.status = status
        self.winner = winner
        self.status_del = ""

    @staticmethod
    def is_valid_id(contest_id):
        return 0 <= contest_id < len(CONTESTS) and CONTESTS[contest_id].status_del != "deleted"

    def repr(self):
        return f'{self.id} {self.name} {self.sport}'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "sport": self.sport,
            "status": self.status,
            "participants": self.participants,
            "winner": self.winner
        }

from src.database import get_user

def login(username, password):
    user = get_user(username)

    if user and user[1] == password:
        return user[2]

    return None
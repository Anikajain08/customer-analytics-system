def login(username, password):
    user = get_user(username)
    print("DEBUG USER:", user)

    if user and user[1] == password:
        return user[2]

    return None
def parse_user(user):
    try:
        return ({
            "id": user.id,
            "username": user.username,
        })
    except AttributeError:
        return None

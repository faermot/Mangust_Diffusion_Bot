def get_user_id(message):
    user_id = message.from_user.id
    user_id = str(user_id)
    return user_id
def get_user_id(message):
    user_id = message.from_user.id
    user_id = str(user_id)
    return user_id


def get_keys():
    with open('keys', 'r') as f:
        keys = [line.strip() for line in f.readlines()]
    return keys


def get_used_keys():
    with open("used_keys", 'r') as f:
        used_keys = [line.strip() for line in f.readlines()]
    return used_keys


def set_used_key(key):
    with open("used_keys", 'a') as f:
        f.write("\n" + key)
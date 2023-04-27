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
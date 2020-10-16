from . import models as db
def login(**kwargs):
    username = kwargs.get('username', None)
    password = kwargs.get('password', None)
    if not username:
        return 400, {"msg": "Missing username parameter"}
    if not password:
        return 400, {"msg": "Missing password parameter"}

    if username != 'test' or password != 'test':
        return 401, {"msg": "Bad username or password"}
    return 200, db.UserObj(username=username,roles=["client","admin"])

from uuid import uuid4
from datetime import datetime as dt


class UserObj(object):
    def __init__(self, username, roles):
        self.username = username
        self.roles = roles
        self.token_randomize = str(uuid4())

    @property
    def token_access(self):
        return self.__token_access

    @token_access.setter
    def token_access(self, token_access):
        self.__token_access = token_access

    @property
    def token_refresh(self):
        return self.__token_refresh["val"]

    @token_refresh.setter
    def token_refresh(self, token_refresh):
        self.__token_refresh = dict(val=token_refresh, ref=dt.utcnow())

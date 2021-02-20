import datetime

# トークン
class AuthToken:
    expire = datetime.datetime.now()
    value = ""

    def __init__(self):
        pass

import datetime
import uuid

# トークン
class AuthToken:
    expire = datetime.datetime.now()
    value = ""

    def __init__(self):
        self.value = str(uuid.uuid4())

    def setExpireMinutes(self, base_date, after_minuts):
        self.expire = base_date + datetime.timedelta(minutes=after_minuts)

    def setExpireDay(self, base_date, after_day):
        self.expire = base_date + datetime.timedelta(days=after_day)

    def isExpired(self, check_datetime):
        return self.value <= check_datetime

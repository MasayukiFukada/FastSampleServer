from auth_token import AuthToken
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

# 認証データ構造定義
class AuthData:
    id = -1
    mail_address = ""
    password = ""
    access_token = AuthToken()
    refresh_token = AuthToken()
    is_active = False

    def __init__(self, id, mail_address, password, is_active):
        self.id = id
        self.mail_address = mail_address
        self.password = password
        self.is_active = is_active

    def validate(self, check_mail_address, check_password):
        is_same_address = self.mail_address == check_mail_address
        is_same_password = self.password == check_password
        return is_same_address & is_same_password

# 認証リポジトリ
class AuthRepository:
    data = []

    def __init__(self):
        admin = AuthData(0, "admin@example.com", "admin", True)
        self._append(admin)

    # 内部専用の追加処理
    def _append(self, account):
        self.data.append(account)

    def authenticate(self, input_mail_address, input_password):
        for index in range(len(self.data)):
            identify = self.data[index]
            if not identify.validate(input_mail_address, input_password):
                continue
            # 認証された
            contents = { "id": identify.id }
            headers = {}
            headers["x-auth-token"] = identify.access_token.value
            headers["x-refresh-token"] = identify.refresh_token.value
            return JSONResponse(status_code=status.HTTP_200_OK, content=contents, headers=headers)

        # 認証されなかった
        contents = {}
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=contents)


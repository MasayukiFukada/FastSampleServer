from auth_token import AuthToken
from fastapi import status
from fastapi.responses import JSONResponse
import datetime

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

    def refreshToken(self):
        self.access_token = AuthToken()
        self.refresh_token = AuthToken()
        baseDatetime = datetime.datetime.now()
        self.access_token.setExpireMinutes(baseDatetime, 1)
        self.refresh_token.setExpireMinutes(baseDatetime, 3)

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

    def authenticate(self, post_credential):
        for index in range(len(self.data)):
            identify = self.data[index]
            if not identify.validate(post_credential.mail_address, post_credential.password):
                continue
            # 認証された
            identify.refreshToken()
            contents = {"id": identify.id}
            headers = {}
            headers["x-auth-token"] = identify.access_token.value
            headers["x-refresh-token"] = identify.refresh_token.value
            return JSONResponse(status_code=status.HTTP_200_OK, content=contents, headers=headers)

        # 認証されなかった
        contents = {}
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=contents)

    def refresh(self, id, post_refresh_token):
        try:
            num_id = int(id)
            for index in range(len(self.data)):
                identify = self.data[index]
                if identify.id != num_id:
                    continue
                if identify.refresh_token.value != post_refresh_token.refresh_token:
                    # リフレッシュトークンが違う
                    contents = {"refresh": False}
                    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=contents)
                if identify.refresh_token.isExpired(datetime.datetime.now()):
                    # リフレッシュトークンが期限切れ
                    contents = {"refresh": False}
                    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=contents)
                # リフレッシュ許可
                identify.refreshToken()
                contents = {"id": identify.id}
                headers = {}
                headers["x-auth-token"] = identify.access_token.value
                headers["x-refresh-token"] = identify.refresh_token.value
                return JSONResponse(status_code=status.HTTP_200_OK, content=contents, headers=headers)
            # その他の事象
            contents = {"refresh": False}
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=contents)
        except ValueError:
            contents = {"refresh": False}
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=contents)

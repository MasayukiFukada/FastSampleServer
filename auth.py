from auth_token import AuthToken

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

    def validate(self):
        return True

# 認証リポジトリ
class AuthRepository:
    data = []

    def __init__(self):
        admin = AuthData(0, "admin@example.com", "admin", True)
        self.append(admin)

    # 読み込み
    def load(self):
        pass

    # 追加
    def append(self, new_auth):
        if not new_auth.validate():
            return False

        # 新しい ID (最大値)を割り当てる
        self.data.append(new_auth)
        return True

    # 削除
    def remove(self, target_auth):
        for index in range(len(self.data)):
            if self.data[index].id == target_auth.id:
                self.data.remove(index)
                break

    # 更新
    def update(self, update_auth):
        for index in range(len(self.data)):
            if self.data[index].id == update_auth.id:
                self.data[index] = update_auth

    # 最大 ID を取得
    def _max_id(self):
        return -1

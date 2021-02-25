from fastapi import FastAPI, Header, Depends, HTTPException
import auth
import item
from post_parameter import PostCredential, PostRefreshToken, PostItem
import datetime

tags_metadata = [
    {
        "name": "認証",
        "description": "ログインやトークンの管理など認証に関する操作を扱います。",
    },
    {
        "name": "アイテム",
        "description": "項目の CRUD 操作を扱います。",
    }
]

item_repository = item.ItemRepository()
auth_repository = auth.AuthRepository()

app = FastAPI(
    title="高速サンプルサーバー",
    description="開発環境の確認などサンプルのサーバーが必要になった時に使います。",
    version="0.1.0",
    openapi_tags=tags_metadata
)


def get_auth_token(Authorization: str = Header(None)):
    if Authorization is None:
        raise HTTPException(
            401, headers={"WWW-Authenticate": 'Bearer realm="token_required"'})
    if Authorization[:7] != "Bearer ":
        raise HTTPException(
            400, headers={"WWW-Authenticate": 'Bearer realm="invalid_request"'})
    return Authorization[7:]


def is_authorized(Authorization: str = Header(None)):
    token = get_auth_token(Authorization)
    return auth_repository.isInclude(token, datetime.datetime.now())

# ------------------------------------------------------------------------------


@app.post("/auth/token", tags=["認証"], description="トークンを作成します ※ ログイン")
def create_token(credential: PostCredential):
    return auth_repository.authenticate(credential)


@app.post("/auth/refresh", tags=["認証"], description="トークンを更新します")
def refresh_token(id: int, refresh_token: PostRefreshToken):
    return auth_repository.refresh(id, refresh_token)


@app.delete("/auth/token", tags=["認証"], description="トークンを削除します ※ログアウト")
def drop_token(token: str = Depends(get_auth_token)):
    return auth_repository.remove(token)

# ------------------------------------------------------------------------------


@app.get("/items", tags=["アイテム"], description="一覧を取得します")
def get_items():
    return item_repository.list()


@app.post("/item", tags=["アイテム"], description="新規登録します")
def create_item(post_item: PostItem, isAuthorized: str = Depends(is_authorized)):
    if not isAuthorized:
        raise HTTPException(401)
    return item_repository.append(post_item)


@app.put("/item/{id}", tags=["アイテム"], description="更新します")
def update_item(id: int, post_item: PostItem, isAuthorized: str = Depends(is_authorized)):
    if not isAuthorized:
        raise HTTPException(401)
    return item_repository.update(id, post_item)


@app.delete("/item/{id}", tags=["アイテム"], description="削除します")
def remove_item(id: int, isAuthorized: str = Depends(is_authorized)):
    if not isAuthorized:
        raise HTTPException(401)
    return item_repository.remove(id)

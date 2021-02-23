from fastapi import FastAPI
import auth
import item

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

# ------------------------------------------------------------------------------

@app.post("/auth/token", tags=["認証"], description="トークンを作成します ※ ログイン")
def create_token(mail_address, password):
  return auth_repository.authenticate(mail_address, password)

@app.post("/auth/refresh", tags=["認証"], description="トークンを更新します")
def refresh_token():
  return {}

# ------------------------------------------------------------------------------

@app.get("/items", tags=["アイテム"], description="一覧を取得します")
def get_items():
  return item_repository.list()

@app.post("/item", tags=["アイテム"], description="新規登録します")
def create_item(image_base64, link_url):
  max_id = item_repository.max_id()
  new_item = item.ItemData(max_id, image_base64, link_url)
  item_repository.append(new_item)
  return { "item_id" : max_id }

@app.put("/item/{id}", tags=["アイテム"], description="更新します")
def update_item(id, image_base64, link_url):
  try:
    num_id = int(id)
    replace_item = item.ItemData(num_id, image_base64, link_url)
    isFound = item_repository.update(replace_item)
    return { "update" : isFound }
  except ValueError:
    return { "update" : False }


@app.delete("/item/{id}", tags=["アイテム"], description="削除します")
def remove_item(id):
  try:
    num_id = int(id)
    isFound = item_repository.remove(num_id)
    return { "delete" : isFound }
  except ValueError:
    return { "delete" : False }


from fastapi import status, HTTPException
from fastapi.responses import JSONResponse

# アイテムデータ構造定義


class ItemData:
    id = -1
    image_base64 = ""
    link_url = ""

    def __init__(self, id, image_base64, link_url):
        self.id = id
        self.image_base64 = image_base64
        self.link_url = link_url

    def validate(self):
        return True

# アイテムリポジトリ


class ItemRepository:
    data = []

    def __init__(self):
        pass

    # 読み込み
    def list(self):
        return self.data

    # 追加
    def append(self, post_item):
        max_id = self.max_id()
        new_item = ItemData(max_id, post_item.image_base64, post_item.link_url)
        if not new_item.validate():
            contents = {}
            raise HTTPException(400)

        # 新しい ID (最大値)を割り当てる
        self.data.append(new_item)
        contents = {"item_id": new_item.id}
        return JSONResponse(status_code=status.HTTP_200_OK, content=contents)

    # 削除
    def remove(self, id):
        try:
            remove_id = int(id)
            for index in range(len(self.data)):
                if self.data[index].id == remove_id:
                    del self.data[index]
                    contents = {"delete": remove_id}
                    return JSONResponse(status_code=status.HTTP_200_OK, content=contents)
            raise HTTPException(404)
        except ValueError:
            raise HTTPException(400)

    # 更新
    def update(self, id, post_item):
        try:
            update_id = int(id)
            for index in range(len(self.data)):
                if self.data[index].id == update_id:
                    update_item = ItemData(
                        update_id, post_item.image_base64, post_item.link_url)
                    self.data[index] = update_item
                    contents = {"update": update_id}
                    return JSONResponse(status_code=status.HTTP_200_OK, content=contents)
            raise HTTPException(404)
        except ValueError:
            raise HTTPException(400)

    # 最大 ID を取得
    def max_id(self):
        if len(self.data) < 1:
            return 1
        return max(self.data, key=lambda x: x.id).id + 1

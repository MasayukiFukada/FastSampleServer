from fastapi import status
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
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=contents)

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
                    contents = {"delete": True}
                    return JSONResponse(status_code=status.HTTP_200_OK, content=contents)
            contents = {"delete": False}
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=contents)
        except ValueError:
            contents = {"delete": False}
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=contents)

    # 更新
    def update(self, id, post_item):
        try:
            num_id = int(id)
            for index in range(len(self.data)):
                if self.data[index].id == num_id:
                    update_item = ItemData(
                        num_id, post_item.image_base64, post_item.link_url)
                    self.data[index] = update_item
                    contents = {"update": True}
                    return JSONResponse(status_code=status.HTTP_200_OK, content=contents)
            contents = {"update": False}
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=contents)
        except ValueError:
            contents = {"update": False}
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=contents)

    # 最大 ID を取得
    def max_id(self):
        if len(self.data) < 1:
            return 1
        return max(self.data, key=lambda x: x.id).id + 1

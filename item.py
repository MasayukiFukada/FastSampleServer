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
    def append(self, new_item):
        if not new_item.validate():
            return False

        # 新しい ID (最大値)を割り当てる
        self.data.append(new_item)
        return True

    # 削除
    def remove(self, remove_id):
        for index in range(len(self.data)):
            if self.data[index].id == remove_id:
                del self.data[index]
                return True
        return False

    # 更新
    def update(self, update_item):
        for index in range(len(self.data)):
            if self.data[index].id == update_item.id:
                self.data[index] = update_item
                return True
        return False

    # 最大 ID を取得
    def max_id(self):
        if len(self.data) < 1:
            return 1
        return max(self.data, key=lambda x: x.id).id + 1

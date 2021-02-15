# Fast Sample Server

ちょっとした開発のサンプルサーバー

機能一覧
* 

## 必要な環境

* Python3
  * FastAPI
  * Uvicorn

```
$ pip3 install fastapi uvicorn
```

## 使い方

main_app.py に書いたサーバーをポート 3000 で起動

```
$ uvicorn main_app:app --port 3000

# run.sh を用意しているので実行しても良い
```

FastAPI を使用しているのでドキュメントも表示可能。
基本的に API の仕様はドキュメントを参照すること。

* API サーバー
  * http://localhost:3000
  * Swagger 形式のドキュメント
    * http://localhost:3000/docs
  * ReDoc 形式のドキュメント
    * http://localhost:3000/redoc




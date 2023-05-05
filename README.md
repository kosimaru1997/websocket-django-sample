# django-docker-sample

## 作成手順メモ

1. containerディレクトリを作成

2. Dockerfileを作成  
*WORK_DIRを./appに設定

3. requirements.txtに使用するライブラリを記述

4. dokcer-compose.ymlを作成  
*ローカルの./appディレクトリにDockerの./appディレクトリをマウント

5. 下記コマンドを実行
 - Docker上でプロジェクトを作成し、ローカルの./appディレクトリと同期する。
```sh
docker-compose run web django-admin startproject myweb .
```

6. 下記コマンドを実行
- Docker上でアプリケーションを作成し、ローカルの./appディレクトリと同期する。
```
docker-compose run web python manage.py startapp myweb_app
```

7. setting.pyにデータベース接続設定を修正する

8. docker-compose upをし、http://localhost:8000/ にアクセスできることを確認する

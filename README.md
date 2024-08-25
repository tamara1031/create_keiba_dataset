## requirements
- TODO

## 使用方法
1. docker-composeでmysqlコンテナを起動
1. get_and_insert_race_idsを実行してレースIDをDBに登録
    - 期間は好きに調整
1. get_and_insert_race_resultsを実行してレースIDに紐づくレース結果をスクレイピングしてくる
    - だいぶ時間がかかるため注意

# 前処置管理アプリ（バックエンド / Flask）

内視鏡（大腸カメラ）前処置の進捗（下剤内服・排便/便性状・腹痛/嘔気/嘔吐）を記録し、管理者側で確認できるようにするバックエンドAPIです。  
フロントエンド（別リポジトリ）からこのAPIを呼び出して利用します。

---

## 機能概要
- 便性状（提示画像）マスタの取得
- 症状マスタの取得
- 検査日（セッション）作成
- 下剤内服の記録
- 排便（便レベル）の記録
- 症状（腹痛/嘔気/嘔吐など）の記録
- 上記ログの取得（GET）

---

## 必要環境
- Python 3.x
- SQLite3

---

## セットアップ（ローカル）
### 1) 仮想環境作成 & 依存関係インストール
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

2) DB作成（schema/seed方式）
mkdir -p db
sqlite3 db/prep.db < db/schema.sql
sqlite3 db/prep.db < db/seed.sql

3) 起動
python3 app.py

---

## 「②の意味」を一言で言うと
GitHubには `prep.db`（DB本体）を入れない代わりに、  
`schema.sql`（テーブル作成）と `seed.sql`（初期データ）を使って、各PCで

- 新しく `db/prep.db` を作る
- マスタ（便レベル/症状/下剤）を入れる

という手順を書いています。

---

もし今あなたの `db/schema.sql` や `db/seed.sql` がまだ無い/場所が不安なら、こちらも確認できます：

```bash
ls -l db

動作確認例
curl http://127.0.0.1:5000/health
curl http://127.0.0.1:5000/api/stool-conditions
curl http://127.0.0.1:5000/api/symptoms

API一覧
Health

GET /health

Master

GET /api/stool-conditions

GET /api/symptoms

Exam days（セッション）

GET /api/exam-days

POST /api/exam-days

POST例：
curl -s -X POST http://127.0.0.1:5000/api/exam-days \
  -H "Content-Type: application/json" \
  -d '{"exam_id":"DEMO-001","patient_id":1,"exam_date":"2025-12-17","exam_time":"09:00"}'

Bowel movements（排便）

GET /api/exam-days/<exam_day_id>/bowel-movements

POST /api/exam-days/<exam_day_id>/bowel-movements

POST例：

curl -s -X POST http://127.0.0.1:5000/api/exam-days/1/bowel-movements \
  -H "Content-Type: application/json" \
  -d '{"recorded_at":"2025-12-17 07:30","condition_id":4,"bm_no":1}'

Symptoms（症状）

GET /api/exam-days/<exam_day_id>/symptoms

POST /api/exam-days/<exam_day_id>/symptoms

POST例：

curl -s -X POST http://127.0.0.1:5000/api/exam-days/1/symptoms \
  -H "Content-Type: application/json" \
  -d '{"recorded_at":"2025-12-17 07:40","symptom_id":2,"severity":2,"note":"少し気持ち悪い"}'

Laxatives（下剤）

POST /api/exam-days/<exam_day_id>/laxatives

POST例：

curl -s -X POST http://127.0.0.1:5000/api/exam-days/1/laxatives \
  -H "Content-Type: application/json" \
  -d '{"dose_no":1,"taken_at":"2025-12-17 06:30","laxative_type_id":1}'

補足（卒業制作向け）

実運用を想定し、DB本体（prep.db）はGitHubに含めず、schema/seedで再現する方式にしています。

Render等にデプロイする場合は、SQLiteの永続化やPostgreSQL移行も検討対象です。


---


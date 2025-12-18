import os
import sqlite3
from flask import Flask, g, jsonify, request
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "db", "prep.db")


def get_db():
    if "db" not in g:
        db_path = os.environ.get("SQLITE_DB_PATH", DEFAULT_DB_PATH)
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        g.db = conn
    return g.db


def close_db(_e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ★ ローカル開発用：すべて許可

app.teardown_appcontext(close_db)

@app.get("/health")
def health():
    return {"ok": True}

# 便レベル（提示画像）の一覧
@app.get("/api/stool-conditions")
def stool_conditions():
    db = get_db()
    rows = db.execute(
        "SELECT condition_id, label, image_path FROM stool_conditions"
    ).fetchall()
    return jsonify([dict(r) for r in rows])
    

    # 症状マスタ（腹痛/嘔気/嘔吐など）
    @app.get("/api/symptoms")
    def symptoms():
        db = get_db()
        rows = db.execute(
            "SELECT symptom_id, symptom FROM symptoms ORDER BY symptom_id"
        ).fetchall()
        return jsonify([dict(r) for r in rows])
    @app.get("/api/exam-days")
    def list_exam_days():
        db = get_db()
        rows = db.execute(
            """
            SELECT e.exam_day_id, e.exam_date, e.exam_time, e.exam_id, e.patient_id
            FROM exam_days e
            ORDER BY e.exam_date DESC, e.exam_time DESC, e.exam_day_id DESC
            """
        ).fetchall()
        return jsonify([dict(r) for r in rows])

    @app.get("/api/exam-days/<int:exam_day_id>/bowel-movements")
    def get_bm(exam_day_id: int):
        db = get_db()
        rows = db.execute(
            """
            SELECT
              s.record_id, s.exam_day_id, s.recorded_at, s.bm_no,
              s.condition_id, c.label, c.image_path
            FROM stool_records s
            JOIN stool_conditions c ON c.condition_id = s.condition_id
            WHERE s.exam_day_id = ?
            ORDER BY s.recorded_at ASC, s.record_id ASC
            """,
            (exam_day_id,),
        ).fetchall()
        return jsonify([dict(r) for r in rows])

    @app.get("/api/exam-days/<int:exam_day_id>/symptoms")
    def get_symptom_logs(exam_day_id: int):
        db = get_db()
        rows = db.execute(
            """
            SELECT
              r.record_id, r.exam_day_id, r.recorded_at,
              r.symptom_id, s.symptom, r.severity, r.note
            FROM symptom_records r
            JOIN symptoms s ON s.symptom_id = r.symptom_id
            WHERE r.exam_day_id = ?
            ORDER BY r.recorded_at ASC, r.record_id ASC
            """,
            (exam_day_id,),
        ).fetchall()
        return jsonify([dict(r) for r in rows])

    # 検査（当日セッション）作成：exam_daysに1行作る
    # 例：{"exam_id":"E20251217-001","patient_id":1,"exam_date":"2025-12-17","exam_time":"09:00"}
    @app.post("/api/exam-days")
    def create_exam_day():
        data = request.get_json(force=True) or {}
        exam_id = data.get("exam_id")
        patient_id = data.get("patient_id")
        exam_date = data.get("exam_date")
        exam_time = data.get("exam_time")

        if not exam_id or not patient_id or not exam_date:
            return {"error": "exam_id, patient_id, exam_date are required"}, 400

        db = get_db()
        db.execute(
            "INSERT INTO exam_days (exam_date, exam_time, exam_id, patient_id) VALUES (?, ?, ?, ?)",
            (exam_date, exam_time, exam_id, patient_id),
        )
        db.commit()

        row = db.execute(
            "SELECT * FROM exam_days WHERE exam_id = ?", (exam_id,)
        ).fetchone()
        return jsonify(dict(row)), 201

    # 排便記録：stool_records に追加
    # 例：{"recorded_at":"2025-12-17 07:30","condition_id":4,"bm_no":3}
    @app.post("/api/exam-days/<int:exam_day_id>/bowel-movements")
    def add_bm(exam_day_id: int):
        data = request.get_json(force=True) or {}
        recorded_at = data.get("recorded_at")
        condition_id = data.get("condition_id")
        bm_no = data.get("bm_no")

        if not recorded_at or not condition_id:
            return {"error": "recorded_at and condition_id are required"}, 400

        db = get_db()
        db.execute(
            """
            INSERT INTO stool_records (exam_day_id, recorded_at, condition_id, bm_no)
            VALUES (?, ?, ?, ?)
            """,
            (exam_day_id, recorded_at, int(condition_id), bm_no),
        )
        db.commit()
        return {"ok": True}, 201

    # 症状記録：symptom_records に追加
    # 例：{"recorded_at":"2025-12-17 07:40","symptom_id":1,"severity":2,"note":"少し気持ち悪い"}
    @app.post("/api/exam-days/<int:exam_day_id>/symptoms")
    def add_symptom(exam_day_id: int):
        data = request.get_json(force=True) or {}
        recorded_at = data.get("recorded_at")
        symptom_id = data.get("symptom_id")

        if not recorded_at or not symptom_id:
            return {"error": "recorded_at and symptom_id are required"}, 400

        severity = data.get("severity")
        note = data.get("note")

        db = get_db()
        db.execute(
            """
            INSERT INTO symptom_records (exam_day_id, recorded_at, symptom_id, severity, note)
            VALUES (?, ?, ?, ?, ?)
            """,
            (exam_day_id, recorded_at, int(symptom_id), severity, note),
        )
        db.commit()
        return {"ok": True}, 201

    # 下剤記録：laxatives に追加
    # 例：{"dose_no":1,"taken_at":"2025-12-17 06:30","laxative_type_id":2}
    @app.post("/api/exam-days/<int:exam_day_id>/laxatives")
    def add_laxative(exam_day_id: int):
        data = request.get_json(force=True) or {}
        dose_no = data.get("dose_no")
        taken_at = data.get("taken_at")
        laxative_type_id = data.get("laxative_type_id")

        if not dose_no:
            return {"error": "dose_no is required"}, 400

        db = get_db()
        db.execute(
            """
            INSERT INTO laxatives (exam_day_id, dose_no, taken_at, laxative_type_id, drug_type)
            VALUES (?, ?, ?, ?, NULL)
            """,
            (exam_day_id, int(dose_no), taken_at, laxative_type_id),
        )
        db.commit()
        return {"ok": True}, 201

    return app




if __name__ == "__main__":
    app.run(debug=True)


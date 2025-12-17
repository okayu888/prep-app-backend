PRAGMA foreign_keys = ON;

-- 症状マスタ
CREATE TABLE IF NOT EXISTS symptoms (
  symptom_id INTEGER PRIMARY KEY AUTOINCREMENT,
  symptom    TEXT NOT NULL UNIQUE
);

-- 便性状の記録（いつ、どの検査IDで、どの性状を選んだか）
CREATE TABLE IF NOT EXISTS stool_records (
  record_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  exam_id      TEXT NOT NULL,
  recorded_at  TEXT NOT NULL,          -- YYYY-MM-DD HH:MM
  condition_id INTEGER NOT NULL,
  bm_no        INTEGER,                -- 何回目の排便か（任意）
  FOREIGN KEY (exam_id) REFERENCES exam_days(exam_id),
  FOREIGN KEY (condition_id) REFERENCES stool_conditions(condition_id)
);

-- 症状の記録（腹痛・嘔吐など）
CREATE TABLE IF NOT EXISTS symptom_records (
  record_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  exam_id      TEXT NOT NULL,
  recorded_at  TEXT NOT NULL,
  symptom_id   INTEGER NOT NULL,
  severity     INTEGER,                -- 例: 0なし,1軽,2中,3強
  note         TEXT,
  FOREIGN KEY (exam_id) REFERENCES exam_days(exam_id),
  FOREIGN KEY (symptom_id) REFERENCES symptoms(symptom_id)
);


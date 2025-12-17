CREATE TABLE patients (
  patient_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  card_id      TEXT UNIQUE,
  name         TEXT,
  birthdate    TEXT,
  age          INTEGER,
  sex          TEXT,
  history      TEXT,
  meds         TEXT
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE exam_days (
  exam_day_id  INTEGER PRIMARY KEY AUTOINCREMENT,
  exam_date    TEXT NOT NULL,
  exam_time    TEXT,
  exam_id      TEXT UNIQUE NOT NULL,
  patient_id   INTEGER NOT NULL, prep_location TEXT, day_code TEXT, status TEXT DEFAULT 'in_progress', last_seen_at TEXT,
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);
CREATE TABLE stool_conditions (
  condition_id INTEGER PRIMARY KEY AUTOINCREMENT,
  image_path   TEXT,
  label        TEXT NOT NULL
);
CREATE TABLE symptoms (
  symptom_id INTEGER PRIMARY KEY AUTOINCREMENT,
  symptom    TEXT NOT NULL UNIQUE
);
CREATE TABLE laxative_types (
  laxative_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "laxatives" (
  laxative_id       INTEGER PRIMARY KEY AUTOINCREMENT,
  exam_day_id       INTEGER NOT NULL,
  dose_no           INTEGER NOT NULL,
  taken_at          TEXT,
  laxative_type_id  INTEGER,   -- マスタ参照（推奨）
  drug_type         TEXT,      -- 移行中の互換用（後で消してもOK）
  FOREIGN KEY (exam_day_id) REFERENCES exam_days(exam_day_id),
  FOREIGN KEY (laxative_type_id) REFERENCES laxative_types(laxative_type_id)
);
CREATE TABLE IF NOT EXISTS "stool_records" (
  record_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  exam_day_id  INTEGER NOT NULL,
  recorded_at  TEXT NOT NULL,
  condition_id INTEGER NOT NULL,
  bm_no        INTEGER,
  FOREIGN KEY (exam_day_id) REFERENCES exam_days(exam_day_id),
  FOREIGN KEY (condition_id) REFERENCES stool_conditions(condition_id)
);
CREATE TABLE IF NOT EXISTS "symptom_records" (
  record_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  exam_day_id  INTEGER NOT NULL,
  recorded_at  TEXT NOT NULL,
  symptom_id   INTEGER NOT NULL,
  severity     INTEGER,
  note         TEXT,
  FOREIGN KEY (exam_day_id) REFERENCES exam_days(exam_day_id),
  FOREIGN KEY (symptom_id) REFERENCES symptoms(symptom_id)
);
CREATE UNIQUE INDEX idx_exam_days_exam_id ON exam_days(exam_id);

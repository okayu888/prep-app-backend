-- 便レベル（提示画像）
INSERT OR IGNORE INTO stool_conditions (image_path, label) VALUES
('static/stool/lv1.png','レベル1'),
('static/stool/lv2.png','レベル2'),
('static/stool/lv3.png','レベル3'),
('static/stool/lv4.png','レベル4'),
('static/stool/lv5.png','レベル5'),
('static/stool/lv6.png','レベル6');

-- 症状マスタ
INSERT OR IGNORE INTO symptoms (symptom) VALUES
('腹痛'),
('嘔気'),
('嘔吐');

-- 下剤マスタ
INSERT OR IGNORE INTO laxative_types (name) VALUES
('モビプレップ'),
('サルプレップ'),
('ピコプレップ'),
('ニフレック'),
('マグコロールP'),
('ビジクリア');


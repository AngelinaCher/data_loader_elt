-- Таблица хранения сырых данных о постах
CREATE TABLE IF NOT EXISTS stg.posts (
    stg_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    post_id INT NOT NULL,
    user_id INT NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    source TEXT NOT NULL,
    load_time TIMESTAMP DEFAULT NOW()
);
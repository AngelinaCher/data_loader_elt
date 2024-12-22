-- Таблица хранения сырых данных о постах
CREATE TABLE IF NOT EXISTS stg.posts (
    "stg_id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "userId" INT NOT NULL,
    "id" INT NOT NULL,
    "title" TEXT NOT NULL,
    "body" TEXT,
    "source" TEXT NOT NULL,
    "load_time" TIMESTAMP DEFAULT NOW()
);
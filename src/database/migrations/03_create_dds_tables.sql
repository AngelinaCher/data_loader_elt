-- Хаб для пользователей
CREATE TABLE IF NOT EXISTS dds.h_user (
    hub_user_hash_key VARCHAR(255) PRIMARY KEY,
    user_id BIGINT NOT NULL,
    record_source TEXT NOT NULL,
    load_date TIMESTAMP NOT NULL
);

-- Хаб для постов
CREATE TABLE IF NOT EXISTS dds.h_post (
    hub_post_hash_key VARCHAR(255) PRIMARY KEY,
    post_id BIGINT NOT NULL,
    record_source TEXT NOT NULL,
    load_date TIMESTAMP NOT NULL
);

-- Линк для постов и пользователей
CREATE TABLE IF NOT EXISTS dds.l_user_post (
    hub_user_hash_key VARCHAR(255) NOT NULL,
    hub_post_hash_key VARCHAR(255) NOT NULL,
    record_source TEXT NOT NULL,
    load_date TIMESTAMP NOT NULL,
    FOREIGN KEY (hub_user_hash_key) REFERENCES dds.h_user(hub_user_hash_key),
    FOREIGN KEY (hub_post_hash_key) REFERENCES dds.h_post(hub_post_hash_key)
);

-- Сателлит для пользователя
CREATE TABLE IF NOT EXISTS dds.s_user (
    hub_user_hash_key VARCHAR(255),
    user_id BIGINT NOT NULL,
    record_source TEXT NOT NULL,
    load_date TIMESTAMP NOT NULL,
    hash_diff VARCHAR(255),
    FOREIGN KEY (hub_user_hash_key) REFERENCES dds.h_user(hub_user_hash_key)
);

-- Сателлит для поста
CREATE TABLE IF NOT EXISTS dds.s_post (
    hub_post_hash_key VARCHAR(255),
    user_id BIGINT NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    record_source TEXT NOT NULL,
    load_date TIMESTAMP NOT NULL,
    hash_diff VARCHAR(255),
    FOREIGN KEY (hub_post_hash_key) REFERENCES dds.h_post(hub_post_hash_key)
);
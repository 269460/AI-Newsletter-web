CREATE DATABASE IF NOT EXISTS newsletter;
USE newsletter;

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS article (
    id INT AUTO_INCREMENT PRIMARY KEY,
    link VARCHAR(2083) UNIQUE,
    title VARCHAR(255),
    scrapy_text MEDIUMTEXT,
    source VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS summaries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    article_id INT,
    summary TEXT,
    FOREIGN KEY (article_id) REFERENCES article(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    preferences JSON,
    is_subscribed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    category_id INT,
    frequency ENUM('daily', 'weekly', 'monthly') DEFAULT 'weekly',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    UNIQUE KEY (user_id, category_id)
);

-- Dodanie indeksów dla poprawy wydajności
CREATE INDEX idx_article_link ON article(link);
CREATE INDEX idx_article_category ON article(category_id);
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_user_subscribed ON users(is_subscribed);
-- ===========================
-- Users Table
-- ===========================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firebase_uid VARCHAR(128) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255),
    bio TEXT,
    avatar_url TEXT,
    role ENUM('creator', 'admin', 'premium', 'regular') NOT NULL DEFAULT 'regular',
    status ENUM('active', 'suspended', 'deleted', 'banned') NOT NULL DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ===========================
-- Posts Table
-- ===========================
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    media_url TEXT,
    visibility ENUM('public', 'private', 'followers') DEFAULT 'public',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ===========================
-- Likes Table
-- ===========================
CREATE TABLE likes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_like (user_id, post_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);

-- ===========================
-- Follows Table
-- ===========================
CREATE TABLE follows (
    id INT AUTO_INCREMENT PRIMARY KEY,
    follower_id INT NOT NULL,
    following_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_follow (follower_id, following_id),
    FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ===========================
-- Comments Table
-- ===========================
CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);
-- ===========================
-- POST FLAGS / REPORTS TABLE
-- ===========================
CREATE TABLE post_flags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    reported_by INT NOT NULL,
    reason TEXT,
    reviewed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (reported_by) REFERENCES users(id) ON DELETE CASCADE
);
-- DROP TABLE IF EXISTS comments;
-- DROP TABLE IF EXISTS likes;
-- DROP TABLE IF EXISTS follows;
-- DROP TABLE IF EXISTS posts;
-- DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS post_flags;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS comment_likes;
DROP TABLE IF EXISTS reposts;

-- ===========================
-- COMMENT_LIKES TABLE
-- ===========================
CREATE TABLE comment_likes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    comment_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (comment_id) REFERENCES comments(id) ON DELETE CASCADE,
    UNIQUE KEY unique_comment_like (user_id, comment_id)
);

-- ===========================
-- NOTIFICATIONS TABLE
-- ===========================
CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recipient_id INT NOT NULL,        -- who receives it
    sender_id INT NOT NULL,           -- who triggered it
    type ENUM('like', 'comment', 'follow', 'share') NOT NULL,
    post_id INT NULL,                 -- optional: which post
    comment_id INT NULL,              -- optional: which comment
    message TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recipient_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (comment_id) REFERENCES comments(id) ON DELETE CASCADE
);

-- ===========================
-- REPOST TABLE
-- ===========================
-- ✅ REPOSTS TABLE
CREATE TABLE reposts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    original_post_id INT NOT NULL,
    quote TEXT NULL,
    is_quote BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (original_post_id) REFERENCES posts(id) ON DELETE CASCADE
);

-- ===========================
-- Add repost_id to comments and likes
-- ===========================
ALTER TABLE comments ADD COLUMN repost_id INT NULL;
ALTER TABLE likes ADD COLUMN repost_id INT NULL;

ALTER TABLE comments 
  ADD FOREIGN KEY (repost_id) REFERENCES reposts(id) ON DELETE CASCADE;

ALTER TABLE likes 
  ADD FOREIGN KEY (repost_id) REFERENCES reposts(id) ON DELETE CASCADE;

-- Active: 1750311500814@@localhost@3300@artbook
-- Users Table
CREATE DATABASE IF NOT EXISTS artbook;
USE artbook;

-- Users: firebase_uid is the PK (no numeric id)
CREATE TABLE IF NOT EXISTS users (
    firebase_uid VARCHAR(128) PRIMARY KEY,
    email        VARCHAR(255) NOT NULL UNIQUE,
    display_name VARCHAR(255) NOT NULL,
    bio          TEXT NULL,
    avatar_url   TEXT NULL,
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_admin     BOOLEAN NOT NULL DEFAULT FALSE,
    is_creator   BOOLEAN NOT NULL DEFAULT FALSE
);

-- Posts Table
CREATE TABLE IF NOT EXISTS posts (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    user_id    VARCHAR(128) NOT NULL,
    caption    TEXT,
    image_url  TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_posts_user
      FOREIGN KEY (user_id) REFERENCES users(firebase_uid) ON DELETE CASCADE
);

-- Comments Table
CREATE TABLE IF NOT EXISTS comments (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    post_id    INT NOT NULL,
    user_id    VARCHAR(128) NOT NULL,
    content    TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_comments_post
      FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    CONSTRAINT fk_comments_user
      FOREIGN KEY (user_id) REFERENCES users(firebase_uid) ON DELETE CASCADE
);

-- Likes Table
CREATE TABLE IF NOT EXISTS likes (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    post_id    INT NOT NULL,
    user_id    VARCHAR(128) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY user_post_unique (user_id, post_id),
    CONSTRAINT fk_likes_post
      FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    CONSTRAINT fk_likes_user
      FOREIGN KEY (user_id) REFERENCES users(firebase_uid) ON DELETE CASCADE
);

-- Followers Table
CREATE TABLE IF NOT EXISTS followers (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    follower_id   VARCHAR(128) NOT NULL,
    following_id  VARCHAR(128) NOT NULL,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY follow_unique (follower_id, following_id),
    CONSTRAINT fk_followers_follower
      FOREIGN KEY (follower_id)  REFERENCES users(firebase_uid) ON DELETE CASCADE,
    CONSTRAINT fk_followers_following
      FOREIGN KEY (following_id) REFERENCES users(firebase_uid) ON DELETE CASCADE
);

-- Backfill display_name if missing (uses UID prefix)
UPDATE users
SET display_name = CONCAT('user_', LEFT(firebase_uid, 8))
WHERE display_name IS NULL OR display_name = '';


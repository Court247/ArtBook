-- ===========================
-- Users table
-- ===========================
CREATE TABLE users (
    firebase_uid VARCHAR(128) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255),
    bio TEXT DEFAULT '',
    avatar_url TEXT DEFAULT '',
    role ENUM('creator', 'admin', 'premium', 'regular') NOT NULL DEFAULT 'regular',
    status ENUM('active', 'suspended', 'deleted', 'banned') NOT NULL DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ✅ Posts Table
CREATE TABLE posts (
    id CHAR(36) PRIMARY KEY,
    user_id VARCHAR(128) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(firebase_uid) ON DELETE CASCADE
);

-- ✅ Likes Table
CREATE TABLE likes (
    id CHAR(36) PRIMARY KEY,
    user_id VARCHAR(128) NOT NULL,
    post_id CHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(firebase_uid) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);

-- ✅ Follows Table
CREATE TABLE follows (
    id CHAR(36) PRIMARY KEY,
    follower_id VARCHAR(128) NOT NULL,
    following_id VARCHAR(128) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (follower_id) REFERENCES users(firebase_uid) ON DELETE CASCADE,
    FOREIGN KEY (following_id) REFERENCES users(firebase_uid) ON DELETE CASCADE
);

-- ✅ Comments Table
CREATE TABLE comments (
    id CHAR(36) PRIMARY KEY,
    user_id VARCHAR(128) NOT NULL,
    post_id CHAR(36) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(firebase_uid) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);


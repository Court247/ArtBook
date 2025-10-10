# 🌐 ArtBook (Monorepo) ![version](https://img.shields.io/badge/version-1.0.9-blue)


A full-stack, cross-platform social media application built with:

- 🚀 **FastAPI** for the backend API
- 💻 **React** for the web frontend
- 📱 **Flutter** for the mobile app
- 🔐 **Firebase Auth** for secure authentication
- ☁️ **Firebase Storage** for user media uploads
- 🗃️ **MySQL** for relational data storage

This project is built and maintained as a **monorepo** for easier management and consistent development across platforms.

📑 Table of Contents

1. ⚡ [Quickstart](#-quickstart)
2. 🔑 [Environment Variables](#-environment-variables)
3. 📁 [Project Structure](#-project-structure)
4. 📂 [Folder Breakdown](#-folder-breakdown)
    - [routers/](#-routers--api-route-logic)
    - [models/](#models--sqlalchemy-database-models)
    - [schemas/](#-schemas--pydantic-schemas)
    - [utils/](#-utils--utility-functions)
5. 🧰 [Tech Stack](#-tech-stack)
6. 🔐 [Authentication](#-authentication)
7. 📸 [Media Uploads](#-media-uploads)
8. 📊 [Database Schema (MySQL)](#-database-schema-mysql)
9. 🌍 [API Endpoints (FastAPI)](#-api-endpoints-fastapi)
    - [Users](#-users)
    - [Home/Feed](#-home--feed)
    - [Follow](#-follow)
    - [Comments](#-comments)
    - [Likes](#likes)
    - [Posts](#-posts)
    - [Admin](#️-admin)
10. 🧪 [Testing](#)
11. ✅ [License](#-license)
12. ✍️ [Author](#author)

## ⚡ Quickstart

### 📁 Clone the repo

```bash
git clone https://github.com/yourname/ArtBook.git
cd ArtBook
```
### ✅ Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate # Linux
.\env\Scripts\activate   # Windows

# You only need to do this once, the first time you initialize the environment. 
pip install -r requirements.txt 

uvicorn main:app --reload
```
→ Visit [FastAPI](http://localhost:8000/docs)

### ✅ Web (React)
```bash
cd web
npm install
npm start

```
→ Visit [Web](http://localhost:3000)
### ✅ Mobile (Flutter)
```bash
cd mobile
flutter pub get
flutter run
```
## 🔑 Environment Variables

Since all services use the same .env file. These are just place hold references. All of this will be found in the `backend` folder. 

| Variable             | Description                          | Example                                           |
| -------------------- | ------------------------------------ | ------------------------------------------------- |
| `DATABASE_URL`       | MySQL connection string              | `mysql://user:pass@localhost/artbook`             |
| `FIREBASE_CRED_PATH` | Path to Firebase Admin SDK JSON file | `./firebase-adminsdk.json`                        |
| `REACT_APP_API_URL`  | API base URL for React app           | `http://localhost:8000`                           |
| `FLUTTER_API_URL`    | API base URL for Flutter app         | `http://10.0.2.2:8000` (Android emulator default) |

## 📁 Project Structure
```bash
ArtBook/
├── backend/                         # FastAPI backend
│   ├── main.py
│   ├── requirements.txt
│   ├── VERSION
│   ├── .env
│   ├── artbook-20329-firebase-adminsdk-fbsvc-ddbc5c06ca.json  # (ignored)
│   ├── db/
│   │   └── schema.sql
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   └── utils/
├── web/                             # React Web Frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── firebase.js
│   │   └── App.js
│   ├── .env
│   └── package.json
├── mobile/                          # Flutter Mobile App
│   ├── lib/
│   │   └── firebase_options.dart
│   ├── android/
│   │   └── app/
│   │       └── google-services.json 
│   ├── ios/
│   │   └── Runner/
│   │       └── GoogleService-Info.plist # Currently Android support only.
│   ├── pubspec.yaml
│   ├── .env  
│   └── analysis_options.yaml
├── README.md
├── CHANGELOG.md
└── .gitignore

```
---
## 📂 Folder Breakdown

###  📂models/ — SQLAlchemy Database Models
These define your MySQL table structure in Python using SQLAlchemy ORM.

| File         | Purpose                                                                                       |
| ------------ | --------------------------------------------------------------------------------------------- |
| `user.py`    | Defines the `User` table — stores Firebase UID, email, profile data like avatar and bio.      |
| `post.py`    | Defines the `Post` table — includes caption, image URL, user ID, and timestamp.               |
| `comment.py` | Defines the `Comment` table — stores user comments linked to a post.                          |
| `like.py`    | Defines the `Like` table — tracks which user liked which post (enforces uniqueness per pair). |

---

### 📂 routers/ — API Route Logic

This folder holds all the FastAPI route definitions for each feature (users, posts, etc.). Each file maps to a logical feature in the app.

| File          | Purpose                                                                                                 |
| ------------- | ------------------------------------------------------------------------------------------------------- |
| `users.py`    | Handles user endpoints: getting the current user, updating profile info, and Firebase token validation. |
| `posts.py`    | Handles creation, deletion, and retrieval of posts. Posts include captions and image URLs.              |
| `comments.py` | Adds and retrieves comments for specific posts.                                                         |
| `likes.py`    | Lets users like or unlike a post, and returns the like count for a post.                                |
| `admin.py`    | Dashboard for admin functions                                |

---


### 📂 schemas/ — Pydantic Schemas
These define input and output shapes for API endpoints. They validate incoming request bodies and control what fields are returned in responses. Each schema works alongside its corresponding model and router to ensure data is clean and consistent across the API.

| File         | Purpose                                                                        |
| ------------ | ------------------------------------------------------------------------------ |
| `user.py`    | Models user creation, update, and response formats.                            |
| `post.py`    | Models the creation of posts and what data should be returned to the frontend. |
| `comment.py` | Models comment creation and response formatting.                               |
| `like.py`    | Controls response structure when liking a post or retrieving like info.        |


---
### 📂 utils/ — Utility Functions
This folder contains reusable backend utilities that support your main API logic. Use these to keep your main routers/ and main.py files clean and maintainable.


| File               | Purpose                                                                                   |
| ------------------ | ----------------------------------------------------------------------------------------- |
| `firebase_auth.py` | Initializes Firebase Admin SDK and verifies user ID tokens. Required for authentication.  |
| `image_upload.py`  | Uploads image files to Firebase Storage and returns public download URLs (used in posts). |

---

### 🗄️ db/ — Database Connection Layer

| File          | Purpose                                                                                                                    |
| ------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `database.py` | Creates and manages the SQLAlchemy `engine`, session, and `Base` model class. Used throughout the app to connect to MySQL. |

---
## 🧰 Tech Stack

| Layer           | Technology            |
|----------------|------------------------|
| 🧠 Backend      | FastAPI (Python)       |
| 🧮 Database     | MySQL                  |
| 🧑‍💻 Web App      | React (JS)             |
| 📱 Mobile App   | Flutter (Dart)         |
| 🔐 Auth         | Firebase Auth          |
| 🖼️ Media        | Firebase Storage       |
| 📦 API Type     | REST                   |

---

## 🔐 Authentication

- Authentication is handled through **Firebase Auth**. 
- User token is sent with API request. 
- Backend verifies tokens with Firebase Admin SDK before granting access.
---

## 📸 Media Uploads
- Clients upload media to Firebase Storage.
- Download URLs are sent to backend with post metadata.

---

## 📊 Database Schema (MySQL)

This project uses a relational schema:

```
`users
 ├── id (PK, AUTO_INCREMENT)
 ├── firebase_uid (UNIQUE)
 ├── email (UNIQUE)
 ├── display_name
 ├── bio
 ├── avatar_url
 ├── role ENUM('creator', 'admin', 'premium', 'regular') DEFAULT 'regular'
 ├── status ENUM('active', 'suspended', 'deleted', 'banned') DEFAULT 'active'
 └── created_at DATETIME DEFAULT CURRENT_TIMESTAMP


posts
 ├── id (PK, AUTO_INCREMENT)
 ├── user_id → users.id
 ├── content
 ├── media_url
 ├── visibility ENUM('public', 'private', 'followers') DEFAULT 'public'
 └── created_at DATETIME DEFAULT CURRENT_TIMESTAMP


comments
 ├── id (PK, AUTO_INCREMENT)
 ├── post_id → posts.id
 ├── user_id → users.id
 ├── content
 └── created_at DATETIME DEFAULT CURRENT_TIMESTAMP


likes
 ├── id (PK, AUTO_INCREMENT)
 ├── post_id → posts.id
 ├── user_id → users.id
 ├── created_at DATETIME DEFAULT CURRENT_TIMESTAMP
 └── UNIQUE (user_id, post_id)


follows
 ├── id (PK, AUTO_INCREMENT)
 ├── follower_id → users.id
 ├── following_id → users.id
 ├── created_at DATETIME DEFAULT CURRENT_TIMESTAMP
 └── UNIQUE (follower_id, following_id)


post_flags
 ├── id (PK, AUTO_INCREMENT)
 ├── post_id → posts.id
 ├── reported_by → users.id
 ├── reason
 ├── reviewed BOOLEAN DEFAULT FALSE
 └── created_at DATETIME DEFAULT CURRENT_TIMESTAMP
```

See `/backend/db/schema.sql` for full schema.

---

## 🌍 API Endpoints (FastAPI)

The live API OpenAPI/Swagger UI is available at: http://localhost:8000/docs#/

Use the interactive docs to explore request/response shapes, try endpoints, and view authentication requirements. These are subject to be updated depend on the changing information. 

### 👥 Users
| Method | Endpoint                          | Description |
| ------ | --------------------------------- | ----------- |
| GET    | /users/me                         | Get current authenticated user's profile |
| POST   | /users/                            | Create a user record (server reads Firebase UID from token) |
| PUT    | /users/{firebase_uid}                               | Update user |

### 🏠 Home / Feed

| Method | Endpoint          | Description                                                                               |
| ------ | ----------------- | ----------------------------------------------------------------------------------------- |
| GET    | /home/feed  | Posts from people the user follows + their own posts.       |
| GET    | /home/trending    | Get trending posts (based on likes, comments, flags, or algorithm) Limit 20     |
| GET    | /home/recommended | Get recommended users or posts (simple logic: mutual follows, popular users, etc.)        |
| GET    | /home/activity    | Get recent activity (likes, follows, comments on user’s posts)                            |
| GET    | /home/stats       | Get quick stats (post count, followers, following, likes received) for the logged-in user |

### 😎 Follow
| Method | Endpoint          | Description                                                                               |
| ------ | ----------------- | ----------------------------------------------------------------------------------------- |
| POST    | /follow/        | Posts from people the user follows + their own posts.       |
| DELETE    | /follow/{user_id}    | unfollow    |
| GET    | /follow/following/{user_id} | see who a user follows     |
| GET    | /follow/follower/{user_id}    | see who follows them

###  💬 Comments
| Method | Endpoint          | Description                                                                               |
| ------ | ----------------- | ----------------------------------------------------------------------------------------- |
| POST    | /comments/        | create a new comment on a post.      |
| DELETE    |/comments/{comment_id} | delete a comment (only the author or admin/creator can).   |
| GET    | /comments/post/{post_id} | list all comments for a given post.   |


### 👍Likes
| Method | Endpoint          | Description                                                                               |
| ------ | ----------------- | ----------------------------------------------------------------------------------------- |
| POST    | /likes/posts/{post_id}        | Like or unlike a post  |
| GET    | /likes/post/{post_id}/count | Shows total like count |

### 📝 Posts
| Method | Endpoint               | Description |
| ------ | ---------------------- | ----------- |
| POST   | /posts/create          | Create a post (caption + image URL) |
| GET    | /posts/feed            | Get feed (recent posts from followed users) |
| GET   | /posts/user/{user_id}       | Get user's posts |
| DELETE  | /posts/{post_id}   | Users can delete their posts. |
| POST   | /posts/{post_id}/flag       | Flag a post for admin review |

### 🛡️ Admin
| Method | Endpoint                 | Description |
| ------ | ------------------------ | ----------- |
| GET    | /admin/dashboard         | Test admin access |
| GET    | /admin/users             | Get all registered users |
| DELETE | /admin/users/{firebase_id}   | Delete a user |
| POST | /admin/promote-user/{firebase_id}   | Promote or Demote users |
| GET    | /admin/posts             | Get all posts (to be implemented) |
| GET    | /admin/flagged-posts     | Get flagged posts (to be implemented) |
| DELETE | /admin/posts/{post_id}   | Delete a post (to be implemented)|

Notes:
- Open http://localhost:8000/docs#/ to use the interactive docs and see required auth headers and request schemas.
- The backend verifies Firebase ID tokens; include `Authorization: Bearer <id_token>` where required.

## ✅ License

All rights reserved. Closed source, not for redistribution. You may not use, copy, distribute, or modify any part of this code without express written permission from the author. See [LICENSE.txt](./LICENSE.txt) for full terms.

# Author

Courtney Woods
email: courtney.woodsjobs@gmail.com

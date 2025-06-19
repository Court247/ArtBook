# 🌐 ArtBook (Monorepo) ![version](https://img.shields.io/badge/version-1.0.1-blue)


A full-stack, cross-platform social media application built with:

- 🚀 **FastAPI** for the backend API
- 💻 **React** for the web frontend
- 📱 **Flutter** for the mobile app
- 🔐 **Firebase Auth** for secure authentication
- ☁️ **Firebase Storage** for user media uploads
- 🗃️ **MySQL** for relational data storage

This project is built and maintained as a **monorepo** for easier management and consistent development across platforms.

---

## 📁 Project Structure
```bash
ArtBook/
├── backend/                       # FastAPI backend
│   ├── main.py
│   ├── requirements.txt
│   ├── routers/
│   │   ├── users.py
│   │   ├── posts.py
│   │   ├── comments.py
│   │   ├── likes.py
│   │   └── followers.py
│   ├── models/
│   │   ├── user.py
│   │   ├── post.py
│   │   └── ...
│   ├── schemas/
│   │   ├── user.py
│   │   ├── post.py
│   │   └── ...
│   ├── db/
│   │   └── database.py
│   └── utils/
│       ├── firebase_auth.py
│       └── image_upload.py
├── web/                           # React Web Frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── api/
│   │   └── firebase.js
│   ├── public/
│   ├── .env
│   └── package.json
├── mobile/                        # Flutter Mobile App
│   ├── lib/
│   │   ├── screens/
│   │   ├── services/
│   │   └── firebase_options.dart
│   ├── android/
│   ├── ios/
│   └── pubspec.yaml
├── shared/                        # Shared schemas/docs
│   ├── openapi.json
│   └── mock_data.json
├── README.md
└── .gitignore
```
---
## 📂 Folder Breakdown

### 📂 routers/ — API Route Logic

This folder holds all the FastAPI route definitions for each feature (users, posts, etc.). Each file maps to a logical feature in the app.

| File          | Purpose                                                                                                 |
| ------------- | ------------------------------------------------------------------------------------------------------- |
| `users.py`    | Handles user endpoints: getting the current user, updating profile info, and Firebase token validation. |
| `posts.py`    | Handles creation, deletion, and retrieval of posts. Posts include captions and image URLs.              |
| `comments.py` | Adds and retrieves comments for specific posts.                                                         |
| `likes.py`    | Lets users like or unlike a post, and returns the like count for a post.                                |

---

###  📂models/ — SQLAlchemy Database Models
These define your MySQL table structure in Python using SQLAlchemy ORM.

| File         | Purpose                                                                                       |
| ------------ | --------------------------------------------------------------------------------------------- |
| `user.py`    | Defines the `User` table — stores Firebase UID, email, profile data like avatar and bio.      |
| `post.py`    | Defines the `Post` table — includes caption, image URL, user ID, and timestamp.               |
| `comment.py` | Defines the `Comment` table — stores user comments linked to a post.                          |
| `like.py`    | Defines the `Like` table — tracks which user liked which post (enforces uniqueness per pair). |

---

### 📂 schemas/ — Pydantic Schemas
These define input and output shapes for API endpoints. They validate incoming request bodies and control what fields are returned in responses.

| File         | Purpose                                                                        |
| ------------ | ------------------------------------------------------------------------------ |
| `user.py`    | Models user creation, update, and response formats.                            |
| `post.py`    | Models the creation of posts and what data should be returned to the frontend. |
| `comment.py` | Models comment creation and response formatting.                               |
| `like.py`    | Controls response structure when liking a post or retrieving like info.        |

Each schema works alongside its corresponding model and router to ensure data is clean and consistent across the API.
---
### 📂 utils/ — Utility Functions
This folder contains reusable backend utilities that support your main API logic.

| File               | Purpose                                                                                   |
| ------------------ | ----------------------------------------------------------------------------------------- |
| `firebase_auth.py` | Initializes Firebase Admin SDK and verifies user ID tokens. Required for authentication.  |
| `image_upload.py`  | Uploads image files to Firebase Storage and returns public download URLs (used in posts). |

Use these to keep your main routers/ and main.py files clean and maintainable.
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
| 🧑‍💻 Web App     | React (JS)             |
| 📱 Mobile App   | Flutter (Dart)         |
| 🔐 Auth         | Firebase Auth          |
| 🖼️ Media        | Firebase Storage       |
| 📦 API Type     | REST                   |

---

## 🔐 Authentication

Authentication is handled through **Firebase Auth**. All frontend apps use Firebase SDKs to get a user token, which is verified on the backend for secure access to protected routes.

---

## 📸 Media Uploads

Both mobile and web clients upload images to **Firebase Storage**. The download URL is sent to the backend, which stores it along with post metadata.

---

## 📊 Database Schema (MySQL)

This project uses a relational schema:

- `users`: Auth metadata, profile info
- `posts`: Captions, image URLs
- `likes`: User ↔ post interactions
- `comments`: Replies on posts
- `followers`: User ↔ user follows

See `/backend/db/schema.sql` (coming soon) for full schema.

---

## 📦 Running Locally

### ✅ Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate # Linux
.\env\Scripts\activate   # Windows
pip install -r requirements.txt 
cp .env.example .env

# Set DATABASE_URL and Firebase path in .env
uvicorn main:app --reload

```
### ✅ Web (React)
```bash
cd web
npm install
npm start

```
### ✅ Mobile (Flutter)
```bash
cd mobile
flutter pub get
flutter run
```
## 🌍 API Endpoints (FastAPI)

```bash
| Method | Endpoint               | Description                  |
| ------ | ---------------------- | ---------------------------- |
| POST   | `/auth/verify-token`   | Verifies Firebase ID token   |
| GET    | `/users/me`            | Get logged-in user info      |
| POST   | `/posts/create`        | Create new post with caption |
| GET    | `/posts/feed`          | Get user feed                |
| POST   | `/posts/{id}/like`     | Like/unlike a post           |
| POST   | `/posts/{id}/comments` | Comment on a post            |
| POST   | `/follow/{user_id}`    | Follow or unfollow a user    |

```
## ✅ License

All rights reserved. You may not use, copy, distribute, or modify any part of this code without express written permission from the author. See [LICENSE.txt](./LICENSE.txt) for full terms.

# Author

Courtney Woods
email: courtney.woodsjobs@gmail.com

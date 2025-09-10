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
├── backend/                         # FastAPI backend
│   ├── main.py
│   ├── requirements.txt
│   ├── VERSION
│   ├── .env
│   ├── artbook-20329-firebase-adminsdk-fbsvc-ddbc5c06ca.json  # (ignored)
│   ├── db/
│   │   └── schema.sql
│   ├── models/
│   │   ├── comment.py
│   │   ├── like.py
│   │   ├── post.py
│   │   └── users.py
│   ├── routers/
│   │   ├── admin.py
│   │   ├── comment.py
│   │   ├── like.py
│   │   ├── post.py
│   │   └── users.py
│   ├── schemas/
│   │   ├── comment.py
│   │   ├── like.py
│   │   ├── post.py
│   │   └── user.py
│   └── utils/
│       ├── firebase_auth.py
│       └── image_upload.py
├── web/                           # React Web Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── PrivateRoute.jsx
│   │   │   └── Spinner.jsx
│   │   ├── pages/
│   │   │   ├── CreateAccount.jsx
│   │   │   ├── HomePage.jsx
│   │   │   └── LoginPage.jsx
│   │   ├── firebase.js
│   │   └── App.js
│   ├── .env
│   └── package.json
├── mobile/                        # Flutter Mobile App
│   ├── lib/
│   │   └── firebase_options.dart
│   ├── android/
│   │   └── app/
│   │       └── google-services.json 
│   ├── ios/
│   │   └── Runner/
│   │       └── GoogleService-Info.plist 
│   ├── pubspec.yaml
│   ├── .env  
│   └── analysis_options.yaml
├── README.md
├── CHANGELOG.md
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

See `/backend/db/schema.sql` for full schema.

---

## 📦 Running Locally

### ✅ Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate # Linux
.\env\Scripts\activate   # Windows
pip install -r requirements.txt 

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

### 🔐 Auth + User Endpoints

| Method | Endpoint             | Description                |
| ------ | -------------------- | -------------------------- |
| POST   | `/auth/verify-token` | Verifies Firebase ID token |
| GET    | `/users/me`          | Get logged-in user profile |

###📝 Post Endpoints

| Method | Endpoint               | Description                                 |
| ------ | ---------------------- | ------------------------------------------- |
| POST   | `/posts/create`        | Create a new post (caption + image)         |
| GET    | `/posts/feed`          | Get feed (recent posts from followed users) |
| POST   | `/posts/{id}/like`     | Like or unlike a post                       |
| POST   | `/posts/{id}/comments` | Add a comment to a post                     |
| POST   | `/posts/{id}/flag`     | Flag a post for admin review                |

###👥 Social (Follow) Endpoints

| Method | Endpoint            | Description               |
| ------ | ------------------- | ------------------------- |
| POST   | `/follow/{user_id}` | Follow or unfollow a user |

###🛡️ Admin Endpoints (Firebase Admins Only)

| Method | Endpoint                 | Description              |
| ------ | ------------------------ | ------------------------ |
| GET    | `/admin/dashboard`       | Test admin access        |
| GET    | `/admin/users`           | Get all registered users |
| DELETE | `/admin/users/{user_id}` | Delete a user            |
| GET    | `/admin/posts`           | Get all posts            |
| GET    | `/admin/flagged-posts`   | Get all flagged posts    |
| DELETE | `/admin/posts/{post_id}` | Delete a post            |

## ✅ License

All rights reserved. You may not use, copy, distribute, or modify any part of this code without express written permission from the author. See [LICENSE.txt](./LICENSE.txt) for full terms.

# Author

Courtney Woods
email: courtney.woodsjobs@gmail.com

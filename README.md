# 🌐 ArtBook (Monorepo) ![version](https://img.shields.io/badge/version-1.0.5-blue)


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

    - [Auth + Users](#-auth--user-endpoints)

    - [Posts](#)

    - [Social](#)

    - [Admin](#)

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

- `users`: Auth metadata, profile info
- `posts`: Captions, image URLs
- `likes`: User ↔ post interactions
- `comments`: Replies on posts
- `followers`: User ↔ user follows

See `/backend/db/schema.sql` for full schema.

---

## 🌍 API Endpoints (FastAPI)

The live API OpenAPI/Swagger UI is available at: http://localhost:8000/docs#/

Use the interactive docs to explore request/response shapes, try endpoints, and view authentication requirements.

### 🔐 Auth
| Method | Endpoint               | Description                          |
| ------ | ---------------------- | ------------------------------------ |
| POST   | /auth/verify-token     | Verify Firebase ID token and return token payload |

### 👥 Users
| Method | Endpoint                          | Description |
| ------ | --------------------------------- | ----------- |
| GET    | /users/me                         | Get current authenticated user's profile |
| POST   | /users                            | Create a user record (server reads Firebase UID from token) |
| PUT    | /me                               | Update own profile (only safe fields allowed) |
| PUT    | /users/{user_id}                  | Admin/creator update of a user (creators can edit roles; admins limited) |
| PUT    | /users/{user_id}/roles            | Creator-only: set is_admin / is_creator flags |

### 📝 Posts
| Method | Endpoint               | Description |
| ------ | ---------------------- | ----------- |
| POST   | /posts/create          | Create a post (caption + image URL) |
| GET    | /posts/feed            | Get feed (recent posts from followed users) |
| POST   | /posts/{id}/like       | Like or unlike a post |
| POST   | /posts/{id}/comments   | Add a comment to a post |
| POST   | /posts/{id}/flag       | Flag a post for admin review |

### 👥 Social (Follow)
| Method | Endpoint            | Description |
| ------ | ------------------- | ----------- |
| POST   | /follow/{user_id}   | Follow or unfollow a user |

### 🛡️ Admin
| Method | Endpoint                 | Description |
| ------ | ------------------------ | ----------- |
| GET    | /admin/dashboard         | Test admin access |
| GET    | /admin/users             | Get all registered users |
| DELETE | /admin/users/{user_id}   | Delete a user |
| GET    | /admin/posts             | Get all posts |
| GET    | /admin/flagged-posts     | Get flagged posts |
| DELETE | /admin/posts/{post_id}   | Delete a post |

Notes:
- Open http://localhost:8000/docs#/ to use the interactive docs and see required auth headers and request schemas.
- The backend verifies Firebase ID tokens; include Authorization: Bearer <id_token> where required.
- For role management, the DB is the source of truth — use the creator-only roles endpoint to change is_admin/is_creator flags so the database and Firebase claims stay consistent.
## ✅ License

All rights reserved. Closed source, not for redistribution. You may not use, copy, distribute, or modify any part of this code without express written permission from the author. See [LICENSE.txt](./LICENSE.txt) for full terms.

# Author

Courtney Woods
email: courtney.woodsjobs@gmail.com

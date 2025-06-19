# 🌐 ArtBook (Monorepo)

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
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
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

All rights reserved. You may not use, copy, distribute, or modify any part of this code without express written permission from the author. See LICENSE.txt for full terms.

# Author

Courtney Woods
email: courtney.woodsjobs@gmail.com

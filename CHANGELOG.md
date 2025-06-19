# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2025-06-19
### Changed
- Updated Android app build configuration to use Java 17 for compatibility with newer Java versions (`mobile/android/app/build.gradle.kts`).
- Added and updated `.gitignore` entries to ensure all sensitive Firebase config and service account files are ignored, including:
  - `mobile/lib/firebase_options.dart`
  - `mobile/ios/Runner/GoogleService-Info.plist`
  - `mobile/android/app/google-services.json`
  - `backend/artbook-20329-firebase-adminsdk-fbsvc-ddbc5c06ca.json`
  - `.env` files in relevant directories
- Added `backend/VERSION` file to track backend version.
- Created `CHANGELOG.md` to document project changes.
- Created `web/.env` for React environment variables.
- Added new backend files:
  - `backend/models/`
        - `comment.py`
        - `like.py`
        - `post.py`
  - `backend/routers/` (list specific files if known)
        - `comment.py`
        - `like.py`
        - `post.py`
        - `admin.py`
  - `backend/schemas/` (list specific files if known)
        - `comment.py`
        - `like.py`
        - `post.py`
- Changed files:
  - `.gitignore` (updated to ignore new sensitive files)
  - `mobile/android/app/build.gradle.kts` (updated Java version)
  - `CHANGELOG.md` (created and updated)
  - `backend/models/users.py`
  - `db/schema.sql`
- Successfully completed set up for ArtBook FastAPI backend
---

## [1.0.0] - 2025-06-19
### Added
- Initial versioning for monorepo structure (web, backend, mobile)
- Environment variable support for React frontend (`web/.env`)
- Environment variable and secret management guidance for backend and mobile
- `.gitignore` rules for sensitive files (Firebase keys, config, etc.)
- FastAPI backend with user router and CORS setup
- React frontend with Firebase integration
- Flutter mobile app with Firebase integration

### Security
- Added `.gitignore` entries to protect all sensitive Firebase and service account files
- Documented how to generate and store `firebase-service-account.json` securely

---

> Changelog format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
> Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

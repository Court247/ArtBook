# Changelog

All notable changes to this project will be documented in this file.

## [1.0.3] - 2025-06-20
### Added
- Created `web/src/pages/Register.jsx` for user registration page.

### Changed
- Ensured consistent casing for `LoginPage.jsx` across all imports and file names in the React frontend.
- Cleaned up old references to `Loginpage.jsx` (lowercase "p") to prevent import errors.
- Updated project structure documentation in `README.md` for clarity and accuracy.
- Changed Firebase configuration setup instructions in `README.md` to use environment variables for added security.
- Updated backend dependency versions in `backend/requirements.txt` to latest compatible versions.
- Changed database initialization script to handle existing data more gracefully during development setup.
- Updated `routers/comment.py`

### Removed
- removed `web/src/pages/CreateAccount.jsx`
---

## [1.0.2] - 2025-06-19
### Changed
- Updated Android app build configuration to use Java 17 for compatibility with newer Java versions (`mobile/android/app/build.gradle.kts`).
- Added and updated `.gitignore` entries to ensure all sensitive Firebase config and service account files are ignored, including:
  - `mobile/lib/firebase_options.dart`
  - `mobile/ios/Runner/GoogleService-Info.plist`
  - `mobile/android/app/google-services.json`
  - `backend/artbook-20329-firebase-adminsdk-fbsvc-ddbc5c06ca.json`
  - `.env` files in relevant directories
- Created `CHANGELOG.md` to document project changes.
- Changed files:
  - `.gitignore` (updated to ignore new sensitive files)
  - `mobile/android/app/build.gradle.kts` (updated Java version)
  - `CHANGELOG.md` (created and updated)
  - `backend/models/users.py`
  - `db/schema.sql`
  - `README.md` 
- Successfully completed set up for ArtBook FastAPI backend
- Set up the web environment. 

### Added
- Added `backend/VERSION` file to track backend version.
- Created `web/.env` for React environment variables.
- Added new backend files:
  - `backend/models/`
        - `comment.py`
        - `like.py`
        - `post.py`
  - `backend/routers/` 
        - `comment.py`
        - `like.py`
        - `post.py`
        - `admin.py`
  - `backend/schemas/` 
        - `comment.py`
        - `like.py`
        - `post.py`
- Added new web files:
  - `components/`
    - `PrivateRoute.jsx`
    - `Spinner.jsx`
  - `pages/`
    - `CreateAccount.jsx`
    - `HomePage.jsx`
    - `LoginPage.jsx`


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

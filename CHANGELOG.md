# Changelog

All notable changes to this project will be documented in this file.

## [1.0.6] - 2025-09-25

### Added
 - Added in `Register.jsx` in pages
    - Added inline `API_URL` resolution using Vite env (`import.meta.env.VITE_API_URL` with localhost fallback).
    - Added Firebase email/password registration flow (`createUserWithEmailAndPassword`), token retrieval (`getIdToken`), and localStorage persistence.
    - Added POST `/users` call sending `display_name` and `email` with `Authorization: Bearer <token>` header.
    - Frontend `Register.jsx` now sends Firebase ID token in the `Authorization` header to authenticate backend requests.
 - Added in `firebase.js` in src
    - Added Vite-based Firebase config keys (`import.meta.env.VITE_FIREBASE_*`).
  - Added dependancy
    - `axios`
    - `email validator`
  - Added handling of environment variable `VITE_API_URL` to dynamically target backend.
  - Registration flow extended: after creating Firebase user, frontend also creates a corresponding entry in the MySQL DB via FastAPI `/users/`.
  - Support for optional fields (`bio`, `avatar_url`) in user creation request.
  - Added in `user.py` in `schema`
    - Added `uid` parameter so that the UID of user gets added to the mysql database. 
  - Added new users table with correct parameters in ArtBook database.
  - Added in `firebase_auth` in `utils`
    - Added "`creator`" claim support for your creator-only endpoints.

### Changed
  - Migrated frontend environment variable strategy from CRA (`REACT_APP_*`) to Vite (`VITE_*`), affecting `Register.jsx` and `firebase.js`
  - Normalized API base URL handling to trim trailing slashes and use fallback `http://localhost:8000` when `VITE_API_URL` is unset.  
  - Changed `Register.jsx`
    - Improved error handling in `Register.jsx`: now throws with status + response text if account creation fails.
    - Updated `Register.jsx` to navigate to `/home` after successful registration.
    - Made bio in schema optional
    - `Register.jsx` updated to call correct endpoint `(/users/)` instead of incorrect `/users` or `/users/users`.
 - Changed in `firebase.js`
    - Ensured `firebase.js` reads only the necessary Vite-prefixed keys (removed legacy `REACT_APP_` usage).
  - Changed in `user.py` in `schemas`
    - `bio` field in `UserCreate` schema changed from required → optional (Optional[str] = None).
    - `UserResponse.id` is a string (Firebase UID) instead of `int`.
    - `orm_mode = True` so SQLAlchemy models map cleanly to Pydantic responses.
  - Changed in `users.py` in `routers`
    - Router definitions in `routers/users.py` updated to use `@router.post("/")` instead of `@router.post("/users")`.
    - Cleaned up FastAPI routes to avoid double prefixes like `/users/users`.
    - Pulled `firebase_uid` straight from `get_token_payload` (verified Firebase token).
    - `/users/` now always binds the Firebase UID to the DB user.
    - Prevents UID spoofing.
    - Always uses `firebase_uid` from token.
    - `uid` removed from schema expectations.
  - Changed in `admin.py` in `routers`
    - `require_admin` protects admin endpoints.
    - `require_creator` ensures only the creator can promote/demote users.
    - All queries use `firebase_uid` (string PK) consistently.
  - Changed in `users.py` in `models/`
    - `firebase_uid` is the primary key (`String(128)`), no auto-increment `id`.
    - Columns match `schemas/user.py` and what you insert in `routers/users.py`.
    - Email is `unique=True` to prevent duplicates.
    - Commented out anything that doesn't deal in `users`. This includes imports. 
    
### Removed
 - Removed in `Register.jsx`
    - Removed prior CRA-specific env usage (`process.env.REACT_APP_API_URL`) from registration flow and Firebase initialization.
  - Removed `AdminPage.jsx`
  - Removed all tables in ArtBook database
  - Removed in `users.py` in `routers/`
    - Removed any need to send `uid` in request body.
  - Removed in `user.py` in `schemas`
    - Removed `uid` from UserCreate — the backend now derives it from the Firebase token.

### Fixed

  - 404 error during registration caused by mismatch between frontend route `(/users)` and backend route `(/users/users)`.
  - 422 (Unprocessable Content) error fixed by explicitly including `display_name` in `Register.jsx` request body.
  - React Vite migration issues:
    - Corrected import paths `(../components/...` vs `./...)` in `Admin.jsx `and related pages.
    - Ensured JSX runtime compatibility with Vite `(jsxDEV)`.
    - Missing dependency error: resolved by replacing `axios` with `fetch` in early tests, then reinstating `axios` with `npm install axios`.
  - Fixed in `firebase_auth` in `utils`
    - Changed parameter from `auth_header → authorization: str = Header(...)`.
      - Now binds correctly to the `Authorization: Bearer` ... header you’re sending.
    - Firebase initialized only once with `if not firebase_admin._apps`.

## [1.0.5] - 2025-09-24
### Added
- Added `Table of Contents` section to `README.md`
- Added `QuickStart` section to `README.md`
- Added `Environment Variables` section to `README.md`
- Added in `users.py` in `routers/`
  - Creator-only role-management endpoint: `PUT /users/{user_id}/roles` to grant/revoke is_admin and is_creator.
  - Admin/creator user-management endpoint: `PUT /users/{user_id}` to update user fields with creator/admin restrictions.
- Added in `user.py` in `schemas`
    - Added `is_creator` variable in schema.
- Added in `users.py` in `models/`
  - Added `is_creator` boolean column to User model (default: False).
- Added in `set_admin.py` in `scripts`. 
  - Added a way to set and remove admin claims. 
  - Added guard to prevent modification of creator accounts.
  - Added optional DB sync: if `BACKEND_URL` and `ADMIN_API_KEY` env vars are set, the script will call the backend creator-only role endpoint (`PUT /api/users/{uid}/roles`) to keep the DB as the source of truth in sync with Firebase claims.
- Added in `schema.sql` in `db`
  - Added `is_creator` BOOLEAN column (NOT NULL DEFAULT FALSE).
- Added in `database.py` in `db/`
  - Added environment validation: raises a clear error if `DATABASE_URL` is not set.
### Changed
- Changed `README.md`
  - Updated "API Endpoints (FastAPI)" section to point to the local OpenAPI docs: http://localhost:8000/docs#/
  - Documented current backend endpoints (Auth, Users, Posts, Social, Admin) and their purposes, including:
    - Auth: `POST /auth/verify-token`
    - Users: `GET /users/me`, `POST /users`, `PUT /me`, `PUT /users/{user_id}`, `PUT /users/{user_id}/roles`
    - Posts: `POST /posts/create`, `GET /posts/feed`, `POST /posts/{id}/like`, `POST /posts/{id}/comments`, `POST /posts/{id}/flag`
    - Social: `POST /follow/{user_id}`
    - Admin: `GET /admin/*`, `DELETE /admin/users/{user_id}`, `DELETE /admin/posts/{post_id}`
  - Added notes about using the interactive docs, required `Authorization: Bearer <id_token>` header, and that role management should use the creator-only DB endpoint so the database remains the source of truth.
- Changed `Project Structure` section in `README.md`
- Changed `users.py` in `models/`
  - Ensured `firebase_uid` and `email` have indexes/uniqueness for efficient lookups.
  - `created_at` set to default to `datetime.utcnow()` for new records.
  - Reminder: run a DB migration (alembic revision --autogenerate -m "users: add is_creator" && alembic upgrade head) to apply model changes.
  - Optional: consider adding a __repr__ or audit fields if needed for debugging and role-change traceability.
- Changed `set_admin.py` in `scripts`. 
  - Wrapped code in `try-except`for error handling.
  - Changed added a cred path to the `.env` variable so that it's not hard coded into the program. 
  - Replaced hard-coded service account path with `FIREBASE_CRED_PATH` env var.
  - Fixed bug when `custom_claims` is `None` (now handled as empty dict).
  - Improved CLI prompts and logging output.
- Changed `admin.py` in `routers`
  - Uses `require_creator` for role management
  - Prevents creator account deletion or demotion
  - New users default to `is_admin = False` and `is_creator = False` on creation.
  - Regular users cannot change role flags via `/me` (only allowed fields: display_name, bio, avatar_url).
  - Creators can edit anyone and change roles; admins can edit non-admin/non-creator users only and cannot change role flags.
  - `users.py` router updated to enforce role boundaries and use DB as source of truth for roles.
- Changed `users.py` in `routers`
- Changed `user.py` in `schemas`
  - Made `display_name` required and treated as the user's username (UserCreate.display_name is now required).
  - Updated `UserUpdate` to allow optional `display_name` for edits.
  - Updated `UserResponse` to include `display_name` and `is_creator`; `Config.orm_mode = True` set for ORM compatibility.
  - Ensured schemas align with `backend/models/users.py` (including `is_creator`).
- Changed `schema.sql` in `db/`
  - Ensured `display_name` is NOT NULL and backfilled NULL values with `CONCAT('user_', id)`.
  - Confirmed `created_at` uses `CURRENT_TIMESTAMP` default for new records.
  - Verified foreign key constraints for `posts`, `comments`, `likes`, and `followers` reference `users(id)` with `ON DELETE CASCADE`.
  - Reminder: apply the SQL changes or run DB migration to sync schema with models.

- Changed `database.py` in `db/`
  - Enabled `pool_pre_ping=True` to reduce stale connection errors.
  - Made SQLAlchemy `echo` configurable via `SQLALCHEMY_ECHO` env var for debug logging.
  - Set `SessionLocal` with `expire_on_commit=False` to keep ORM objects usable after commit (configurable choice).
  - Overall: improved robustness and clearer failure modes for DB connection handling.
### Removed
- Removed  `Running Locally` Section. 
- Removed in `user.py` in `schemas`
  - Removed `firebase_uid` from `UserCreate` (server assigns UID from token / auth).
- Removed in `admin.py` in `routers`
  - Removed token-based admin sync; roles are no longer trusted from token claims.
- Removed in `users.py` in `routers`
  - Removed duplicate imports for the FastAPI
  - Removed duplicate function name read_currently_user (one helper and one route)
  - Removed overlapping routes `/me` and `/users/me`. 

### Security
- in `users.py` in `routers/`
  - Role elevation now requires a creator action (prevents untrusted token claims from granting admin/creator).

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

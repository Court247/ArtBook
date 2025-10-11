# Changelog

All notable changes to this project will be documented in this file.

## [1.0.10]

### Added
- Added `routers/`
  - `notifications.py`
    - Added `/notifications` routes for retrieval and marking read.
    - Connected to Pydantic response model.
    - Unified ordering and pagination logic.
  - `repost.py`
    - Added repost + quote repost creation logic.
    - Added notifications for original post author.
    - Split endpoints for simple reposts and quote reposts.
    - Added retrieval routes for user reposts and quotes separately.  
- Added `schemas/`
  - `notifications.py`
    - New file created.
    - Added `NotificationCreate` and `NotificationResponse` schemas.
    - Covers all notification event types.
  - `repost.py`
    - New schema added for the repost/quote repost feature.
    - Added `RepostCreate` model to handle `original_post_id` and optional `quote`.
    - Added `RepostResponse` model for returning repost details (`id`, `user_id`, `original_post_id`, `quote`, `is_quote`, `created_at`).
    - Integrated with repost router to support both simple and quote repost types.
    - Configured `from_attributes = True` for ORM compatibility.
- Added `utils/`
  - `notificaitons.py`
- Added `models/`
  - `notifications.py`
    - Rebuilt relationships to include `back_populates` for `Post` and `Comment`.
    - Enum types standardized: (`like`, `comment`, `follow`, `share`).
    - Ensured cross-model linkage consistency.
  - `repost.py`
    - Added new `Repost` model.
    - Fields: `user_id`, `original_post_id`, `quote`, `is_quote`, `created_at`.
    - Added relationships: `user`, `original_post`.
    - Supports both simple reposts and quote reposts.

### Changed
- Changed in `utils/` folder
  - `firebase_auth.py`
    - Refactored Firebase initialization for cleaner error handling.
    - Added lazy app initialization to prevent multiple Firebase app instances.
    - Fixed incorrect environment variable (`FIREBASE_CRED_PATH` → `FIREBASE_AUTH_EMULATOR_HOST`) for emulator mode.
    - Simplified token verification logic and unified with `get_current_user`.
    - Improved return data to include Firebase UID mapping.
  - notifications.py
    - Added reusable `create_notification()` helper for universal event notifications.
    - Implemented automatic self-notification prevention.
    - Added support for all event types (`like`, `comment`, `follow`, `share`).
    - Integrated commit and refresh handling for DB safety.
    - Standardized notification creation across routers.
- Changed in `database/` folder
  - `database.py`
    - Confirmed consistent `SessionLocal` and `engine` creation.
    - Cleaned up base import and removed deprecated references.
  - `schema.sql`
    - Added full schema for reposts feature (`reposts` table).
    - Retained all relationships and constraints with `ON DELETE CASCADE`.
    - Added indexes for performance on `user_id` and `post_id`.
    - Verified all foreign key references align with Firebase UID mapping.
- Changed in `models/` folder
  - `users.py`
    - Expanded role and status enums (`creator`, `admin`, `premium`, `regular`).
    - Added notification relationships (`sent_notifications`, `received_notifications`).
    - Added `reposts` relationship (`reposts`) for new repost system.
    - Cleaned follow relationships and cascade rules.
  - `post.py`
    - Added `reposts` relationship linking to `Repost` model.
    - Added `notifications` relationship for event tracking.
    - Verified `visibility` enum consistency (`public`, `private`, `followers`).
  - `comment.py`
    - Linked notifications to `comment` interactions.
    - Confirmed one-to-many with `CommentLike`.
    - Standardized naming to `author` instead of `user` for clarity.
  - `like.py`
    - Verified unique constraint (`user_id`, `post_id`).
    - Retained clean relationship with `User` and `Post`.
    - Confirmed notification trigger readiness for post likes.
  - `comment_like.py`
    - Added UniqueConstraint on (`user_id`, `comment_id`).
    - Integrated relationship with `User` and `Comment`.
    - Prepared for automatic notification creation.
  - `follow.py`
    - Confirmed cascade deletion.
    - Integrated unique constraint (`follower_id`, `following_id`).
    - Router now triggers “follow” notifications.
- Changed in `schemas/`
  - `user.py`
    - Simplified user responses and made Firebase UID explicit.
    - Unified field names to match DB (`display_name`, `avatar_url`).
  - `post.py`
    - Added fields for repost and embedded post display.
    - Fixed duplicate `FeedUser`/`FeedPostResponse` definitions.
    - Cleaned up validation and relationships.
  - `comment.py`
    - Standardized output with consistent field naming.
    - Prepared for extended notifications integration.
  - `comment_likes.py`
    - Added `CommentLikeResponse` and `CommentLikeCreate`.
    - Linked timestamps and user relationships.
  - `follow.py`
    - Added minimalistic Pydantic models for follow system consistency.
  - `post_flag.py`
    - Added optional `reason` field and audit-ready `reviewed` flag.
- Changed in `routers/` 
  - `admin.py`
    - Confirmed consistent imports and route registration.
  - `users.py`
    - Integrated Firebase UID references throughout.
    - Cleaned and simplified endpoints for fetching and updating user data.
  - `posts.py`
    - Verified post creation, editing, and visibility handling.
    - Prepared for embedded repost display in feeds.
  - `comments.py`
    - Added notification trigger for post comments.
    - Enforced `post_id` validation.
    - Removed duplicate functions and cleaned route structure.
  - `comment_likes.py`
    - Removed duplicate route definitions that caused syntax errors.
    - Unified into single toggle endpoint.
    - Added notification trigger for comment author on like.
  - `likes.py`
    - Added notification trigger for post likes.
    - Refactored toggle logic for idempotent like/unlike behavior.
    - Cleaned imports and removed duplicate parentheses causing crash.
  - `follow.py`
    - Added notification trigger for new followers.
    - Added duplication guard to prevent refollowing.
    - Cleaned logic for self-follow prevention.
  - `home.py`
    - Fixed missing `id` in `FeedUser` construction.
    - Cleaned random feed logic and ordering.
  - `admin.py`
    - Minor formatting and import cleanup.
## [1.0.9] - 2025-10-09

### Added
- Added `schema/post_flag.py` 
- Added `models/post_flag.py`
- Added `routers/post_flag.py` 
- Added new relationship schema in `README.md`
- Added new table `comment_likes`
- Added `models/comment_like.py`
  - keeps track of comment likes
- Added `schema/comment_likes.py`
- Added `routers/comment_likes.py`
- Added `notifications `database table
  - Notifies user of likes, comments, or follows. 
- Added `repost` database table
  - Allows users to repost and share posts.
### Changed
- Changed `db/schema.sql`
  - `Users` table
    - Added auto-incrementing `id` (primary key)
    - Changed `firebase_uid` as `VARCHAR(128) UNIQUE NOT NULL`
    - Removed defaults
  - `Posts` table
    - References `users(id) `
    - Added `media_url` and `visibility`
  - `Likes` table
    - Has `UNIQUE` composite keys (`user_id`, `post_id` and `follower_id`, `following_id`)
    - Proper cascading delete behavior
  - `Follows` table
    - Has `UNIQUE` composite keys (`user_id`, `post_id` and `follower_id`, `following_id`)
    - Proper cascading delete behavior
  - `Comments` table
    - Links properly to both posts and users
  - `Post_flag` table
    - New moderation table (`reported_by`, `reason`, `reviewed`)
- Changed `schemas/`files
  - `schemas/user.py`
    - Added `INT AUTO_INCREMENT` primary keys
    - Keep `firebase_uid` as unique
  - `schemas/comment.py`
    - Added `INT AUTO_INCREMENT` primary keys
    - Keep `firebase_uid` as unique
  - `schemas/follow.py`
    - Added `INT AUTO_INCREMENT` primary keys
    - Keep `firebase_uid` as unique
  - `schemas/like.py`
    - Added `INT AUTO_INCREMENT` primary keys
    - Keep `firebase_uid` as unique
  - `schemas/post.py`
    - Added `INT AUTO_INCREMENT` primary keys
    - Keep `firebase_uid` as unique
    - Include the new `visibility`and `media_url`
  - `schemas/post_flag.py`
    - Added `INT AUTO_INCREMENT` primary keys
    - Keep `firebase_uid` as unique
- Changed `models/` files
  - Added `INT AUTO_INCREMENT` primary keys
  - All relationships are consistent and cascade properly
  - `visibility`, `post_flags`, and constraints are correct
  - `firebase_uid` is still unique but not a PK
- Changed `main.py`
  - CORS safe
- Changed `models/`
  - `comment.py`
    - Added new `like` relationship
  - `users.py`
    - Added new `commment_likes` relationship



## [1.0.8] - 2025-09-27

### Added
- `README.md`
  - Added "Home" Section in API Endpoints 
  - Added 'Followers" section to API Endpoints
- Added to `models/`
  - `follow.py`
- Added to `routers/`
  - `follow.py`
  - home.py
- Added to `schemas/`
  - `follow.py`
- `firebase_auth.py`
  - Added `get_current_user` method to get the current user
- `comments.py` in `schemas/`
  - Created Pydantic schemas:
    - `CommentBase` → holds `content`.
    - `CommentCreate` → extends base, adds `post_id`.
    - `CommentResponse` → full representation (`id`, `user_id`, `post_id`, `content`, `created_at`).
  - Added `Config.from_attributes = True`for SQLAlchemy compatibility.
- `comments.py` in `routers/`
  - Added endpoints:
    - POST `/comments/` → create a comment on a post.
      - Requires valid post ID, authenticated user.
    - GET `/comments/post/{post_id}` → list all comments on a post.
      - Sorted by newest first.
    - DELETE `/comments/{comment_id}` → delete a comment.
      - Allowed if: comment owner OR `creator`/`admin`.
- New tables to database
  - posts
  - likes
  - follows
  - comments
### Changed
- `README.md`
  - Changed the "Users" Section in the API Endpoints
- `posts.py` in `routers/`
  - uncommented routers
  - Confirmed `comments` relationship already exists:
  - `comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")`

- `comment.py`in` models/`
  - Added `Comment` model with fields:
    - `id` (UUID string, primary key)
    - `user_id` → FK to `users.firebase_uid`
    - `post_id` → FK to `posts.id`
    - `content` (text)
    - `created_at` (datetime, default now)
  - Relationships:
    - `author` → back to `User.comments`
    - `post` → back to `Post.comments`
- `users.py` in `models/`
  - Added `comments` relationship:
    - `comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")`
- `main.py` in `backend/`
  - registered comments router
- routers/
  - updated all router folders to properly process `firebase_uid` instead of `user_id`
### Removed
- `README.md`
  - Removed the "Auth" section in the API Endpoints
  - Removed the "Social", "Posts", and "Admin" API Endpoints section in the read me. Will add them as the building progresses. Saves confusion and frustration.

## [1.0.7] - 2025-09-26

### Added
- `Register.jsx` in `pages/`
  - Added `firebase_uid: firebaseUser.uid` to the request body.
- `users.py` in `models/`
  - Added a single `role` column using an Enum (`creator`, `admin`, `premium`, `regular`).
  - Helper methods `is_creator()` and `is_admin()` make permission checks simpler.
- `firebase_auth.py` in `utils/`
  - Added token verification helper (`get_token_payload`) that reads Firebase ID tokens.
  - Added `set_custom_user_claims` so backend can sync Firebase custom claims (`admin: True`, `creator: True`).
  - Added a function `enforce_user_status(user)`
- Role-based system added
  - We refactored your backend to use a `role` column instead of separate `is_creator` / `is_admin` booleans.
  - Roles available: `creator`, `admin`, `regular `(expandable to `premium` later).
  - Enforcement logic:
    - __Creator__: can do everything, including promoting/demoting admins.
    - __Admin__: can manage regular/premium users, but not creators or other admins.
    - __Regular__: can only edit their own data.
### Changed
- `Register.jsx` in `pages/`
  - Included `bio` + `avatar_url` as empty strings (safe defaults).
- `users.py` in `models/`
  - Database migration SQL provided:
      - Add `role` column (default `regular`).
      - Convert old booleans into `role`.
      - Drop old columns when safe.
- `users.py` in `schemas/`
  - Updated Pydantic models to use `role` instead of multiple booleans.
  - `UserCreate` accepts `firebase_uid` and optional `role` (but by default it’s `regular`).
  - `UserUpdate` only allows updating profile fields (no role changes).
  - `UserResponse` includes `role` so frontend can display it.
  - Updated for Pydantic v2 (`from_attributes = True`).
- `firebase_auth.py` in `utils/`
  - Defined permission helpers:
    -` require_creator()` → only creators can continue.
    - `require_admin()` → allows admins & creators.
    - `require_self_or_admin()` → user can update their own data, or admins/creators can.
    - `forbid_admin_on_creator_db()` → prevents admins from touching creator accounts.
    - `forbid_admin_on_admin_db()` → prevents admins from editing other admins (only creators can).
- `users.py` in `routers/`
  - `POST /users/` → create a new user, defaults to `role="regular"`.
  - `GET /users/me` → returns the logged-in user.
  - `PUT /users/{firebase_uid}` → update profile info.
  - Checks: user can update self, or admin/creator can update others.
  - Admins cannot update creators or other admins.
  - Only profile fields (no `role` changes here).
- `admin.py` in `routers/`
  - `GET /admin/dashboard` → example admin-only endpoint.
  - `GET /admin/users` → list all users (admin/creator only).
  - `DELETE /admin/users/{firebase_uid}` → delete a user.
  - Admins cannot delete creators or other admins (only creators can).
  - `POST /admin/promote-user/{firebase_uid}` → creator-only.
  - Promote/demote users to/from admin.
  - Updates both DB (`role`) and Firebase custom claims (admin).
- Profile status enforcement introduced
  - Added a `status` column to `User` model (inside `models/users.py`).
  - Enum `StatusEnum`: `active`, `deleted`, `suspended`, `banned`.
  - Default is `active`.
- Status enforcement logic
  - Added a function `enforce_user_status(user)` in `firebase_auth.py`.
  - Blocks access if the user is `deleted`, `suspended`, or `banned`.
### Removed
- `Register.jsx` in `pages/`
  - Removed `password` from the payload (since backend doesn’t expect it).
- `users.py` in `models/`
  - Removed `is_creator` and `is_admin` boolean flags.
### Fixed
- `firebase_auth.py` in `utils/`
  - He error `NameError: name 'models'` is not defined fixed
  - Fixed by importing directly from `models/users.py`


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

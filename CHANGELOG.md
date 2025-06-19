# Changelog

All notable changes to this project will be documented in this file.

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

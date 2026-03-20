# ArtBook Backend TODO

## Critical Bugs

- [x] **Fix broken unfollow endpoint** — `router_follow.py:66` has a variable name mismatch that causes a `NameError` crash on `DELETE /follow/{following_id}`
- [x] **Fix missing Post import in admin router** — `router_admin.py` uses the `Post` model but never imports it, crashing `GET /admin/posts`
- [x] **Fix duplicate relationship definitions in Notification model** — `model_notifications.py` defines `recipient` and `sender` relationships twice, causing unpredictable SQLAlchemy behavior

---

## Privacy / Security Bugs

- [ ] **Enforce post visibility on `GET /posts/`** — currently returns all posts (including private and followers-only) to unauthenticated users
- [ ] **Enforce post visibility on `GET /posts/user/{user_id}`** — same issue, no auth and no visibility filtering
- [ ] **Add auth to `GET /home/trending`** — currently fully public with no token required
- [ ] **Block follows to suspended/deleted/banned users** — `router_follow.py` doesn't check the target user's status before allowing a follow

---

## Missing Endpoints

- [ ] **`GET /posts/{post_id}`** — no way to fetch a single post by ID
- [ ] **`PUT /posts/{post_id}`** — no way to edit a post
- [ ] **`DELETE /repost/{id}`** — users cannot remove their reposts
- [ ] **`POST /upload`** — image upload utility exists in `utils/image_upload.py` but there is no router endpoint wired up to it
- [ ] **`GET /users/{user_id}`** — no public profile view endpoint with follower/post counts
- [ ] **`GET /follow/status/{user_id}`** — no way to check if the current user follows someone (needed for Follow/Following button state)
- [ ] **`PUT /comments/{id}`** — no way to edit a comment

---

## Input Validation

- [x] **Add content length validation to posts** — no min/max length enforced in schema
- [ ] **Add content validation to comments** — empty comments and excessively long comments are allowed
- [x] **Add display name length validation to user schema** — no min/max on `display_name`
- [x] **Validate media URLs** — `media_url` on posts accepts any string with no URL format check

---

## Response Schema Improvements

- [ ] **Include author info in `PostResponse`** — currently only returns `user_id`, forcing the frontend to make a second query to get author details
- [ ] **Include author info in `CommentResponse`** — same issue
- [ ] **Include original post content in `RepostResponse`** — currently only returns `original_post_id`, not the post itself

---

## Performance

- [ ] **Fix N+1 query pattern in `GET /home/feed`** — for each post, separate queries are made for the author and each comment's author; should use joins or eager loading
- [ ] **Fix Python-side sorting in `GET /home/activity`** — fetches all likes into Python then sorts, instead of using SQL `ORDER BY`
- [ ] **Include reposts in `GET /home/feed`** — the feed currently only shows original posts, not reposts from followed users

---

## Error Handling

- [ ] **Add try/except around `db.commit()` calls across all routers** — unhandled database errors return unhelpful 500 responses
- [ ] **Standardise like/unlike response format** — `router_comment_likes.py` returns a `JSONResponse` for unlike but a model object for like; should be consistent

---

## Notifications

- [ ] **Add `POST /notifications/read-all`** — no way to mark all notifications as read at once
- [ ] **Add `DELETE /notifications/{id}`** — no way to delete a notification
- [ ] **Add pagination to `GET /notifications`** — no limit/offset support

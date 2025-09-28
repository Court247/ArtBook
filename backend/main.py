from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users as users_router, follow as follow_router, posts as posts_router, home as home_router, comments, likes, admin

app = FastAPI(
    title="ArtBook",
    version="1.0.8",
    description="Backend API for a cross-platform social media app using FastAPI, MySQL, and Firebase."
)

# 🛡️ CORS (adjust allowed_origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: replace with exact domains in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 Route registration
app.include_router(users_router.router)
app.include_router(home_router.router)
app.include_router(follow_router.router)
app.include_router(posts_router.router)
app.include_router(comments.router)
app.include_router(likes.router)
app.include_router(admin.router)

# ✅ Health check
@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}

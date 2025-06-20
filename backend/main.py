from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import users, posts, comments, likes, admin

app = FastAPI(
    title="ArtBook",
    version="1.0.2",
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
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(comments.router, tags=["Comments"])
app.include_router(likes.router, tags=["Likes"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])  # 👈 new

# ✅ Health check
@app.get("/")
def root():
    return {"message": "Backend is running 🚀"}

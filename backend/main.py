# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ⚙️ Load environment variables (optional)
# from dotenv import load_dotenv
# load_dotenv()

# 🧱 Initialize Database (do not move this)
from db.database import Base, engine

# ⚠️ Initialize FastAPI app BEFORE importing firebase or routers
app = FastAPI(
    title="ArtBook",
    version="1.0.9",
    description="FastAPI backend for ArtBook with Firebase Auth and MySQL.",
)

# ---------------------------------------------------------
# ✅ CORS Middleware must be registered *before* routers or Firebase
# ---------------------------------------------------------
origins = [
    "http://localhost:5173",        # Vite dev server
    "http://127.0.0.1:5173",
    "https://artbook.app",          # production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Explicit origins only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # Or: ["Authorization", "Content-Type"]
)

# ---------------------------------------------------------
# Import Firebase AFTER middleware
# ---------------------------------------------------------
import utils.firebase_auth  # initializes Firebase here safely

# ---------------------------------------------------------
# Initialize database (optional for dev)
# ---------------------------------------------------------
Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------
# Import and register routers AFTER app + middleware setup
# ---------------------------------------------------------
from routers import (
    users as users_router,
    posts as posts_router,
    comments as comments_router,
    likes as likes_router,
    follow as follow_router,
    home as home_router,
    admin as admin_router,
    comment_likes as comment_likes_router,
)

app.include_router(users_router.router)
app.include_router(posts_router.router)
app.include_router(comments_router.router)
app.include_router(likes_router.router)
app.include_router(follow_router.router)
app.include_router(home_router.router)
app.include_router(admin_router.router)
app.include_router(comment_likes_router.router)


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------
@app.get("/")
def root():
    return {"message": "ArtBook Backend is running 🚀"}

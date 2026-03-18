# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.database import Base, engine

# Import ALL models so Base.metadata knows every table
from models import (
    model_users,
    model_post,
    model_comment,
    model_like,
    model_follow,
    model_post_flag,
    model_comment_like,
    model_notifications,
    model_repost,
)

app = FastAPI(
    title="ArtBook",
    version="1.0.13",
    description="FastAPI backend for ArtBook with Firebase Auth and MySQL.",
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://artbook.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Init Firebase AFTER middleware
import utils.firebase_auth  # noqa: F401

# Dev convenience (creates missing tables)
Base.metadata.create_all(bind=engine)

# Routers
from routers import (
    router_users,
    router_posts,
    router_comments,
    router_likes,
    router_follow,
    router_home,
    router_admin,
    router_comment_likes,
    router_notifications,
    router_repost,
)

app.include_router(router_users.router)
app.include_router(router_posts.router)
app.include_router(router_comments.router)
app.include_router(router_likes.router)
app.include_router(router_follow.router)
app.include_router(router_home.router)
app.include_router(router_admin.router)
app.include_router(router_comment_likes.router)
app.include_router(router_notifications.router)
app.include_router(router_repost.router)


@app.get("/")
def root():
    return {"message": "ArtBook Backend is running"}

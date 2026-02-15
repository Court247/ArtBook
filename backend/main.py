	# main.py
	from fastapi import FastAPI
	from fastapi.middleware.cors import CORSMiddleware
	
	# �sT�,? Load environment variables (optional)
	# from dotenv import load_dotenv
	# load_dotenv()
	
	# dY� Initialize Database (do not move this)
	from backend.models import model_comment as _comment_model, model_comment_like as _comment_like_model, model_follow as _follow_model, model_like as _like_model, model_notifications as _notifications_model, model_post as _post_model, model_post_flag as _post_flag_model, model_repost as _repost_model
from backend.routers import router_admin as admin_router, router_comment_likes as comment_likes_router, router_comments as comments_router, router_follow as follow_router, router_home as home_router, router_likes as likes_router, router_notifications as notifications_router, router_posts as posts_router, router_repost as repost_router
from db.database import Base, engine
	
	# �s��,? Initialize FastAPI app BEFORE importing firebase or routers
	app = FastAPI(
	    title="ArtBook",
	    version="1.0.10",
	    description="FastAPI backend for ArtBook with Firebase Auth and MySQL.",
	)
	
	# ---------------------------------------------------------
	# �o. CORS Middleware must be registered *before* routers or Firebase
	# ---------------------------------------------------------
	origins = [
	    "http://localhost:5173",        # Vite dev server
	    "http://127.0.0.1:5173",
	    "http://localhost:3000",        # CRA dev server
	    "http://127.0.0.1:3000",
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
	# Ensure all models are imported before creating tables
	# ---------------------------------------------------------
	# This guarantees Base.metadata knows about every table.
	from backend.models import (
	    model_users as _users_model,
	)
	
	# ---------------------------------------------------------
	# Initialize database (optional for dev)
	# ---------------------------------------------------------
	Base.metadata.create_all(bind=engine)
	
	# ---------------------------------------------------------
	# Import and register routers AFTER app + middleware setup
	# ---------------------------------------------------------
	from backend.routers import (
	    router_users as users_router,
	)
	
	app.include_router(users_router.router)
	app.include_router(posts_router.router)
	app.include_router(comments_router.router)
	app.include_router(likes_router.router)
	app.include_router(follow_router.router)
	app.include_router(home_router.router)
	app.include_router(admin_router.router)
	app.include_router(comment_likes_router.router)
	app.include_router(notifications_router.router)
	app.include_router(repost_router.router)
	
	
	
	
	# ---------------------------------------------------------
	# Health check
	# ---------------------------------------------------------
	@app.get("/")
	def root():
	    return {"message": "ArtBook Backend is running dYs?"}


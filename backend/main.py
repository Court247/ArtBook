from fastapi import FastAPI
from routers import users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Social Media Backend is running"}

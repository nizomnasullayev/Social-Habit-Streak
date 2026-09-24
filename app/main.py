from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, habits

app = FastAPI(title="My App")
app.router.redirect_slashes = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(habits.router)

@app.get("/")
def root():
    return {"message": "API is running"}
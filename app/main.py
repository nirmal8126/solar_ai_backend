from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, leads, chat
from app.auth.router import router as auth_router
app.include_router(auth_router, prefix="/auth")

app = FastAPI(title="Solar AI Backend")

# CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REGISTER ROUTERS (must come AFTER app = FastAPI)
app.include_router(health.router)
app.include_router(leads.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Solar AI Backend is running"}

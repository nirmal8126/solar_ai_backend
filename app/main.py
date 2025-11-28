from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.auth.router import router as auth_router
from app.routers import health, leads, chat

app = FastAPI(title="Solar AI Backend")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- REGISTER ROUTERS ---
app.include_router(auth_router)           # /auth/*
app.include_router(health.router)
app.include_router(leads.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Solar AI Backend is running"}

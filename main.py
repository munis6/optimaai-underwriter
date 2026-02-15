from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import router

print(">>> MAIN.PY LOADED <<<")

app = FastAPI()

# ============================
# CORS FIX (REQUIRED FOR FRONTEND)
# ============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # allow all origins for demo
    allow_credentials=True,
    allow_methods=["*"],      # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)

# Register all routes
app.include_router(router)

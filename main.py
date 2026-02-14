from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.router import router

print(">>> MAIN.PY LOADED <<<")

app = FastAPI()

# Register all routes from router.py
app.include_router(router)


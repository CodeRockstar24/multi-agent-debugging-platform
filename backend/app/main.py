from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.db.database import init_db

app = FastAPI(
    title="Code Debugger AI Backend",
    description="Backend for a multi-agent software debugging assistant",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Code Debugger AI backend is running"
    }

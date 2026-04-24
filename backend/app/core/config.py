import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    app_name: str = "Code Debugger AI Backend"
    version: str = "0.1.0"
    debug: bool = True
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    pinecone_api_key: str | None = os.getenv("PINECONE_API_KEY")
    pinecone_index_name: str = os.getenv("PINECONE_INDEX_NAME", "code-debugger-memory")


settings = Settings()

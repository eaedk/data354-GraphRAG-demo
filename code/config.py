import os
from pathlib import Path


class Config:
    class Path:
        APP_HOME = Path(os.getenv("APP_HOME", Path(__file__).parent.parent))
        DATABASE_DIR = APP_HOME / "docs-db"
        DOCUMENTS_DIR = APP_HOME / "tmp"
        IMAGES_DIR = APP_HOME / "code" / "assets" / "images"

    class Database:
        DOCUMENTS_COLLECTION = "vector" # or "documents"

    class Model:
        EMBEDDINGS = "text-embedding-ada-002" #"llama3.1" #"nomic-embed-text" #"BAAI/bge-base-en-v1.5" # 
        LOCAL_LLM = "gemma2:9b" # or "llama3.1"
        REMOTE_LLM = "gpt-4o" #or "llama-3.1-70b-versatile"
        TEMPERATURE = 0.0
        MAX_TOKENS = 8000 # if needed
        USE_LOCAL = False

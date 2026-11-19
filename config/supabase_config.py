from supabase import create_client
from dotenv import load_dotenv


import os


def createDatabaseClient():
    try:
        load_dotenv()
        url: str | None = os.getenv("supabaseUrl")
        key: str | None = os.getenv("supabaseKey")

        if not url or not key:
            raise ValueError("Could not connect to database")

        supabase = create_client(supabase_key=key, supabase_url=url)
        return supabase
    except Exception:
        raise

import os
import time
import threading
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# Load credentials from .env file
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client safely
supabase: Client | None = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Failed to connect to Supabase: {e}")

def start_keep_alive():
    """
    Background thread that runs every 6 minutes (360 seconds)
    to insert a blank/pulse record, keeping the free tier active.
    """
    def ping_database():
        while True:
            if supabase:
                try:
                    # Assumes you created a table named 'keep_alive' with a 'last_pulse' column
                    supabase.table('keep_alive').insert({
                        "last_pulse": str(datetime.now()),
                        "status": "active_pulse"
                    }).execute()
                    print(f"[{datetime.now()}] Supabase ping successful.")
                except Exception as e:
                    print(f"Supabase ping failed: {e}")
            
            # Wait exactly 6 minutes before pinging again
            time.sleep(360)

    # Run as a daemon thread so it closes when the server stops
    thread = threading.Thread(target=ping_database, daemon=True)
    thread.start()
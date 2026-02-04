import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")
service_key: str = os.environ.get("SUPABASE_SERVICE_KEY", "")

if not url:
    print("Warning: SUPABASE_URL not set")

# Standard client (uses Anon key usually)
supabase: Client = create_client(url, key)

# Admin client (uses Service Role key) - Use this for backend ops that need to bypass RLS (like checking invite tokens if table is restricted)
# Only create if key exists
supabase_admin: Client = None
if service_key:
    supabase_admin = create_client(url, service_key)

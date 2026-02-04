import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load env vars
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
service_key = os.environ.get("SUPABASE_SERVICE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_KEY not found in environment.")
    exit(1)

# Use service key if available to bypass RLS
if service_key:
    # print("Using Service Key (Admin)...")
    supabase: Client = create_client(url, service_key)
else:
    print("Using Anon Key (RLS enforced)...")
    supabase: Client = create_client(url, key)

print("Fetching Painting Guides...")

try:
    # Fetch guides
    res = supabase.table("painting_guides").select("*").execute()
    
    guides = res.data
    print(f"Found {len(guides)} guides.")
    
    for g in guides:
        img_id = g.get("image_drive_id")
        print(f"- Guide: {g.get('name')} (ID: {g.get('id')})")
        print(f"  Image Drive ID: {img_id if img_id else 'None'}")
        
        if img_id:
            print(f"  --> Has Image!")
        else:
            print(f"  --> No Image")
            
except Exception as e:
    print(f"Error fetching data: {e}")

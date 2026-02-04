
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: Missing env vars")
    exit(1)

supabase: Client = create_client(url, key)

email = "cvesspy@gmail.com"
password = "gyn9zjf-jqn4ZHA6kmh"
try:
    supabase.auth.sign_in_with_password({"email": email, "password": password})
    print("Signed in successfully.")
except Exception as e:
    print(f"Sign in failed: {e}")
    exit(1)

print("--- Testing Select * ---")
try:
    res = supabase.table("catalog_paints").select("*").limit(5).execute()
    print(f"Select * success. Rows: {len(res.data)}")
    if res.data:
        print(f"Sample: {res.data[0]['name']}")
except Exception as e:
    print(f"Select * failed: {e}")

print("\n--- Testing Select with Join ---")
try:
    res = supabase.table("catalog_paints").select("*, paint_brands(name)").limit(5).execute()
    print(f"Select Join success. Rows: {len(res.data)}")
    if res.data:
        print(f"Sample with brand: {res.data[0]['name']} - {res.data[0].get('paint_brands')}")
except Exception as e:
    print(f"Select Join failed: {e}")

print("\n--- Testing Search 'black' ---")
try:
    res = supabase.table("catalog_paints").select("*, paint_brands(name)").ilike("name", "%black%").limit(5).execute()
    print(f"Search success. Rows: {len(res.data)}")
    for p in res.data:
        print(f"- {p['name']}")
except Exception as e:
    print(f"Search failed: {e}")

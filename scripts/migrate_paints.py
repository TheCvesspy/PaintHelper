import os
import re
import sys
from supabase import create_client, Client
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL and SUPABASE_KEY must be set in .env")
    sys.exit(1)

supabase: Client = create_client(url, key)

ASSETS_DIR = Path("assets/paints")

def parse_markdown_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.readlines()

    brand_name = None
    logo_path = None
    paints = []
    
    headers = []
    cols_map = {}

    for line in content:
        line = line.strip()
        if not line:
            continue
        
        # Extract Brand Name
        if line.startswith("# "):
            brand_name = line[2:].strip()
            continue
        
        # Extract Logo
        if line.startswith("![") and "logos" in line:
            # Match (path) or (path "title")
            match = re.search(r'\(([^"\s\)]+)', line)
            if match:
                raw_path = match.group(1)
                # Clean path: remove ../ if present
                logo_path = raw_path.replace("../", "")
            continue
            
        # Parse Table Header
        if line.startswith("|") and "Name" in line and not headers:
            headers = [h.strip() for h in line.strip("|").split("|")]
            for idx, h in enumerate(headers):
                cols_map[h] = idx
            continue
            
        # Parse Table Row
        if line.startswith("|") and not "---" in line and headers:
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) != len(headers):
                # Handle cases where pipes might be missing or extra? 
                # For now assume mostly correct, or skip malformed
                if len(parts) < len(headers):
                     # pad with empty strings
                     parts += [""] * (len(headers) - len(parts))
                else:
                     parts = parts[:len(headers)]

            row_data = {}
            for col_name, idx in cols_map.items():
                if idx < len(parts):
                    row_data[col_name] = parts[idx]
            
            # Extract Hex and clean it
            hex_val = None
            raw_hex_field = ""
            if "Hex" in row_data:
                raw_hex_field = row_data["Hex"]
            
            # Regex to find #123456 inside the cell
            hex_match = re.search(r'(#[0-9A-Fa-f]{6})', raw_hex_field)
            if hex_match:
                hex_val = hex_match.group(1)
            elif raw_hex_field.startswith("#"):
                 hex_val = raw_hex_field[:7] # Simple fallback
            
            if not hex_val:
                # Some files might not have Hex column or it's empty, skip or warn?
                # looking at file samples, Hex seems present.
                pass

            # Extract RGB
            r = row_data.get("R", "0")
            g = row_data.get("G", "0")
            b = row_data.get("B", "0")
            
            try:
                rgb = {"r": int(r), "g": int(g), "b": int(b)}
            except ValueError:
                rgb = {"r": 0, "g": 0, "b": 0}

            # Product Code
            code = row_data.get("Code", "")
            
            # Set (formerly Range)
            paint_set = row_data.get("Set", "")
            
            paint_name = row_data.get("Name", "")
            
            if paint_name and hex_val:
                paints.append({
                    "name": paint_name,
                    "product_code": code,
                    "set": paint_set,
                    "color_hex": hex_val
                })

    return {
        "brand": brand_name,
        "logo": logo_path,
        "paints": paints
    }

def slugify(text):
    return re.sub(r'[\W_]+', '-', text.lower()).strip('-')

def migrate():
    if not ASSETS_DIR.exists():
        print(f"Directory not found: {ASSETS_DIR}")
        return

    for md_file in ASSETS_DIR.glob("*.md"):
        print(f"Processing {md_file.name}...")
        data = parse_markdown_file(md_file)
        
        if not data["brand"]:
            print(f"Skipping {md_file.name}: No brand found")
            continue

        brand_slug = slugify(data["brand"])
        
        # Upsert Brand
        brand_payload = {
            "name": data["brand"],
            "slug": brand_slug,
            "logo_path": data["logo"]
        }
        
        # Check if brand exists
        res = supabase.table("paint_brands").select("id").eq("slug", brand_slug).execute()
        if res.data:
            brand_id = res.data[0]['id']
            # UPDATE logo path
            print(f"Updating Brand: {data['brand']}")
            supabase.table("paint_brands").update(brand_payload).eq("id", brand_id).execute()
        else:
            res = supabase.table("paint_brands").insert(brand_payload).execute()
            brand_id = res.data[0]['id']
            print(f"Created Brand: {data['brand']}")

        if not data["paints"]:
            continue

        paints_to_insert = []
        for p in data["paints"]:
            set_name = p["set"]
            set_id = None
            
            if set_name:
                # Upsert Set
                # Check if set exists
                res_set = supabase.table("paint_sets").select("id").eq("brand_id", brand_id).eq("name", set_name).execute()
                if res_set.data:
                    set_id = res_set.data[0]['id']
                else:
                    res_set_ins = supabase.table("paint_sets").insert({"brand_id": brand_id, "name": set_name}).execute()
                    if res_set_ins.data:
                        set_id = res_set_ins.data[0]['id']

            paints_to_insert.append({
                "brand_id": brand_id,
                # "brand": data["brand"],  # REQUSTED REMOVAL
                "name": p["name"],
                "product_code": p["product_code"],
                "paint_set_id": set_id,
                "color_hex": p["color_hex"]
                # Removed color_rgb
            })
        
        # DELETE existing paints for this brand to perform a clean sync
        supabase.table("catalog_paints").delete().eq("brand_id", brand_id).execute()
        
        # Insert new
        count = 0
        chunk_size = 100
        for i in range(0, len(paints_to_insert), chunk_size):
            chunk = paints_to_insert[i:i + chunk_size]
            try:
                supabase.table("catalog_paints").insert(chunk).execute()
                count += len(chunk)
            except Exception as e:
                print(f"Error inserting chunk: {e}")
            
        print(f"Synced {count} paints for {data['brand']}")

if __name__ == "__main__":
    migrate()

import requests

file_id = "1FAiw3OGxkSxzuiTi2hXMVYdtM96TBtPu"
url = f"https://drive.google.com/uc?export=view&id={file_id}"

print(f"Testing URL: {url}")

try:
    resp = requests.get(url, allow_redirects=True)
    print(f"Status Code: {resp.status_code}")
    print(f"Headers: {resp.headers}")
    if resp.status_code == 200:
        print("✅ SUCCESS: File is public")
    else:
        print("❌ FAILURE: File is private or blocked")
        print(resp.text[:500])
except Exception as e:
    print(f"Error: {e}")

import httpx
from fastapi import Response, APIRouter

async def proxy_google_drive_image(file_id: str):
    """
    Proxies image requests to Google Drive to bypass referrer policies.
    """
    if not file_id:
        return Response(status_code=400)
        
    url = f"https://drive.google.com/uc?export=view&id={file_id}"
    
    try:
        async with httpx.AsyncClient() as client:
            # Fetch from Google Drive
            # We follow redirects because the download URL usually redirects to actual content
            resp = await client.get(url, follow_redirects=True)
            
            if resp.status_code != 200:
                print(f"Failed to fetch image {file_id}: {resp.status_code}")
                return Response(status_code=resp.status_code)
            
            # Forward the content and correct content-type
            return Response(
                content=resp.content,
                media_type=resp.headers.get("content-type", "image/jpeg"),
                headers={
                    "Cache-Control": "public, max-age=31536000" # Cache for 1 year
                }
            )
            
    except Exception as e:
        print(f"Proxy error for {file_id}: {e}")
        return Response(status_code=500)

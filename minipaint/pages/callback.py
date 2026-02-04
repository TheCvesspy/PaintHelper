import reflex as rx
from ..state import BaseState
from ..services.supabase import supabase
from ..services import drive_service

class CallbackState(BaseState):
    
    async def handle_callback(self):
        # Authenticate user first
        await self.check_auth()
        if not self.user:
            yield rx.redirect("/login")
            
        # Get code from query params
        # args = self.router.query  # Failed: no attribute 'query'
        # Parse from self.router.url as recommended by deprecation warning
        import urllib.parse
        parsed_url = urllib.parse.urlparse(str(self.router.url))
        query_params = urllib.parse.parse_qs(parsed_url.query)
        code = query_params.get("code", [None])[0]
        
        if not code:
            yield rx.toast("Error: No code received from Google.")
            
        try:
            # Exchange code
            # We need the redirect_uri used (must match what was sent)
            # For local dev: http://localhost:3000/callback
            # We need to know the base URL. For now assume localhost:3000 or derive from request?
            # Reflex usually runs on localhost:3000
            redirect_uri = "http://localhost:3000/callback" 
            
            tokens = drive_service.exchange_code(code, redirect_uri)
            refresh_token = tokens.get("refresh_token")
            access_token = tokens.get("access_token")
            
            if not refresh_token:
                # If user re-auths without prompt=consent, functionality might be limited if we didn't store it before
                # But for MVP assume we got it.
                pass

            # Store in Supabase
            user_id = self.user.get("id")
            
            # Check if settings exist
            existing = supabase.table("user_settings").select("*").eq("user_id", user_id).execute()
            
            data = {
                "user_id": user_id,
                "drive_refresh_token": refresh_token, # Note: Should be encrypted in prod
                # We can also store access_token but it expires. Refresh token is key.
            }
            
            # Initialize Drive to create folder
            service = drive_service.get_drive_service(access_token)
            # Check for folder or create logic can go here. 
            # For now, just save.
            
            if existing.data:
                supabase.table("user_settings").update(data).eq("user_id", user_id).execute()
            else:
                supabase.table("user_settings").insert(data).execute()
                
            yield rx.redirect("/dashboard")
            
        except Exception as e:
            yield rx.toast(f"Auth Error: {str(e)}")

def callback_page():
    return rx.center(
        rx.vstack(
            rx.spinner(),
            rx.text("Connecting to Google Drive..."),
        ),
        height="100vh",
        on_mount=CallbackState.handle_callback
    )

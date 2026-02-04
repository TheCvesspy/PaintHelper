import reflex as rx
from ..services import drive_service
from ..services.supabase import supabase


class SettingsState(rx.State):
    """State for user settings and integrations"""
    
    is_drive_connected: bool = False
    
    async def check_drive_connection(self):
        """Check if user has connected Google Drive"""
        # Access parent state to get user info
        parent = await self.get_state(type(self).__bases__[0])
        if not hasattr(parent, 'user') or not parent.user:
            return
        
        try:
            res = supabase.table("user_settings").select("drive_refresh_token").eq(
                "user_id", parent.user.get("id")
            ).execute()
            
            if res.data and res.data[0].get("drive_refresh_token"):
                self.is_drive_connected = True
            else:
                self.is_drive_connected = False
        except Exception as e:
            print(f"Error checking drive connection: {e}")
            self.is_drive_connected = False
    
    def connect_drive(self):
        """Redirect to Google Drive OAuth"""
        url = drive_service.get_auth_url("http://localhost:3000/callback")
        return rx.redirect(url)
    
    async def disconnect_drive(self):
        """Disconnect Google Drive integration"""
        parent = await self.get_state(type(self).__bases__[0])
        if not hasattr(parent, 'user') or not parent.user:
            return
        
        try:
            # Clear tokens from DB
            supabase.table("user_settings").update({
                "drive_refresh_token": None,
                "drive_folder_id": None
            }).eq("user_id", parent.user.get("id")).execute()
            
            self.is_drive_connected = False
            yield rx.toast("❌ Disconnected from Google Drive")
        except Exception as e:
            yield rx.toast(f"Error disconnecting: {e}")

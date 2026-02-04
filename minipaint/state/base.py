import reflex as rx
import os
import json
from ..services.supabase import supabase


def get_admin_emails():
    """Helper to load admin emails dynamically."""
    admin_config_path = "admin_config.json"
    emails = []
    
    # 1. Try Config File
    if os.path.exists(admin_config_path):
        try:
            with open(admin_config_path, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception as e:
            print(f"Error reading admin config: {e}")
            
    # 2. Fallback to Env List
    if not emails:
        env_list_str = os.environ.get("ADMIN_EMAILS", "[]")
        try:
            env_list = json.loads(env_list_str)
            if isinstance(env_list, list):
                emails = env_list
        except: pass
        
    # 3. Fallback to Single Env
    if not emails:
         single = os.environ.get("ADMIN_EMAIL")
         if single:
             emails = [single]
             
    return emails

class BaseState(rx.State):
    user: dict = {}
    
    async def check_auth(self):
        """Check if user is authenticated via Supabase."""
        # In a real app, we might check an access token stored in local storage
        # and validate it with Supabase.
        # For this MVP, we will assume the session is handled via 'on_load' checks 
        # or we will implement a simple session restoration if possible.
        session = supabase.auth.get_session()
        if session:
            self.user = session.user.__dict__ # specific to supabase return type
            
            # Check if user is banned
            try:
                # Use supabase_admin if available to ensure we can read the ban list regardless of policies (though we set public read)
                # Fallback to standard client
                client = supabase
                # Import here to avoid circular dependency if needed, or rely on global import
                from ..services.supabase import supabase_admin
                if supabase_admin:
                    client = supabase_admin
                    
                res = client.table("banned_users").select("reason").eq("email", self.user.get("email")).execute()
                if res.data:
                    # User is banned
                    print(f"User {self.user.get('email')} is banned. Reason: {res.data[0]['reason']}")
                    return self.logout()
            except Exception as e:
                print(f"Error checking ban status: {e}")
        else:
            self.user = {}

    @rx.var
    def is_authenticated(self) -> bool:
        return bool(self.user)

    @rx.var
    def is_admin(self) -> bool:
        """Check if the current user is an admin."""
        if not self.user or "email" not in self.user:
            return False
        
        # Reload admins dynamically to allow runtime config changes
        current_admins = get_admin_emails()
        return self.user["email"] in current_admins
        
    def logout(self):
        supabase.auth.sign_out()
        self.user = {}
        return rx.redirect("/")

import reflex as rx
from ..services.supabase import supabase, supabase_admin
from ..state import BaseState 
import asyncio

# Note: We need a BaseState or similar. For now, inheriting from rx.State.
# Actually, let's create a minimal state here or import.

class RegistrationState(BaseState):
    email: str = ""
    password: str = ""
    invite_token: str = ""
    error_msg: str = ""
    success_msg: str = ""
    is_loading: bool = False

    def set_email(self, val):
        self.email = val

    def set_password(self, val):
        self.password = val

    def set_invite_token(self, val):
        self.invite_token = val

    async def register(self):
        self.is_loading = True
        self.error_msg = ""
        self.success_msg = ""
        yield
        
        # 1. Validate Input
        if not self.email or not self.password or not self.invite_token:
            self.error_msg = "Please fill in all fields."
            self.is_loading = False
            return

        # 2. Validate Token (Server-side check)
        # We need supabase_admin to check the token if RLS blocks public read
        if not supabase_admin:
            self.error_msg = "Server configuration error (Service Key missing)."
            self.is_loading = False
            return

        try:
            # Check if token exists and is active
            res = supabase_admin.table("access_tokens").select("*").eq("token_code", self.invite_token).eq("status", "active").execute()
            
            if not res.data:
                self.error_msg = "Invalid or expired Invite Token."
                self.is_loading = False
                return
            
            token_record = res.data[0]
            
            # 3. Register User
            # Supabase Auth sign_up
            auth_res = supabase.auth.sign_up({"email": self.email, "password": self.password})
            
            if auth_res.user:
                # 4. Consume Token
                # Mark token as used
                supabase_admin.table("access_tokens").update({
                    "status": "used",
                    "used_at": "now()",
                    "used_by_email": self.email
                }).eq("id", token_record['id']).execute()
                
                self.success_msg = "Registration successful! Redirecting..."
                yield
                await asyncio.sleep(1)
                yield rx.redirect("/login")
            else:
                 # Check if session is missing (confirmation required?)
                 if auth_res.session is None and auth_res.user is not None:
                     self.success_msg = "Registration successful! Please check your email to confirm."
                 else:
                    self.error_msg = "Registration failed."
        except Exception as e:
            self.error_msg = f"An error occurred: {str(e)}"
        
        self.is_loading = False

def registration_page():
    return rx.center(
        rx.vstack(
            rx.image(src="/quills_hub_logo.png", width="100%", height="auto", border_radius="10px 10px 0 0"),
            rx.vstack(
                rx.heading("Join Quill's Hub", size="9", font_family="Pirata One"),
                rx.text("Enter your invite token to get started.", color="gray"),
                rx.box(height="10px"),
                
                rx.vstack(
                    rx.text("Email", size="5", weight="medium", width="100%", font_family="Pirata One"),
                    rx.input(
                        placeholder="Email", 
                        on_blur=RegistrationState.set_email,
                        width="100%"
                    ),
                    spacing="1", width="100%"
                ),
                rx.vstack(
                    rx.text("Password", size="5", weight="medium", width="100%", font_family="Pirata One"),
                    rx.input(
                        placeholder="Password", 
                        type="password", 
                        on_blur=RegistrationState.set_password,
                        width="100%"
                    ),
                    spacing="1", width="100%"
                ),
                rx.vstack(
                    rx.text("Invite Token", size="5", weight="medium", width="100%", font_family="Pirata One"),
                    rx.input(
                        placeholder="Invite Token (UUID)", 
                        on_blur=RegistrationState.set_invite_token,
                        width="100%"
                    ),
                    spacing="1", width="100%"
                ),
                
                rx.cond(
                    RegistrationState.error_msg,
                    rx.callout.root(
                        rx.callout.icon(),
                        rx.callout.text(RegistrationState.error_msg),
                        color_scheme="red",
                        width="100%"
                    ),
                ),
                rx.cond(
                    RegistrationState.success_msg,
                    rx.callout.root(
                        rx.callout.icon(),
                        rx.callout.text(RegistrationState.success_msg),
                        color_scheme="green",
                        width="100%"
                    ),
                ),
                
                rx.button(
                    "Sign Up", 
                    on_click=RegistrationState.register,
                    loading=RegistrationState.is_loading,
                    width="100%",
                    size="3",
                    margin_top="4"
                ),
                
                rx.link("Back to Login", href="/login", size="2", margin_top="1em"),
                
                width="100%",
                padding="2em",
                align_items="center",
                spacing="4"
            ),
            
            width="400px",
            border="1px solid #eaeaea",
            border_radius="10px",
            bg="white",
            spacing="0"
        ),
        height="100vh",
        bg="#f5f5f5"
    )

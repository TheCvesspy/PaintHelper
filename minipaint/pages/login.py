import reflex as rx
from ..services.supabase import supabase
import asyncio

class LoginState(rx.State):
    email: str = ""
    password: str = ""
    error_msg: str = ""
    is_loading: bool = False

    def set_email(self, val):
        self.email = val

    def set_password(self, val):
        self.password = val

    async def login(self):
        self.is_loading = True
        self.error_msg = ""
        yield
        
        try:
            res = supabase.auth.sign_in_with_password({"email": self.email, "password": self.password})
            if res.user:
                self.is_loading = False
                yield rx.redirect("/dashboard")
            else:
                self.error_msg = "Login failed."
        except Exception as e:
            self.error_msg = f"Error: {str(e)}"
        
        self.is_loading = False

def login_page():
    return rx.center(
        rx.vstack(
            rx.image(src="/quills_hub_logo.png", width="100%", height="auto", border_radius="12px 12px 0 0"),
            rx.vstack(
                rx.heading("Quill's Hub", size="9", margin_bottom="0.5em", font_family="Pirata One"),
                rx.text("Sign in to your account", color="gray", margin_bottom="1.5em", size="2"),
                
                rx.vstack(
                    rx.text("Email", size="5", weight="medium", width="100%", font_family="Pirata One"),
                    rx.input(placeholder="Enter your email", on_blur=LoginState.set_email, width="100%", variant="surface"),
                    spacing="1",
                    width="100%"
                ),
                
                rx.vstack(
                    rx.text("Password", size="5", weight="medium", width="100%", font_family="Pirata One"),
                    rx.input(placeholder="Enter your password", type="password", on_blur=LoginState.set_password, width="100%", variant="surface"),
                    spacing="1",
                    width="100%"
                ),

                rx.cond(
                    LoginState.error_msg,
                    rx.callout.root(
                        rx.callout.icon(),
                        rx.callout.text(LoginState.error_msg),
                        color_scheme="red",
                        width="100%"
                    ),
                ),
                
                rx.button("Sign In", on_click=LoginState.login, loading=LoginState.is_loading, width="100%", size="3", margin_top="1em"),
                
                rx.hstack(
                    rx.text("Not a member yet?", size="3", color="gray"),
                    rx.link("Register", href="/register", size="3", color_scheme="violet", weight="bold"),
                    spacing="1",
                    margin_top="1em"
                ),
                width="100%",
                padding="2em",
                align_items="center"
            ),
            
            width="100%",
            max_width="400px",
            border=f"1px solid {rx.color('mauve', 4)}",
            border_radius="12px",
            background=rx.color("mauve", 2),
            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
            align_items="center",
            spacing="0"
        ),
        height="100vh",
        background=rx.color("mauve", 1),
        padding="1em"
    )

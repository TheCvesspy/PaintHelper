import reflex as rx
import os
from ..state import BaseState
from ..services.supabase import supabase_admin

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")

class AdminState(BaseState):
    tokens: list[dict] = []
    
    async def check_access(self):
        """Run on page mount to ensure admin access."""
        # await self.check_auth() # Ensure user is loaded
        print(f"DEBUG: AdminState.check_access called. User: {self.user}")
        
        # Use central admin check
        if not self.is_admin:
             return rx.redirect("/")
        
        await self.fetch_tokens()

    banned_users: list[dict] = []
    ban_email: str = ""
    ban_reason: str = ""

    def set_ban_email(self, val):
        self.ban_email = val

    def set_ban_reason(self, val):
        self.ban_reason = val

    async def fetch_tokens(self):
        if not supabase_admin: return
        res = supabase_admin.table("access_tokens").select("*").order("created_at", desc=True).execute()
        self.tokens = res.data

    async def generate_token(self):
        if not supabase_admin: return
        res = supabase_admin.table("access_tokens").insert({}).execute()
        if res.data:
            self.tokens.insert(0, res.data[0]) 

    async def revoke_token(self, token_id):
        if not supabase_admin: return
        supabase_admin.table("access_tokens").update({"status": "revoked"}).eq("id", token_id).execute()
        await self.fetch_tokens()

    async def fetch_banned_users(self):
        if not supabase_admin: return
        try:
            res = supabase_admin.table("banned_users").select("*").order("banned_at", desc=True).execute()
            self.banned_users = res.data
        except Exception as e:
            print(f"Error fetching banned users (table might be missing): {e}")
            # Optional: yield rx.toast("Could not fetch banned users. Run migration.")

    async def ban_user(self):
        if not self.ban_email or not supabase_admin: return
        
        # 1. Insert into banned_users
        try:
            supabase_admin.table("banned_users").insert({
                "email": self.ban_email,
                "reason": self.ban_reason,
                "banned_by": self.user.get("id")
            }).execute()
            
            # 2. To strictly enforce immediate lockout, we could invalidate sessions, 
            # but standard auth check on page load handles it reasonably well for this scope.
            
            self.ban_email = ""
            self.ban_reason = ""
            await self.fetch_banned_users()
            yield rx.toast(f"User {self.ban_email} banned.")
        except Exception as e:
            yield rx.toast(f"Error banning user: {str(e)}")

    async def unban_user(self, user_id):
        if not supabase_admin: return
        supabase_admin.table("banned_users").delete().eq("id", user_id).execute()
        await self.fetch_banned_users()


def render_admin_view():
    return rx.vstack(
        rx.heading("Admin Dashboard", size="8"),
        rx.text(f"Logged in as: {ADMIN_EMAIL}", color="gray"),
        rx.divider(),
        
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("Access Tokens", value="tokens"),
                rx.tabs.trigger("User Management", value="users"),
            ),
            rx.tabs.content(
                rx.vstack(
                    rx.hstack(
                        rx.button("Generate New Token", on_click=AdminState.generate_token, color_scheme="blue"),
                        rx.button("Refresh List", on_click=AdminState.fetch_tokens, variant="outline"),
                        spacing="4"
                    ),
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Token UUID"),
                                rx.table.column_header_cell("Status"),
                                rx.table.column_header_cell("Used By"),
                                rx.table.column_header_cell("Created At"),
                                rx.table.column_header_cell("Actions"),
                            )
                        ),
                        rx.table.body(
                            rx.foreach(
                                AdminState.tokens,
                                lambda token: rx.table.row(
                                    rx.table.cell(token["token_code"]),
                                    rx.table.cell(
                                        rx.badge(token["status"], color_scheme=rx.cond(token["status"] == "active", "green", "gray"))
                                    ),
                                    rx.table.cell(token["used_by_email"]),
                                    rx.table.cell(token["created_at"]),
                                    rx.table.cell(
                                        rx.cond(
                                            token["status"] == "active",
                                            rx.button("Revoke", size="1", color_scheme="red", variant="soft", 
                                                    on_click=lambda: AdminState.revoke_token(token["id"])),
                                            rx.text("-")
                                        )
                                    ),
                                )
                            )
                        ),
                        width="100%"
                    ),
                    spacing="4",
                    width="100%"
                ),
                value="tokens",
                width="100%"
            ),
            rx.tabs.content(
                rx.vstack(
                    rx.heading("Banned Users", size="5"),
                    rx.hstack(
                        rx.input(placeholder="Email to ban", value=AdminState.ban_email, on_change=AdminState.set_ban_email),
                        rx.input(placeholder="Reason", value=AdminState.ban_reason, on_change=AdminState.set_ban_reason),
                        rx.button("Ban User", on_click=AdminState.ban_user, color_scheme="red"),
                        align_items="center"
                    ),
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell("Email"),
                                rx.table.column_header_cell("Reason"),
                                rx.table.column_header_cell("Banned At"),
                                rx.table.column_header_cell("Actions"),
                            )
                        ),
                        rx.table.body(
                            rx.foreach(
                                AdminState.banned_users,
                                lambda u: rx.table.row(
                                    rx.table.cell(u["email"]),
                                    rx.table.cell(u["reason"]),
                                    rx.table.cell(u["banned_at"]),
                                    rx.table.cell(
                                        rx.button("Unban", size="1", variant="outline", 
                                                on_click=lambda: AdminState.unban_user(u["id"]))
                                    ),
                                )
                            )
                        ),
                        width="100%"
                    ),
                    spacing="4",
                    width="100%"
                ),
                value="users",
                width="100%"
            ),
            defaultValue="tokens",
            width="100%"
        ),
        
        spacing="6",
        padding="2em",
        width="100%",
        on_mount=[AdminState.fetch_tokens, AdminState.fetch_banned_users]
    )

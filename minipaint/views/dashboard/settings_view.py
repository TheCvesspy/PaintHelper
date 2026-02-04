import reflex as rx


def render_settings_view():
    """User settings and integrations view"""
    # Import dependencies locally to avoid circular imports
    from ...pages.dashboard import DashboardState
    
    return rx.vstack(
        rx.heading("User Settings", size="5"),
        rx.divider(),
        
        # Drive Integration
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.icon("hard-drive", size=24),
                    rx.heading("Google Drive Integration", size="4"),
                    rx.spacer(),
                    rx.cond(
                        DashboardState.is_drive_connected,
                        rx.badge("Connected", color_scheme="green", variant="solid"),
                        rx.badge("Not Connected", color_scheme="gray", variant="solid")
                    ),
                    width="100%",
                    align_items="center"
                ),
                rx.text("Connect your Google Drive to upload and manage reference images for your painting guides.", color="gray", size="2"),
                rx.cond(
                    DashboardState.is_drive_connected,
                    rx.button("Disconnect Drive", on_click=DashboardState.disconnect_drive, color_scheme="red", variant="outline"),
                    rx.button("Connect Google Drive", on_click=DashboardState.connect_drive, variant="solid")
                ),
                spacing="4",
                width="100%"
            ),
            width="100%",
            max_width="600px"
        ),
        
        width="100%",
        spacing="4"
    )

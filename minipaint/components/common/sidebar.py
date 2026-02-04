import reflex as rx
from ...styles import THEME_COLORS


def sidebar_item(text: str, icon: str, tab: str, state_class):
    """Renders a primary sidebar navigation item"""
    active = state_class.active_tab == tab
    return rx.button(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text, weight="medium", font_family="Pirata One", size="6"),
            spacing="3",
            align_items="center",
            width="100%"
        ),
        variant="ghost",
        color_scheme=rx.cond(active, "violet", "gray"),
        bg=rx.cond(active, rx.color("violet", 3), "transparent"),
        width="100%",
        justify_content="start",
        padding="12px",
        on_click=lambda: state_class.set_active_tab(tab)
    )


def sidebar_sub_item(text: str, tab: str, state_class):
    """Renders a sub-menu item for nested navigation"""
    active = state_class.active_tab == tab
    return rx.button(
        rx.text(text, size="4", font_family="Pirata One"),
        variant="ghost",
        color_scheme=rx.cond(active, "violet", "gray"),
        bg=rx.cond(active, rx.color("violet", 3), "transparent"),
        width="88%",  # Significantly reduced width
        min_width="0",
        border_radius="0 8px 8px 0",  # Rounded right edge
        justify_content="start",
        padding_left="2.5em",
        padding_y="8px",
        on_click=lambda: state_class.set_active_tab(tab)
    )


def sidebar(state_class):
    """Main sidebar navigation component"""
    return rx.vstack(
        # Logo Banner
        rx.box(
            rx.image(src="/quills_hub_logo.png", width="100%", height="auto", border_radius="0"),
            width="100%",
            padding="0",
            margin_bottom="1em"
        ),
        
        # Nav
        rx.vstack(
            sidebar_item("Printing", "printer", "print_jobs", state_class),
            
            # Paints section with sub-items
            rx.vstack(
                sidebar_item("Paints", "palette", "paints_owned", state_class),
                sidebar_sub_item("Owned", "paints_owned", state_class),
                sidebar_sub_item("Library", "paints_library", state_class),
                sidebar_sub_item("Shopping List", "paints_wishlist", state_class),
                spacing="0",
                width="100%"
            ),

            sidebar_item("Painting Guides", "book-open", "painting_guides", state_class),
            
            # Admin Link (Conditional)
            rx.cond(
                state_class.is_admin,
                sidebar_item("Admin", "shield-check", "admin", state_class),
            ),
            
            spacing="1",
            width="100%",
            padding_x="1em"
        ),
        
        rx.spacer(),
        
        # User Profile
        rx.vstack(
            rx.divider(),
            rx.hstack(
                rx.avatar(fallback="U", size="2"),
                rx.vstack(
                    rx.text(state_class.user["email"], size="1", weight="bold"),
                    spacing="0",
                    align_items="start"
                ),
                rx.spacer(),
                rx.hstack(
                    rx.button(
                        rx.icon("settings", size=16), 
                        variant="ghost", 
                        color_scheme="gray", 
                        on_click=lambda: state_class.set_active_tab("settings"), 
                        size="2"
                    ),
                    rx.button(
                        rx.icon("log-out", size=16), 
                        variant="ghost", 
                        color_scheme="gray", 
                        on_click=state_class.logout, 
                        size="2"
                    ),
                    spacing="1"
                ),
                width="100%",
                align_items="center",
                padding="1em"
            ),
            width="100%",
            spacing="0"
        ),
        
        height="100vh",
        width="260px",
        border_right=f"1px solid {rx.color('mauve', 4)}",
        bg=rx.color_mode_cond(
            light=THEME_COLORS["light"]["surface"], 
            dark=THEME_COLORS["dark"]["surface"]
        ),
    )

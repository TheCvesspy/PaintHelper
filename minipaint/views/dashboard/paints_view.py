import reflex as rx


def paints_tab():
    """Paints library, owned, and wishlist views"""
    # Import dependencies locally to avoid circular imports
    from ...pages.dashboard import DashboardState, render_create_custom_modal, render_owned_view, render_library_view, render_wishlist_view
    
    return rx.vstack(
        render_create_custom_modal(),
        
        # Conditional heading based on active tab
        rx.cond(
            DashboardState.active_tab == "paints_library",
            rx.heading("Paint Library", size="5"),
            rx.cond(
                DashboardState.active_tab == "paints_owned",
                rx.heading("Owned Paints", size="5"),
                rx.heading("Shopping List", size="5")
            )
        ),
        
        rx.divider(),
        
        # Conditional view based on active tab
        rx.cond(
            DashboardState.active_tab == "paints_owned",
            render_owned_view(),
            rx.cond(
                DashboardState.active_tab == "paints_library",
                render_library_view(),
                render_wishlist_view()
            )
        ),
        
        width="100%",
        spacing="4",
        align_items="start"
    )

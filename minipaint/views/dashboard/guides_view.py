import reflex as rx


def painting_guides_tab():
    """Painting guides list and management view"""
    # Import dependencies locally to avoid circular imports  
    from ...pages.dashboard import DashboardState, render_create_guide_modal, render_guide_detail_modal, render_cancel_confirmation_modal, render_delete_confirmation_modal
    state_class = DashboardState
    
    return rx.vstack(
        render_create_guide_modal(),
        render_guide_detail_modal(),
        render_cancel_confirmation_modal(),
        render_delete_confirmation_modal(),
        rx.hstack(
            rx.heading("Painting Guides", size="5"),
            rx.spacer(),
            # View Toggle
            rx.tooltip(
                rx.icon_button(
                    rx.cond(
                        state_class.guide_view_mode == "grid",
                        rx.icon("table", size=16),
                        rx.icon("layout-grid", size=16)
                    ),
                    size="2",
                    variant="soft",
                    on_click=state_class.toggle_guide_view_mode
                ),
                content=rx.cond(
                    state_class.guide_view_mode == "grid",
                    "Switch to Table View",
                    "Switch to Grid View"
                )
            ),
            rx.button("New Guide", on_click=state_class.toggle_guide_modal)
        ),
        
        rx.cond(
            state_class.guide_view_mode == "grid",
            rx.grid(
                rx.foreach(
                    state_class.painting_guides,
                    lambda guide: rx.card(
                        rx.vstack(
                            rx.hstack(
                                rx.vstack(
                                    rx.text(guide.name, weight="bold", size="2", max_width="120px", overflow="hidden", text_overflow="ellipsis", white_space="nowrap"),
                                    rx.text(f"{guide.guide_details.length()} Sections", size="1", color="violet"),
                                    align_items="start",
                                    spacing="1"
                                ),
                                width="100%",
                                align_items="start"
                            ),
                            rx.divider(),
                            rx.hstack(
                                rx.tooltip(
                                    rx.button(
                                        rx.icon("pencil", size=14),
                                        on_click=lambda e: [rx.stop_propagation, state_class.open_guide_for_edit(guide)],
                                        variant="ghost",
                                        size="1",
                                        color_scheme="violet"
                                    ),
                                    content="Edit"
                                ),
                                rx.tooltip(
                                    rx.button(
                                        rx.icon("trash-2", size=14),
                                        on_click=lambda e: [rx.stop_propagation, state_class.handle_delete_click(guide.id)],
                                        variant="ghost",
                                        size="1",
                                        color_scheme="red"
                                    ),
                                    content="Delete"
                                ),
                                width="100%",
                                justify="end",
                                spacing="2"
                            ),
                            width="100%",
                            spacing="2"
                        ),
                        on_click=lambda: state_class.open_guide_detail(guide),
                        width="100%",
                        cursor="pointer",
                        _hover={"boxShadow": "lg", "border": f"1px solid {rx.color('violet', 8)}"},
                        variant="classic",
                        padding="3"
                    )
                ),
                columns=rx.breakpoints(
                    initial="1",
                    sm="2",
                    md="3",
                    lg="4",
                    xl="6",
                ),
                spacing="4",
                width="100%"
            ),
            # Table View
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Name"),
                        rx.table.column_header_cell("Type"),
                        rx.table.column_header_cell("Steps"),
                        rx.table.column_header_cell("Created"),
                        rx.table.column_header_cell("Actions"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        state_class.painting_guides,
                        lambda guide: rx.table.row(
                            rx.table.cell(rx.text(guide.name, weight="bold", color="violet")),
                            rx.table.cell(rx.text(guide.guide_type.capitalize(), size="2")),
                            rx.table.cell(rx.text(guide.guide_details.length().to_string(), size="2")),
                            rx.table.cell(rx.text(guide.created_at, size="1", color="gray")),
                            rx.table.cell(
                                rx.hstack(
                                    rx.icon_button(rx.icon("eye", size=16), size="1", variant="ghost", on_click=lambda e: [rx.stop_propagation, state_class.open_guide_detail(guide)]),
                                    rx.icon_button(rx.icon("pencil", size=16), size="1", variant="ghost", color_scheme="violet", on_click=lambda e: [rx.stop_propagation, state_class.open_guide_for_edit(guide)]),
                                    rx.icon_button(rx.icon("trash-2", size=16), size="1", variant="ghost", color_scheme="red", on_click=lambda e: [rx.stop_propagation, state_class.handle_delete_click(guide.id)]),
                                    spacing="2"
                                )
                            ),
                            on_click=lambda: state_class.open_guide_detail(guide),
                            style={"cursor": "pointer"},
                            _hover={"background_color": rx.color("gray", 3)}
                        )
                    )
                ),
                width="100%",
                variant="surface",
                size="1"
            )
        ),
        
        width="100%",
        spacing="4",
        align_items="start"
    )

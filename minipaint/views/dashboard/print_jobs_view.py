import reflex as rx


def print_jobs_tab():
    """Print jobs and batch management view"""
    # Import dependencies locally to avoid circular imports
    from ...pages.dashboard import DashboardState, render_batch
    from ...components import create_batch_modal, add_job_modal
    
    return rx.vstack(
        rx.hstack(
            rx.heading("Printing Management", size="5"),
            rx.spacer(),
            # Create Batch Trigger
            rx.button("New Batch", on_click=lambda: DashboardState.set_create_batch_modal_open(True)),
            rx.spacer(),
            rx.text("Show Archived", size="2"),
            rx.switch(on_change=DashboardState.toggle_show_archived, checked=DashboardState.show_archived),
            align_items="center",
            width="100%"
        ),
        
        # Batches List (Vertical Stack of Cards)
        rx.vstack(
            rx.foreach(DashboardState.batches, render_batch),
            width="100%",
            spacing="4"
        ),
        
        
        # Create Batch Modal
        create_batch_modal(DashboardState),

        
        # Misprint Modal
        rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Job Complete - Check for Misprints"),
                rx.dialog.description("Mark any items that failed and need reprinting."),
                rx.cond(
                    DashboardState.active_job_misprint,
                    rx.foreach(
                        DashboardState.active_job_misprint.print_job_items,
                        lambda item: rx.hstack(
                            rx.text(f"{item.name} (x{item.quantity})"),
                            rx.spacer(),
                            rx.text("Failed Qty:"),
                            rx.input(
                                type="number", 
                                placeholder="0", 
                                min=0,
                                max=item.quantity,
                                on_change=lambda val: DashboardState.set_misprint_qty(item.id, val),
                                width="60px"
                            )
                        )
                    ),
                ),
                rx.flex(
                    rx.dialog.close(
                        rx.button("Cancel", color_scheme="gray", variant="soft"),
                    ),
                    rx.dialog.close(
                        rx.button("Confirm", on_click=DashboardState.confirm_job_completion),
                    ),
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),
            ),
            open=DashboardState.misprint_modal_open,
        ),
        
        
        # Add Job Modal
        add_job_modal(DashboardState),

        
        width="100%",
        spacing="4",
        align_items="start"
    )


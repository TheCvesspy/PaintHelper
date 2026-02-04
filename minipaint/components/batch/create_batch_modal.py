import reflex as rx


def create_batch_modal(state_class):
    """Modal dialog for creating a new batch"""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Create New Batch"),
            rx.vstack(
                rx.input(
                    placeholder="Batch Name", 
                    value=state_class.new_batch_name, 
                    on_change=state_class.set_new_batch_name
                ),
                rx.text("Type:", size="1"),
                rx.select(
                    ["Resin", "FDM"], 
                    value=state_class.new_batch_tag, 
                    on_change=state_class.set_new_batch_tag
                ),
                rx.text("Due Date:", size="1"),
                rx.input(
                    type="date", 
                    value=state_class.new_batch_due_date, 
                    on_change=state_class.set_new_batch_due_date
                ),
                rx.button(
                    "Create", 
                    on_click=state_class.add_batch, 
                    width="100%"
                ),
                spacing="4"
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Cancel", color_scheme="gray", variant="soft"),
                ),
                justify="end",
                margin_top="16px"
            )
        ),
        open=state_class.create_batch_modal_open,
        on_open_change=state_class.set_create_batch_modal_open
    )

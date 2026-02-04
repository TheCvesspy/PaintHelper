import reflex as rx


def add_job_modal(state_class):
    """Modal dialog for adding/editing print jobs with staged items"""
    return rx.dialog.root(
        rx.dialog.content(
            # Header
            rx.hstack(
                rx.dialog.title(
                    rx.cond(
                        state_class.editing_job_id != "",
                        "Edit Print Job",
                        "Add New Print Job"
                    )
                ),
                rx.spacer(),
                rx.dialog.close(
                    rx.button(rx.icon("x"), variant="ghost", color_scheme="gray", size="2")
                ),
                width="100%",
                align_items="start"
            ),
            
            # Body
            rx.vstack(
                rx.hstack(
                    rx.input(
                        placeholder="Item Name", 
                        value=state_class.new_item_name, 
                        on_change=state_class.set_new_item_name
                    ),
                    rx.input(
                        type="number", 
                        placeholder="Qty", 
                        value=state_class.new_item_qty, 
                        on_change=state_class.set_new_item_qty, 
                        width="70px"
                    ),
                    rx.input(
                        placeholder="Link (Opt)", 
                        value=state_class.new_item_link, 
                        on_change=state_class.set_new_item_link
                    ),
                    rx.button(
                        rx.cond(state_class.editing_stage_item_index >= 0, "Update", "Add"),
                        on_click=state_class.add_staging_item, 
                        variant="soft"
                    ),
                ),
                rx.cond(
                    state_class.staging_job_items,
                    rx.vstack(
                        rx.text("Staged Items:", weight="bold", size="2"),
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("Name"),
                                    rx.table.column_header_cell("Qty"),
                                    rx.table.column_header_cell("Link"),
                                    rx.table.column_header_cell("Action"),
                                )
                            ),
                            rx.table.body(
                                rx.foreach(
                                    state_class.staging_job_items,
                                    lambda item, idx: rx.table.row(
                                        rx.table.cell(item["name"]),
                                        rx.table.cell(item["quantity"]),
                                        rx.table.cell(
                                            rx.cond(
                                                item["link_url"] != "",
                                                rx.icon("link", size=12),
                                                rx.text("-")
                                            )
                                        ),
                                        rx.table.cell(
                                            rx.hstack(
                                                rx.button(
                                                    rx.icon("pencil", size=14), 
                                                    size="1", 
                                                    variant="ghost",
                                                    color_scheme="blue", 
                                                    on_click=lambda: state_class.edit_staging_item(idx)
                                                ),
                                                rx.button(
                                                    rx.icon("trash-2", size=14), 
                                                    size="1", 
                                                    variant="ghost", 
                                                    color_scheme="red",
                                                    on_click=lambda: state_class.remove_staging_item(idx)
                                                ),
                                                spacing="1"
                                            )
                                        )
                                    )
                                )
                            ),
                            width="100%"
                        ),
                    )
                ),
                width="100%",
                spacing="4"
            ),
            
            # Footer
            rx.flex(
                rx.button(
                    rx.cond(
                        state_class.editing_job_id != "",
                        "Save Changes",
                        "Create Job"
                    ), 
                    on_click=state_class.add_print_job, 
                    width="150px",
                    variant="solid"
                ),
                justify="end",
                width="100%",
                margin_top="16px"
            ),
            max_width="600px",
        ),
        open=state_class.add_job_modal_open,
        on_open_change=state_class.set_add_job_modal_open
    )

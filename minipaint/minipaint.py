"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from .styles import global_style


class State(rx.State):
    """The app state."""


app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=False,
        accent_color="violet",
        gray_color="mauve",
    ),
    style=global_style,
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=Pirata+One&display=swap",
    ],
    head_components=[
        rx.el.link(rel="icon", href="/favicon.png"),
        rx.el.title("Quills Hub"),
    ],
)

# from .api import proxy_google_drive_image
# # Register custom API route for image proxying
# if hasattr(app, "_api"):
#    # app._api.add_route("/api/image_proxy/{file_id}", proxy_google_drive_image, methods=["GET"])
#    pass

from .pages.registration import registration_page
# from .pages.admin import admin_page
from .pages.login import login_page
from .pages.dashboard import dashboard_page
from .pages.callback import callback_page

app.add_page(login_page, route="/", title="Quills Hub")
app.add_page(registration_page, route="/register", title="Quills Hub | Register")
app.add_page(login_page, route="/login", title="Quills Hub")
# app.add_page(admin_page, route="/admin", title="Quills Hub | Admin")
app.add_page(dashboard_page, route="/dashboard", title="Quills Hub | Dashboard")
app.add_page(callback_page, route="/callback")

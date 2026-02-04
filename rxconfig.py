import reflex as rx

config = rx.Config(
    app_name="minipaint",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)
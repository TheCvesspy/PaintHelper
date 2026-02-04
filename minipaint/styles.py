import reflex as rx

# Deep Nebula Theme
# Primary: #2E1A47 (Deep Purple) / #7F5AB5 (Lighter Purple)
# Background: #F3F0F7 (Light Lavender) / #121212 (Dark Grey)
# Surface: #FFFFFF (White) / #2E1A47 (Deep Purple - Primary)
# Accent: #5B3C88 (Medium Purple) / #D8B4FE (Lavender)

THEME_COLORS = {
    "light": {
        "primary": "#2E1A47",
        "background": "#F3F0F7",
        "surface": "#FFFFFF",
        "accent": "#5B3C88",
        "text_main": "#0F0818",
        "text_muted": "#5D526E",
    },
    "dark": {
        "primary": "#7F5AB5",
        "background": "#121212",
        "surface": "#2E1A47", # Custom request: Primary usage for Surface in Dark mode
        "accent": "#D8B4FE",
        "text_main": "#FFFFFF",
        "text_muted": "#A69BB5",
    }
}

global_style = {
    "body": {
        "background": THEME_COLORS["light"]["background"],
        "color": THEME_COLORS["light"]["text_main"],
        "_dark": {
             "background": THEME_COLORS["dark"]["background"],
             "color": THEME_COLORS["dark"]["text_main"],
        }
    }
}

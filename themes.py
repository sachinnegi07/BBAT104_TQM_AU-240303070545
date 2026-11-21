
import customtkinter as ctk


THEME_COLORS = {
    "Blue": {
        "primary": "#1F6AA5",
        "hover": "#144870",
    },
    "Green": {
        "primary": "#23865B",
        "hover": "#17623F",
    },
    "Purple": {
        "primary": "#7047B9",
        "hover": "#52338A",
    },
}


def apply_accent_theme(root, theme_name):
    """Apply selected accent colors to existing UI widgets."""

    if theme_name not in THEME_COLORS:
        raise ValueError("Invalid theme selected.")

    colors = THEME_COLORS[theme_name]

    def update_widget(widget):

        if isinstance(widget, ctk.CTkButton):
            widget.configure(
                fg_color=colors["primary"],
                hover_color=colors["hover"]
            )

        elif isinstance(widget, ctk.CTkOptionMenu):
            widget.configure(
                fg_color=colors["primary"],
                button_color=colors["primary"],
                button_hover_color=colors["hover"]
            )

        for child in widget.winfo_children():
            update_widget(child)

    update_widget(root)

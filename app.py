
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Hostel Management System | BBAT104")
app.geometry("900x600")
app.minsize(700, 450)

heading = ctk.CTkLabel(
    app,
    text="Hostel Management System",
    font=ctk.CTkFont(size=28, weight="bold")
)
heading.pack(pady=(70, 15))

subtitle = ctk.CTkLabel(
    app,
    text="BBAT104 | Q03 - Improve Usability",
    font=ctk.CTkFont(size=16)
)
subtitle.pack(pady=10)

ctk.CTkLabel(
    app,
    text="Choose Appearance Mode"
).pack(pady=(40, 10))

appearance_menu = ctk.CTkOptionMenu(
    app,
    values=["System", "Light", "Dark"],
    command=ctk.set_appearance_mode
)
appearance_menu.set("System")
appearance_menu.pack(pady=10)

app.mainloop()

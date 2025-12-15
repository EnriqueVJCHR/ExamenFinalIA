import flet as ft

# Colores del Tema Neon
NEON_CYAN = "#00F3FF"
NEON_PINK = "#FF00FF"
NEON_GREEN = "#39FF14"
DARK_BG = "#0f0f0f"
GLASS_BG = "#1a1a1a"

# Estilos de Texto
TITLE_STYLE = ft.TextStyle(size=30, weight=ft.FontWeight.BOLD, color=NEON_CYAN, font_family="Consolas")
SUBTITLE_STYLE = ft.TextStyle(size=18, color="white", font_family="Roboto")

def get_neon_container(content, padding=20):
    return ft.Container(
        content=content,
        bgcolor=GLASS_BG,
        border=ft.border.all(2, NEON_CYAN),
        border_radius=15,
        padding=padding,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=NEON_CYAN,
            offset=ft.Offset(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER,
        ),
    )

def get_neon_button(text, on_click, color=NEON_CYAN):
    return ft.ElevatedButton(
        text=text,
        style=ft.ButtonStyle(
            color=DARK_BG,
            bgcolor=color,
            text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
            shape=ft.RoundedRectangleBorder(radius=8),
            elevation=10,
        ),
        on_click=on_click,
        width=200,
        height=50
    )

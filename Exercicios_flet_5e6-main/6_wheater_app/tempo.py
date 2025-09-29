import flet as ft
import httpx
from datetime import datetime

API_KEY = "05f4ee67848cc2f2685db6e4c1cf5f3e"

# ===================== ESQUEMAS DE COR =====================

light_color_scheme = ft.ColorScheme(
    primary=ft.Colors.BLUE,
    on_primary=ft.Colors.WHITE,
    background=ft.Colors.WHITE,
    on_background= ft.Colors.BLACK,
    surface=ft.Colors.WHITE,
    on_surface=ft.Colors.BLACK,
)

dark_color_scheme = ft.ColorScheme(
    primary=ft.Colors.BLUE_700,
    on_primary = ft.Colors.WHITE,
    background=ft.Colors.BLACK,
    on_background=ft.Colors.WHITE,
    surface=ft.Colors.BLACK,
    on_surface=ft.Colors.WHITE,
)

light_theme = ft.Theme(color_scheme=light_color_scheme)
dark_theme = ft.Theme(color_scheme=dark_color_scheme)

def get_icon(Icon_code):
    icon_map = {
        "01d": ft.Icons.SUNNY, "01n": ft.Icons.NIGHTLIGHT,
        "02d": ft.Icons.CLOUD, "02n": ft.Icons.CLOUD,
        "03d": ft.Icons.CLOUD, "03n": ft.Icons.CLOUD,
        "04d": ft.Icons.CLOUD, "04n": ft.Icons.CLOUD,
        "09d": ft.Icons.WATER_DROP, "09n": ft.Icons.WATER_DROP,
        "10d": ft.Icons.WATER_DROP, "010n": ft.Icons.WATER_DROP,
        "11d": ft.Icons.FLASH_ON, "011n": ft.Icons.FLASH_ON,
        "13d": ft.Icons.AC_UNIT, "13n": ft.Icons.AC_UNIT,
        "50d": ft.Icons.VISIBILITY, "50n": ft.Icons.VISIBILITY
    }
    return icon_map.get(Icon_code, ft.Icons.QUESTION_MARK)

def translate_weekday(weekday):
    translations = {
        "Mon":"Seg", "Tue" : "Ter", "Wed" : "Qua", "thu": "Qui", "Fri" : "Sex", "Sat" : "Sab", "Sun" : "Dom"
    }
    return translations.get(weekday, weekday)

async def get_weather(city, country):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": f"{city}, {country}",
        "units" : "Metric",
        "lang" : "pt_br"
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
    return resp.json()

async def main(page : ft.Page):
    page.padding = ft.padding.only(left=10, right=10, top=40)
    page.title = "Previsao do Tempo"
    page.theme = light_theme
    page.dark_theme = dark_theme
    page.theme_mode = ft.ThemeMode.LIGHT #inicia no modo claro
    page.window_width = 360
    page.window_height = 760
    page.window_resizable = False

    city= "São Paulo"

    #botao para alternar o tema
    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode - ft.ThemeMode.DARK
            theme_button.icon = ft.Icons.DARK_MODE
            
import flet as ft
from flet import View
from classApp.WidgetClass import Button, ViewClass, Field, Text
from flet import RouteChangeEvent, ViewPopEvent
import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

# VARIABLES GLOBALES
    # ALINIAMIENTO
ALIGN_VERT = ft.MainAxisAlignment.CENTER
ALIGN_HOR = ft.CrossAxisAlignment.CENTER
    # TAMAÑO DE LA VENTANA
WIDTH = config['size']['width']
HEIGHT = config['size']['height']
    # COLORES DE LA APP
COLOR_PRIMARY = config['colors']['primary']
COLOR_SECOND = config['colors']['second']

def main(page: ft.Page) -> None:
    page.title = "Calculator Simulations"
    page.window.height = HEIGHT
    page.window.width = WIDTH
    
    def router_change(e: RouteChangeEvent) -> None:
        page.views.clear()

        # Home --> Menu
        page.views.append(
            ViewClass('/', 
                [
                    Text("Menu", 40),
                    Button('Go to Router Sample', lambda _: page.go('/sample'))
                ])
        )
        
        # Sample Router
        if page.route == '/sample':
            page.views.append(
                ViewClass('/sample', [Text("Sample", 40), Field('Sample Field'), Button('Go to home', lambda _: page.go('/home'))])
            )

        page.update()
    
    def view_pop(e: ViewPopEvent) -> None:
        page.views.pop()
        top_view: View = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = router_change
    page.on_view_pop = view_pop
    page.go(page.route)

    page.update()

if __name__ == "__main__":
    ft.app(main)
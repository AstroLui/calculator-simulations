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
    page.window.center()
    page.window.resizable = False

    def router_change(e: RouteChangeEvent) -> None:
        page.views.clear()

        # Home --> Menu
        page.views.append(
            ViewClass('/', 
                [
                    ft.Column([Text("Welcome to", 20, "w150"), Text("Menu", 35, "w800")], 
                    spacing=0, horizontal_alignment=ALIGN_HOR),
                    # Cada 3 se crea una nueva row
                    ft.Row([
                            Button('Go to Router Sample', lambda _: page.go('/sample')),
                            Button('Reaccion Quimica', lambda _: page.go('/quimica')),
                            Button('Reactor Nuclear', lambda _: page.go('/nuclear'))
                        ], 
                    spacing=10, alignment=ALIGN_VERT)
                ])
        )
        
        # Sample Router
        if page.route == '/sample':
            page.views.append(
                ViewClass('/sample', [Text("Sample", 40, "w800"), Field('Sample Field'), Button('Go to menu', lambda _: page.go('/home'))])
            )

        # Quimica
        if page.route == '/quimica':
            page.views.append(
                ViewClass('quimica', [Text('Quimica', 40, "w800"), Button('Go to menu', lambda _: page.go('/home'))])
            )

        # Nuclear
        if page.route == '/nuclear':
            page.views.append(
                ViewClass('nuclear', [Text('Nuclear', 40, "w800"), Button('Go to menu', lambda _: page.go('/home'))])
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
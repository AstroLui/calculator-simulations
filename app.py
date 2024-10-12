import flet as ft
from flet import View
from flet import RouteChangeEvent, ViewPopEvent

# VARIABLES GLOBALES
    # ALINIAMIENTO
ALIGN_VERT = ft.MainAxisAlignment.CENTER
ALIGN_HOR = ft.CrossAxisAlignment.CENTER
    # TAMAÑO DE LA VENTANA
WIDTH = 300
HEIGHT = 600
    # COLORES DE LA APP
COLOR_PRIMARY = '#d3ee98'
COLOR_SECOND = '#784ca8'

def main(page: ft.Page):
    page.title = "Calculator Simulations"
    page.window.height = HEIGHT
    page.window.width = WIDTH
    
    def router_change(e: RouteChangeEvent):
        page.views.clear()

        # Home
        page.views.append(
            View(
                route='/',
                controls=[
                    ft.ElevatedButton(text="Go to Sample Router", on_click=lambda _: page.go('/sample'), bgcolor=COLOR_SECOND, color=COLOR_PRIMARY)
                ],
                bgcolor= COLOR_PRIMARY,
                vertical_alignment=ALIGN_VERT,
                horizontal_alignment=ALIGN_HOR
            )
        )
        
        # Sample Router
        if page.route == '/sample':
            page.views.append(
            View(
                route='/sample',
                controls=[
                    ft.ElevatedButton(text="Go to Home", on_click=lambda _: page.go('/'), bgcolor=COLOR_SECOND, color=COLOR_PRIMARY)
                ],
                bgcolor= COLOR_PRIMARY,
                vertical_alignment=ALIGN_VERT,
                horizontal_alignment=ALIGN_HOR
            )
        )
    
        page.update()
    
    def view_pop(e: ViewPopEvent):
        page.views.pop()
        top_view: View = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = router_change
    page.on_view_pop = view_pop
    page.go(page.route)

    page.update()

if __name__ == "__main__":
    ft.app(main)
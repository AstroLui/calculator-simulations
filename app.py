import flet as ft
from flet import View
from classApp.WidgetClass import Button, ViewClass, Field, Text
from flet import RouteChangeEvent, ViewPopEvent
from classApp.methods.ContinuoReaccionQuimica import Quimica
from classApp.methods.ContinuoReactorNuclear import Nuclear
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
                    ft.Column([Text("Welcome to", 20, "w150"), Text("Menu", 40, "w800")], 
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
            #VARIABLES PARA LOS METODOS
            QUIMICA = Quimica()
            #Variables de los Fields
            field_1 = Field("Constante de Velocidad de Reaccion (K)", 250)
            field_2 = Field("Concentracion inicial de A (A0)")
            # Function para Button Calcular
            def _(e) -> None: 
                QUIMICA.set_atr(float(field_1.getValue()), float(field_2.getValue()))
                QUIMICA.result()
            
            page.views.append(
                ViewClass('quimica', 
                    [
                        Text('Quimica', 35, "w800"),
                        ft.Row([field_1, field_2], alignment=ALIGN_VERT, spacing=5), 
                        ft.Row([
                            Button('Calcular', click_action=_),
                            Button('Go to menu', lambda _: page.go('/home'))
                        ], alignment=ALIGN_VERT, spacing=5)
                    ])
            )

        # Nuclear
        if page.route == '/nuclear':
            #VARIABLE PARA EL METODO
            NUCLEAR = Nuclear
            NUCLEAR = Nuclear()
            #Variables de los fields
            field_1 = Field('Tasa de Generacion de calor (Q_gen)', 250)
            field_2 = Field('Coeficiente de enfriamiento (K)',210)
            field_3 = Field('Temperatura del sistema (T_cool)', 250)
            field_4 = Field('Capacidad termica del reactor (C)',210)
            field_5 = Field('Temperatura inicial del reactor (T0)', 210)
            # Funcion para button calcular
            def _(e) -> None: 
                NUCLEAR.set_atr(float(field_1.getValue()), float(field_2.getValue()), float(field_3.getValue()), float(field_4.getValue()), float(field_5.getValue()))
                NUCLEAR.result()
                NUCLEAR.resutl()
            
            page.views.append(
                ViewClass('nuclear', 
                    [
                        Text('Nuclear', 35, "w800"), 
                        ft.Row([field_1, field_2], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([field_3, field_4], alignment=ALIGN_VERT, spacing=5),
                        field_5,
                        ft.Row([
                            Button('Calcular', click_action=_),
                            Button('Go to menu', lambda _: page.go('/home'))
                        ], alignment=ALIGN_VERT, spacing=5)
                    ])
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
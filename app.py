import flet as ft
from flet import View
from classApp.WidgetClass import Button, ViewClass, Field, Text, Alert, ButtonAlert, Modal
from flet import RouteChangeEvent, ViewPopEvent
from classApp.methods.ContinuoReaccionQuimica import Quimica
from classApp.methods.ContinuoReactorNuclear import Nuclear
from classApp.methods.DiscretaPeluqueria import Peluqueria
from classApp.methods.DiscretaRestaurante2 import Restaurante2
from classApp.methods.DiscretaSistemaRedes import Redes
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

    alert = Alert([ButtonAlert("Close", lambda _: page.close(alert))])

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
                    spacing=10, alignment=ALIGN_VERT),
                    ft.Row([
                        Button('Peluqueria',lambda _: page.go('/peluqueria')),
                        Button('Restaurante 2', lambda _: page.go('/restaurante2')),
                        Button('Redes', lambda _: page.go('/redes'))
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
                try:
                    QUIMICA.set_atr(float(field_1.getValue()), float(field_2.getValue()))
                    QUIMICA.result()
                except:
                    alert.openAlert(page)

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
            NUCLEAR = Nuclear()
            #Variables de los fields
            field_1 = Field('Tasa de Generacion de calor (Q_gen)', 250)
            field_2 = Field('Coeficiente de enfriamiento (K)',210)
            field_3 = Field('Temperatura del sistema (T_cool)', 250)
            field_4 = Field('Capacidad termica del reactor (C)',210)
            field_5 = Field('Temperatura inicial del reactor (T0)', 210)
            # Funcion para button calcular
            def _(e) -> None: 
                try:
                    NUCLEAR.set_atr(float(field_1.getValue()), float(field_2.getValue()), float(field_3.getValue()), float(field_4.getValue()), float(field_5.getValue()))
                    NUCLEAR.resutl()
                except:
                    alert.openAlert(page)
                
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
        if page.route == '/peluqueria':
            #VARIABLE PARA EL METODO
            PELUQUERIA = Peluqueria()
            #Variables de los fields
            field_1 = Field('Semilla', 250)
            field_2 = Field('Numero de peluqueros', 250)
            field_3 = Field('Tiempo de corte minimo', 250)
            field_4 = Field('Tiempo de corte maximo', 250)
            field_5 = Field('Tiempo entre llegadas', 250)
            field_6 = Field('Total de clientes', 250)
            # Funcion para button calcular
            def _(e) -> None:
                PELUQUERIA.set_atr(int(field_1.getValue()), int(field_2.getValue()), float(field_3.getValue()), float(field_4.getValue()), float(field_5.getValue()), int(field_6.getValue()))
                lcp, tep, upi, log = PELUQUERIA.result()
                result = f"""LPC: {lcp:.2f}
                TEP: {tep:.2f}
                UPI: {upi:.2f}
                """
                megaResult = [ft.Text(result, color=COLOR_SECOND)]
                for i in log:
                    megaResult.append(ft.Text(i, color=COLOR_SECOND))
                newContent = ft.Column(megaResult, scroll=ft.ScrollMode.ALWAYS)
                modal = Modal('Simulación de Peluqueria', newContent)
                page.open(modal)
            
            page.views.append(
                ViewClass('peluqueria', 
                    [
                        Text('Peluqueria', 35, "w800"), 
                        ft.Row([field_1, field_2], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([field_3, field_4], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([field_5, field_6], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([
                            Button('Calcular', click_action=_),
                            Button('Go to menu', lambda _: page.go('/home'))
                        ], alignment=ALIGN_VERT, spacing=5)
                    ])
            )
        if page.route == '/restaurante2':
            #VARIABLE PARA EL METODO
            RESTAURANTE2 = Restaurante2()
            #Variables de los fields
            field_1 = Field('Semilla', 250)
            field_2 = Field('Numero de mesas', 250)
            field_3 = Field('Tiempo comer minimo', 250)
            field_4 = Field('Tiempo comer maximo', 250)
            field_5 = Field('Tiempo entre llegadas', 250)
            field_6 = Field('Total de clientes', 250)
            # Funcion para button calcular
            def _(e) -> None:
                RESTAURANTE2.set_atr(int(field_1.getValue()), int(field_2.getValue()), int(field_3.getValue()), int(field_4.getValue()), int(field_5.getValue()), int(field_6.getValue()))
                log = RESTAURANTE2.result()
                megaResult = []
                for i in log:
                    megaResult.append(ft.Text(i, color=COLOR_SECOND))
                newContent = ft.Column(megaResult, scroll=ft.ScrollMode.ALWAYS)
                modal = Modal('Simulación de Restaurante 2', newContent)
                page.open(modal)
            
            page.views.append(
                ViewClass('restaurante2', 
                    [
                        Text('Restaurante 2', 35, "w800"), 
                        ft.Row([field_1, field_2], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([field_3, field_4], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([field_5, field_6], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([
                            Button('Calcular', click_action=_),
                            Button('Go to menu', lambda _: page.go('/home'))
                        ], alignment=ALIGN_VERT, spacing=5)
                    ])
            )
        if page.route == '/redes':
            #VARIABLE PARA EL METODO
            REDES = Redes()
            #Variables de los fields
            field_1 = Field('Semilla', 250)
            field_2 = Field('Capacidad del servidor', 250)
            field_3 = Field('Capacidad de la cola', 250)
            field_4 = Field('Tiempo de procesamiento minimo', 250)
            field_5 = Field('Tiempo de procesamiento maximo', 250)
            field_6 = Field('Tiempo entre llegadas', 250)
            field_7 = Field('Total de paquetes', 250)
            # Funcion para button calcular
            def _(e) -> None:
                REDES.set_atr(int(field_1.getValue()), int(field_2.getValue()), int(field_3.getValue()), int(field_4.getValue()), int(field_5.getValue()), int(field_6.getValue()), int(field_7.getValue()))
                totalPaquetes, paquetesProcesados, paquetesPerdidos, tasaPerdida, tiempoPromedioEspera, servidor, log = REDES.result()
                result = f"""Total de paquetes simulados: {totalPaquetes}
                Paquetes procesados: {paquetesProcesados}
                Paquetes perdidos: {paquetesPerdidos}
                Tasa de pérdida de paquetes: {tasaPerdida:.2f}%
                Tiempo promedio de espera de los paquetes: {tiempoPromedioEspera:.2f} segundos
                Utilización del servidor: {servidor:.2f}%
                """
                megaResult = [ft.Text(result, color=COLOR_SECOND)]
                for i in log:
                    megaResult.append(ft.Text(i, color=COLOR_SECOND))
                newContent = ft.Column(megaResult, scroll=ft.ScrollMode.ALWAYS)
                modal = Modal('Simulación de Red de Computadoras', newContent)
                page.open(modal)
            
            page.views.append(
                ViewClass('redes', 
                    [
                        Text('Redes', 35, "w800"), 
                        ft.Row([field_1, field_2], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([field_3, field_4], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([field_5, field_6], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([field_7], alignment=ALIGN_VERT, spacing=5),
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
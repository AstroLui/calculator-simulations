import flet as ft
from flet import View
from classApp.WidgetClass import Button, ViewClass, Field, Text, Alert, ButtonAlert, Modal
from flet import RouteChangeEvent, ViewPopEvent
from classApp.methods.ContinuoReaccionQuimica import Quimica
from classApp.methods.ContinuoReactorNuclear import Nuclear
from classApp.methods.DiscretaPeluqueria import Peluqueria
from classApp.methods.DiscretaRestaurante2 import Restaurante2
from classApp.methods.DiscretaSistemaRedes import Redes
from classApp.methods.DiscretaRestaurante import DriveThruSimulation  # Import the new class
import yaml
from classApp.WidgetClass import createTXT
import traceback

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

# VARIABLES GLOBALES
ALIGN_VERT = ft.MainAxisAlignment.CENTER
ALIGN_HOR = ft.CrossAxisAlignment.CENTER
WIDTH = config['size']['width']
HEIGHT = config['size']['height']
COLOR_PRIMARY = config['colors']['primary']
COLOR_SECOND = config['colors']['second']

def main(page: ft.Page) -> None:
    page.title = "Calculadora Simulaciones"
    page.window.height = HEIGHT
    page.window.width = WIDTH
    page.window.center()
    page.window.resizable = False

    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color={ft.ControlState.DEFAULT: ft.colors.TRANSPARENT},
            track_visibility=False,
            thumb_visibility=True,
            thumb_color={ft.ControlState.DEFAULT: COLOR_SECOND}
        )
    )

    alert = Alert([ButtonAlert("Close", lambda _: page.close(alert))])
    modal = Modal([Button("Close", lambda _: page.close(modal))])

    def router_change(e: RouteChangeEvent) -> None:
        page.views.clear()

        # Home --> Menu
        page.views.append(
            ViewClass('/', 
                [
                    ft.Column([Text("Bienvenido a calculadora simulaciones", 20, "w150"), Text("Menú", 40, "w800")], 
                    spacing=0, horizontal_alignment=ALIGN_HOR),
                    ft.Row([
                            Button('Reaccion Química', lambda _: page.go('/quimica')),
                            Button('Reactor Nuclear', lambda _: page.go('/nuclear')),
                            Button('Peluquería',lambda _: page.go('/peluqueria'))
                        ], 
                    spacing=10, alignment=ALIGN_VERT),
                    ft.Row([
                        
                        Button('Restaurante', lambda _: page.go('/restaurante2')),
                        Button('Restaurante Auto-Servicio', lambda _: page.go('/auto_servicio')),
                        Button('Redes', lambda _: page.go('/redes')),
                    ], 
                    spacing=10, alignment=ALIGN_VERT)
                ])
        )

        # Quimica
        if page.route == '/quimica':
            QUIMICA = Quimica()
            field_1 = Field("Constante de Velocidad de Reacción (K)", 250, value='0.1')
            field_2 = Field("Concentración inicial de A (A0)", 250, value='1')
            def _(e) -> None: 
                try:
                    QUIMICA.set_atr(float(field_1.getValue()), float(field_2.getValue()))
                    QUIMICA.result()
                except ValueError:
                    alert.openAlert(page, "Error: Por favor, ingrese valores numéricos válidos.")
                except TypeError:
                    alert.openAlert(page, "Error: Tipo de dato incorrecto.")
                except AttributeError:
                    alert.openAlert(page, "Error: Atributo no encontrado.")
                except Exception as ex:
                    alert.openAlert(page, f"Error inesperado: {str(ex)}")

            page.views.append(
                ViewClass('quimica', 
                    [
                        Text('Quimíca', 35, "w800"),
                        ft.Row([field_1, field_2], alignment=ALIGN_VERT, spacing=5), 
                        ft.Row([
                            Button('Calcular', click_action=_),
                            Button('Volver a menú', lambda _: page.go('/home'))
                        ], alignment=ALIGN_VERT, spacing=5)
                    ])
            )

        # Nuclear
        if page.route == '/nuclear':
            NUCLEAR = Nuclear()
            field_1 = Field('Tasa de Generación de calor (Q_gen)', 250, value='5000')
            field_2 = Field('Coeficiente de enfriamiento (K)',210, value='0.1')
            field_3 = Field('Temperatura del sistema (T_cool)', 250, value='25')
            field_4 = Field('Capacidad térmica del reactor (C)',210, value='10000')
            field_5 = Field('Temperatura inicial del reactor (T0)', 210, value='150')
            def _(e) -> None: 
                try:
                    NUCLEAR.set_atr(float(field_1.getValue()), float(field_2.getValue()), float(field_3.getValue()), float(field_4.getValue()), float(field_5.getValue()))
                    NUCLEAR.resutl()
                except ValueError:
                    alert.openAlert(page, "Error: Por favor, ingrese valores numéricos válidos.")
                except TypeError:
                    alert.openAlert(page, "Error: Tipo de dato incorrecto.")
                except AttributeError:
                    alert.openAlert(page, "Error: Atributo no encontrado.")
                except Exception as ex:
                    alert.openAlert(page, f"Error inesperado: {str(ex)}")
                
            page.views.append(
                ViewClass('nuclear', 
                    [
                        Text('Nuclear', 35, "w800"), 
                        ft.Row([field_1, field_2], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([field_3, field_4], alignment=ALIGN_VERT, spacing=5),
                        field_5,
                        ft.Row([
                            Button('Calcular', click_action=_),
                            Button('Volver a menú', lambda _: page.go('/home'))
                        ], alignment=ALIGN_VERT, spacing=5)
                    ])
            )

        # Peluqueria
        if page.route == '/peluqueria':
            PELUQUERIA = Peluqueria()
            field_1 = Field('Semilla', 250, value='30')
            field_2 = Field('Numero de peluqueros', 250, value='1')
            field_3 = Field('Tiempo de corte mínimo', 250, value='15')
            field_4 = Field('Tiempo de corte máximo', 250, value='30')
            field_5 = Field('Tiempo entre llegadas', 250, value='20')
            field_6 = Field('Total de clientes', 250, value='5')
            def _(e) -> None:
                try:
                    PELUQUERIA.set_atr(int(field_1.getValue()), int(field_2.getValue()), float(field_3.getValue()), float(field_4.getValue()), float(field_5.getValue()), int(field_6.getValue()))
                    PELUQUERIA.result()
                    createTXT(PELUQUERIA.getResultText(), 'SIMULACIÓN PELUQUERÍA')
                    results = [ft.Text(PELUQUERIA.getResultText(), color=COLOR_SECOND)]
                    for i in PELUQUERIA.getLog():
                        results.append(ft.Text(i, color=COLOR_SECOND))
                    createTXT(PELUQUERIA.getLog())
                    modal.openModal(page=page,title='Simulación de Peluqueria', content=results)
                except ValueError:
                    alert.openAlert(page, "Error: Por favor, ingrese valores numéricos válidos.")
                except TypeError:
                    alert.openAlert(page, "Error: Tipo de dato incorrecto.")
                except AttributeError:
                    alert.openAlert(page, "Error: Atributo no encontrado.")
                except Exception as ex:
                    alert.openAlert(page, f"Error inesperado: {str(ex)}")

            page.views.append(
                ViewClass('peluqueria', 
                    [
                        Text('Peluquería', 35, "w800"), 
                        ft.Row([field_1, field_2], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([field_3, field_4], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([field_5, field_6], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([
                            Button('Calcular', click_action=_),
                            Button('Volver a menú', lambda _: page.go('/home'))
                        ], alignment=ALIGN_VERT, spacing=5)
                    ])
            )

        # Restaurante 2
        if page.route == '/restaurante2':
            RESTAURANTE2 = Restaurante2()
            field_1 = Field('Semilla', 250, value='42')
            field_2 = Field('Numero de mesas', 250, value='5')
            field_3 = Field('Tiempo de comer mínimo', 250, value='20')
            field_4 = Field('Tiempo de comer máximo', 250, value='40')
            field_5 = Field('Tiempo entre llegadas', 250, value='10')
            field_6 = Field('Total de clientes', 250, value='10')
            def _(e) -> None:
                try:
                    RESTAURANTE2.set_atr(int(field_1.getValue()), int(field_2.getValue()), int(field_3.getValue()), int(field_4.getValue()), int(field_5.getValue()), int(field_6.getValue()))
                    RESTAURANTE2.result()
                    results = []
                    for i in RESTAURANTE2.getLog():
                        results.append(ft.Text(i, color=COLOR_SECOND))
                    createTXT(RESTAURANTE2.getLog(), 'SIMULACIÓN RESTAURANTE 2')
                    modal.openModal(page, 'Simulación de Restaurante 2', results)
                except ValueError:
                    alert.openAlert(page, "Error: Por favor, ingrese valores numéricos válidos.")
                except TypeError:
                    alert.openAlert(page, "Error: Tipo de dato incorrecto.")
                except AttributeError:
                    alert.openAlert(page, "Error: Atributo no encontrado.")
                except Exception as ex:
                    alert.openAlert(page, f"Error inesperado: {str(ex)}")

            page.views.append(
                ViewClass('restaurante2', 
                    [
                        Text('Restaurante 2', 35, "w800"), 
                        ft.Row([field_1, field_2], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([field_3, field_4], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([field_5, field_6], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([
                            Button('Calcular', click_action=_),
                            Button('Volver a menú', lambda _: page.go('/home'))
                        ], alignment=ALIGN_VERT, spacing=5)
                    ])
            )

        # Redes
        if page.route == '/redes':
            REDES = Redes()
            field_1 = Field('Semilla', 250, value='42')
            field_2 = Field('Capacidad del servidor', 250, value='1')
            field_3 = Field('Capacidad de la cola', 250, value='5')
            field_4 = Field('Tiempo de procesamiento mínimo', 250, value='2')
            field_5 = Field('Tiempo de procesamiento máximo', 250, value='5')
            field_6 = Field('Tiempo entre llegadas', 250, value='3')
            field_7 = Field('Total de paquetes', 250, value='50')
            def _(e) -> None:
                try:
                    REDES.set_atr(int(field_1.getValue()), int(field_2.getValue()), int(field_3.getValue()), int(field_4.getValue()), int(field_5.getValue()), int(field_6.getValue()), int(field_7.getValue()))
                    REDES.result()
                    results = [ft.Text(REDES.getResultText(), color=COLOR_SECOND)]
                    for i in REDES.getLog():
                        results.append(ft.Text(i, color=COLOR_SECOND))
                    createTXT(REDES.getLog(), 'SIMULACION REDES')
                    modal.openModal(page,'Simulación de Red de Computadoras', results)
                    createTXT(REDE.getResultText())

                except ValueError:
                    alert.openAlert(page, "Error: Por favor, ingrese valores numéricos válidos.")
                except TypeError:
                    alert.openAlert(page, "Error: Tipo de dato incorrecto.")
                except AttributeError:
                    alert.openAlert(page, "Error: Atributo no encontrado.")
                except Exception as ex:
                    alert.openAlert(page, f"Error inesperado: {str(ex)}")

            
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
                            Button('Volver a menú', lambda _: page.go('/home'))
                        ], alignment=ALIGN_VERT, spacing=5)
                    ])
            )

        # Drive Thru
        if page.route == '/auto_servicio':
            auto_servicio = DriveThruSimulation()
            field_1 = Field('Numero de counters', 250, value='3')
            field_2 = Field('Semilla', 250, value='42')
            field_3 = Field('Hora de apertura', 250, value='7')
            field_4 = Field('Hora de cierre', 250, value='23')
            field_6 = Field('Inicio de hora pico', 250, value='11')
            field_7 = Field('Fin de hora pico', 250, value='13')
            field_8 = Field('Cota inferior', 250, value='5')
            field_9 = Field('Cota superior', 250, value='10')
            field_10 = Field('Cota inferior', 250, value='1')
            field_11 = Field('Cota superior', 250, value='5')
            
            def _(e) -> None:
                try:
                    auto_servicio.__init__(
                        num_counters=int(field_1.getValue()),
                        random_seed=int(field_2.getValue()),
                        hour_open=int(field_3.getValue()),
                        hour_close=int(field_4.getValue()),
                        peak_start=int(field_6.getValue()),
                        peak_end=int(field_7.getValue()),
                        customer_range_norm=[int(field_8.getValue()), int(field_9.getValue())],
                        customer_range_peak=[int(field_10.getValue()), int(field_11.getValue())]
                    )
                    # Capture the output of the simulation
                    output = auto_servicio.run_with_output_capture()
                    createTXT(output, 'SIMULACIÓN RESTAURANTE AUTO-SERVICIO')
                    
                    # Display the output
                    results = [ft.Text(output, color=COLOR_SECOND)]
                    modal.openModal(page,'Simulación de Restaurante Auto-Servicio', results)
                except ValueError:
                    alert.openAlert(page, "Error: Por favor, ingrese valores numéricos válidos.")
                except TypeError:
                    alert.openAlert(page, "Error: Tipo de dato incorrecto.")
                except AttributeError:
                    alert.openAlert(page, "Error: Atributo no encontrado.")
                except Exception as ex:
                    alert.openAlert(page, f"Error inesperado: {str(ex)}")

            page.views.append(
                ViewClass('auto_servicio', 
                    [
                        Text('Restaurante Auto-Servicio', 35, "w800"), 
                        ft.Row([field_1, field_2], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([field_3, field_4], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([field_6, field_7], alignment=ALIGN_VERT, spacing=5),
                        Text('Rango de clientes en horas normales', 12, "w500"),
                        ft.Row([field_8, field_9], alignment=ALIGN_VERT, spacing=5),
                        Text('Rango de clientes en horas pico', 12, "w500"),
                        ft.Row([field_10, field_11], alignment=ALIGN_VERT, spacing=5),
                        ft.Row([
                            Button('Calcular', click_action=_),
                            Button('Volver a menú', lambda _: page.go('/home'))
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
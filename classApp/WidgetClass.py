import yaml
import flet as ft

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

# VARIABLES GLOBALES
    # ALINIAMIENTO
COLOR_PRIMARY = config['colors']['primary']
COLOR_SECOND = config['colors']['second']
    # COLORES DE LA APP
ALIGN_VERT = ft.MainAxisAlignment.CENTER
ALIGN_HOR = ft.CrossAxisAlignment.CENTER

class Button(ft.ElevatedButton):
    def __init__(self, text, click_action):
        super().__init__()
        self.text= text
        self.bgcolor= COLOR_SECOND
        self.color= COLOR_PRIMARY
        self.on_click = click_action


class ViewClass(ft.View):
    def __init__(self, router, controls):
        super().__init__()
        self.route = router
        self.controls = controls
        self.bgcolor = COLOR_PRIMARY
        self.vertical_alignment = ALIGN_VERT
        self.horizontal_alignment = ALIGN_HOR


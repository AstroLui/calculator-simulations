import yaml
import flet as ft

#Lectura del archivo config
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

# VARIABLES GLOBALES
    # ALINIAMIENTO
ALIGN_VERT = ft.MainAxisAlignment.CENTER
ALIGN_HOR = ft.CrossAxisAlignment.CENTER
    # COLORES DE LA APP
COLOR_PRIMARY = config['colors']['primary']
COLOR_SECOND = config['colors']['second']
DANGER = config['colors']['danger']
    # OTROS
STATE = ft.ControlState

# CLASE BOTON
class Button(ft.ElevatedButton):
    def __init__(self, text: str, click_action):
        super().__init__()
        self.text= text
        self.bgcolor= COLOR_SECOND
        self.color= COLOR_PRIMARY
        self.on_click = click_action
        self.style = ft.ButtonStyle(
            color={
                STATE.HOVERED: COLOR_SECOND,
                STATE.FOCUSED: COLOR_PRIMARY,
                STATE.DEFAULT: COLOR_PRIMARY
            },
            bgcolor={
                STATE.HOVERED: COLOR_PRIMARY,
                STATE.DEFAULT: COLOR_SECOND,
            },
            side={
                STATE.HOVERED: ft.BorderSide(2, COLOR_SECOND),
            }
        )
# CLASE View
class ViewClass(ft.View):
    def __init__(self, router: str, controls):
        super().__init__()
        self.route = router
        self.controls = controls
        self.bgcolor = COLOR_PRIMARY
        self.vertical_alignment = ALIGN_VERT
        self.horizontal_alignment = ALIGN_HOR

# CLASE TextField
class Field(ft.Container):
    def __init__(self, label: str, width: int=200, value=0) -> None:
        super().__init__()
        self._TextField = ft.TextField(
            bgcolor=COLOR_PRIMARY, 
            cursor_color=COLOR_SECOND, 
            color=COLOR_SECOND, 
            border_color=COLOR_SECOND,
            text_align= ALIGN_VERT,
            text_size=config['input']['text-size'],
            height=config['input']['height'],
            value=value,
            width = width
        )
        self.content=ft.Column([
            ft.Text(value=label, color=COLOR_SECOND),
            self._TextField
        ], spacing=5)
        self.padding=10
    
    def getValue(self):
        return self._TextField.value

# CLASE PARA TEXTO EN ESPECIFICOS como Titulos, Subtitulos, etc
class Text(ft.Text):
    def __init__(self, value: str, size: int, weight: str) -> None:
        super().__init__()
        self.value = value
        self.size = size
        self.color = COLOR_SECOND
        self.bgcolor = COLOR_PRIMARY
        self.weight = weight

# CLASE PARA EL MODAL
class Modal(ft.AlertDialog):
    def __init__(self, actions) -> None:
        super().__init__()
        self.content_padding = 20
        self.bgcolor = COLOR_PRIMARY
        self.actions = actions

    def openModal(self, page: ft.Page, title: str, content:[]) -> None:
        self.title = Text(title, 25, 800)
        self.content = ft.Column(content, spacing=5, scroll=ft.ScrollMode.AUTO)
        page.open(self)

# CLASE PARA EL ALERT     
class Alert(ft.AlertDialog):
    def __init__(self, actions) -> None:
        super().__init__()
        self.modal = True
        self.bgcolor = DANGER
        self.title=ft.Text('Mensaje de Error', color=COLOR_PRIMARY)
        self.actions= actions
    
    def openAlert(self, page: ft.Page, text) -> None:
        self.content= ft.Text(text, color=COLOR_PRIMARY)
        page.open(self)


# BUTTON PARA EL ALERT
class ButtonAlert(ft.ElevatedButton):
    def __init__(self, text: str, click_action) -> None:
        super().__init__()
        self.text = text
        self.bgcolor = COLOR_PRIMARY
        self.color = DANGER
        self.on_click = click_action
        self.style = ft.ButtonStyle(
            color={
                STATE.HOVERED: DANGER,
                STATE.FOCUSED: DANGER,
                STATE.DEFAULT: COLOR_PRIMARY
            },
            bgcolor={
                STATE.HOVERED: COLOR_PRIMARY,
                STATE.DEFAULT: DANGER,
            },
            side={
                STATE.DEFAULT: ft.BorderSide(2,COLOR_PRIMARY),
            }
        )

def createTXT(content, title = None) -> None:
    with open('output.txt', 'a') as f:
        if title:
            f.write(f'\n------------------------------------------{title}------------------------------------------')
        if isinstance(content, list):
            f.write('\n')
            for item in content:
                f.write(f'{item}\n')
        else:
            f.write('\n')
            f.write(content)
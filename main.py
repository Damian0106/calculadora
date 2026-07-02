from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.window import Window


Window.clearcolor = (1, 1, 1, 1)

class Calculadora(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        #historial de operaciones
        self.memoria_historial = []
        #pantalla del historial
        self.historial = Label(
            text="",
            font_size=20,
            halign="right",
            valign="bottom",
            size_hint_y=0.15,
            color=(0.4, 0.4, 0.4, 1),
        )
        self.historial.bind(size=self.historial.setter("text_size"))

        # pantalla principal
        self.pantalla = Label(
            text="0",
            font_size=60,
            halign="right",
            valign="middle",
            size_hint_y=0.25,
            color=(0, 0, 0, 1),
        )
        self.pantalla.bind(size=self.pantalla.setter("text_size"))

        self.add_widget(self.historial)
        self.add_widget(self.pantalla)

        # Botones 
        botones = [
            ("C",  "especial"), ("<-",  "especial"), ("%",  "especial"), ("/",  "operador"),
            ("7",  "numero"),   ("8",  "numero"),   ("9",  "numero"),   ("*",  "operador"),
            ("4",  "numero"),   ("5",  "numero"),   ("6",  "numero"),   ("-",  "operador"),
            ("1",  "numero"),   ("2",  "numero"),   ("3",  "numero"),   ("+",  "operador"),
            ("0",  "numero"),   (".",  "numero"),   ("Historial",  "especial"), ("=",  "operador"),
        ]
        
        grid = GridLayout(cols=4, spacing=5, padding=5)

        for texto, tipo in botones:
          
            btn_kwargs = {
                "text": texto,
                "background_normal": "", 
                "color": (1, 1, 1, 1),  #Blanco
            }
            if tipo == "numero":
                btn_kwargs["background_color"] = (0.2, 0.7, 0.9, 1) # Celeste
                btn_kwargs["font_size"] = 40 
            elif tipo == "operador":
                btn_kwargs["background_color"] = (0.1, 0.3, 0.8, 1) # Azul
                btn_kwargs["font_size"] = 34
            elif tipo == "especial":
               
                if texto == "Historial ":
                    btn_kwargs["background_color"] = (0.3, 0.6, 0.5, 1)
                else:
                    btn_kwargs["background_color"] = (0.4, 0.5, 0.7, 1) 
                btn_kwargs["font_size"] = 28

            btn = Button(**btn_kwargs)
            btn.bind(on_release=self.presionar)
            grid.add_widget(btn)

        self.add_widget(grid)

    def presionar(self, btn):
        texto = btn.text
        actual = self.pantalla.text

        if texto == "C":
            self.pantalla.text = "0"
            self.historial.text = ""

        elif texto == "<-":
            if actual in ("0", "Error") or len(actual) <= 1:
                self.pantalla.text = "0"
            else:
                self.pantalla.text = actual[:-1]

        elif texto == "Historial":
            self.mostrar_historial()

        elif texto == "%":
            try:
                val = float(actual) / 100
                resultado = str(int(val)) if val.is_integer() else str(round(val, 6))
                
                # Guardamos la operación de porcentaje en el historial
                self.memoria_historial.append(f"{actual}% = {resultado}")
                self.pantalla.text = resultado
            except Exception:
                self.pantalla.text = "Error"

        elif texto == "=":
            try:
                self.historial.text = actual + " ="
                resultado = eval(actual)
                if isinstance(resultado, float):
                    resultado = int(resultado) if resultado.is_integer() else round(resultado, 4)
                
                resultado_str = str(resultado)
                # Guardamos la operación en la lista de memoria
                self.memoria_historial.append(f"{actual} = {resultado_str}")
                
                self.pantalla.text = resultado_str
            except Exception:
                self.pantalla.text = "Error"

        else:
            if actual == "0" and texto not in ("+", "-", "*", "/", "."):
                self.pantalla.text = texto
            else:
                if texto in ("+", "-", "*", "/") and actual[-1] in ("+", "-", "*", "/"):
                    self.pantalla.text = actual[:-1] + texto
                else:
                    self.pantalla.text += texto

    def mostrar_historial(self):
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        texto_historial = "\n".join(self.memoria_historial) if self.memoria_historial else "No hay operaciones registradas."
        caja_texto = TextInput(
            text=texto_historial,
            readonly=True,
            font_size=24,
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0, 0, 0, 1)
        )
        layout.add_widget(caja_texto)
        box_botones = BoxLayout(size_hint_y=0.2, spacing=10)
        btn_limpiar = Button(
            text="Limpiar", 
            background_normal="", 
            background_color=(0.9, 0.4, 0.2, 1),
            font_size=20
        )
        btn_cerrar = Button(
            text="Cerrar", 
            background_normal="", 
            background_color=(0.2, 0.5, 0.8, 1),
            font_size=20
        )
        
        box_botones.add_widget(btn_limpiar)
        box_botones.add_widget(btn_cerrar)
        layout.add_widget(box_botones)
        
        popup = Popup(
            title="Historial de Operaciones",
            content=layout,
            size_hint=(0.85, 0.7),
            title_size=22
        )
        btn_cerrar.bind(on_release=popup.dismiss)

        def limpiar_historial(instancia):
            self.memoria_historial.clear()
            caja_texto.text = "No hay operaciones registradas."
            
        btn_limpiar.bind(on_release=limpiar_historial)
        
        # Mostramos la ventana
        popup.open()


class CalculadoraApp(App):
    def build(self):
        self.title = "Calculadora"
        return Calculadora()


if __name__ == "__main__":
    CalculadoraApp().run()

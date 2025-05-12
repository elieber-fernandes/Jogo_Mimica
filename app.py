from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDTextButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout
import requests
from bs4 import BeautifulSoup
from functools import partial

KV = '''
MDScreenManager:
    MenuScreen:
    JogadoresScreen:
    PalavrasScreen:
    ResultadoScreen:
    PlacarScreen:

<MenuScreen>:
    name: "menu"
    MDBoxLayout:
        orientation: "vertical"
        padding: [32, 48, 32, 48]
        spacing: 24
        MDBoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: "100dp"
            MDIcon:
                icon: "emoticon-outline"
                halign: "center"
                theme_text_color: "Custom"
                text_color: app.theme_cls.primary_color
                font_size: "72sp"
        MDCard:
            orientation: "vertical"
            padding: 32
            size_hint: 0.95, None
            height: self.minimum_height
            pos_hint: {"center_x": .5, "center_y": .5}
            elevation: 12
            radius: [24, 24, 24, 24]
            shadow_softness: 2
            shadow_offset: [0, 2]
            spacing: 24
            MDLabel:
                text: "Digite o nome do time"
                halign: "center"
                font_style: "H5"
                theme_text_color: "Primary"
            MDTextField:
                id: nome_time
                hint_text: "Nome do time"
                size_hint_x: 0.8
                pos_hint: {"center_x": .5}
                mode: "rectangle"
            MDRaisedButton:
                text: "Próximo"
                md_bg_color: app.theme_cls.primary_color
                pos_hint: {"center_x": .5}
                size_hint_x: 0.5
                radius: [16, 16, 16, 16]
                on_release: app.go_to_jogadores(nome_time.text)

<JogadoresScreen>:
    name: "jogadores"
    MDBoxLayout:
        orientation: "vertical"
        padding: [32, 48, 32, 48]
        spacing: 24
        MDCard:
            orientation: "vertical"
            padding: 32
            size_hint: 0.95, None
            height: self.minimum_height
            pos_hint: {"center_x": .5, "center_y": .5}
            elevation: 12
            radius: [24, 24, 24, 24]
            shadow_softness: 2
            shadow_offset: [0, 2]
            spacing: 24
            MDLabel:
                id: time_label
                text: ""
                halign: "center"
                font_style: "H5"
                theme_text_color: "Primary"
            MDTextField:
                id: nomes_jogadores
                hint_text: "Ex: Ana, João, Maria"
                size_hint_x: 0.8
                pos_hint: {"center_x": .5}
                mode: "rectangle"
            MDRaisedButton:
                text: "Adicionar outro time"
                pos_hint: {"center_x": .5}
                size_hint_x: 0.8
                radius: [16, 16, 16, 16]
                md_bg_color: app.theme_cls.primary_dark
                on_release: app.adicionar_time(nomes_jogadores.text, True)
            MDRaisedButton:
                text: "Próximo"
                md_bg_color: app.theme_cls.primary_color
                pos_hint: {"center_x": .5}
                size_hint_x: 0.5
                radius: [16, 16, 16, 16]
                on_release: app.adicionar_time(nomes_jogadores.text, False)

<PalavrasScreen>:
    name: "palavras"
    MDBoxLayout:
        orientation: "vertical"
        padding: [32, 48, 32, 48]
        spacing: 24

        MDLabel:
            id: instrucao
            text: "Escolha uma palavra para mimicar"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Primary"
            size_hint_y: None
            height: self.texture_size[1] + dp(16)
        MDLabel:
            id: jogador_info
            text: ""
            halign: "center"
            font_style: "Subtitle1"
            theme_text_color: "Secondary"
            size_hint_y: None
            height: self.texture_size[1] + dp(8)

        Widget:

        MDCard:
            orientation: "vertical"
            padding: [24, 32, 24, 32]
            size_hint: 0.95, None
            height: self.minimum_height
            pos_hint: {"center_x": .5, "center_y": .5}
            elevation: 12
            radius: [24, 24, 24, 24]
            shadow_softness: 2
            shadow_offset: [0, 2]
            spacing: 32

            MDBoxLayout:
                id: palavras_box
                orientation: "vertical"
                spacing: 16
                size_hint_y: None
                height: self.minimum_height
                pos_hint: {"center_x": .5}

            MDRaisedButton:
                id: confirmar_btn
                text: "Confirmar"
                pos_hint: {"center_x": .5}
                size_hint_x: 0.7
                radius: [16, 16, 16, 16]
                md_bg_color: app.theme_cls.primary_color
                on_release: app.confirmar_palavra()

        Widget:

<ResultadoScreen>:
    name: "resultado"
    MDBoxLayout:
        orientation: "vertical"
        padding: [32, 48, 32, 48]
        spacing: 24

        MDLabel:
            text: "Quem acertou?"
            halign: "center"
            font_style: "H5"
            theme_text_color: "Primary"
            pos_hint: {"center_x": .5}

        MDCard:
            orientation: "vertical"
            padding: 24
            size_hint: 0.95, None
            height: self.minimum_height
            pos_hint: {"center_x": .5}
            elevation: 12
            radius: [24, 24, 24, 24]
            shadow_softness: 2
            shadow_offset: [0, 2]
            spacing: 16

            MDBoxLayout:
                id: times_box
                orientation: "vertical"
                spacing: 16
                size_hint_y: None
                height: self.minimum_height
                pos_hint: {"center_x": .5}

        MDRaisedButton:
            text: "Confirmar"
            pos_hint: {"center_x": .5}
            size_hint_x: 0.5
            radius: [16, 16, 16, 16]
            md_bg_color: app.theme_cls.primary_color
            on_release: app.confirmar_vencedor()

<PlacarScreen>:
    name: "placar"
    MDBoxLayout:
        orientation: "vertical"
        padding: [32, 48, 32, 48]
        spacing: 24

        MDLabel:
            text: "Placar"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Primary"
            pos_hint: {"center_x": .5}

        MDCard:
            orientation: "vertical"
            padding: 24
            size_hint: 0.95, None
            height: self.minimum_height
            pos_hint: {"center_x": .5}
            elevation: 12
            radius: [24, 24, 24, 24]
            shadow_softness: 2
            shadow_offset: [0, 2]
            spacing: 16

            MDBoxLayout:
                id: placar_box
                orientation: "vertical"
                spacing: 8
                size_hint_y: None
                height: self.minimum_height
                pos_hint: {"center_x": .5}

        MDRaisedButton:
            text: "Próxima Rodada"
            pos_hint: {"center_x": .5}
            size_hint_x: 0.5
            radius: [16, 16, 16, 16]
            md_bg_color: app.theme_cls.primary_color
            on_release: app.proxima_rodada()
        MDRaisedButton:
            text: "Novo jogo"
            pos_hint: {"center_x": .5}
            size_hint_x: 0.5
            radius: [16, 16, 16, 16]
            md_bg_color: app.theme_cls.primary_dark
            on_release: app.novo_jogo()
'''

class MenuScreen(MDScreen): pass
class JogadoresScreen(MDScreen): pass
class PalavrasScreen(MDScreen): pass
class ResultadoScreen(MDScreen): pass
class PlacarScreen(MDScreen): pass

class MimicaApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"  # Tema escuro
        self.theme_cls.primary_palette = "Purple"  # Cor roxa
        self.times = []
        self.jogadores = []
        self.pontuacao = {}
        self.current_time = ""
        self.palavra_escolhida = ""
        self.palavras = []
        self.vencedor = ""
        self.time_index = 0
        self.jogador_index = 0
        return Builder.load_string(KV)

    def go_to_jogadores(self, nome_time):
        if not nome_time.strip():
            self.show_dialog("Digite o nome do time")
            return
        self.current_time = nome_time.strip()
        self.root.get_screen('jogadores').ids.time_label.text = f"Time: {self.current_time}"
        self.root.current = 'jogadores'

    def adicionar_time(self, nomes, adicionar_outro):
        nomes = [j.strip() for j in nomes.split(',') if j.strip()]
        if not nomes:
            self.show_dialog("Digite os nomes dos jogadores")
            return
        self.times.append(self.current_time)
        self.jogadores.append(nomes)
        self.pontuacao[self.current_time] = 0
        if adicionar_outro:
            self.root.current = 'menu'
        else:
            self.time_index = 0
            self.jogador_index = 0
            self.root.current = 'palavras'
            self.carregar_palavras()

    def carregar_palavras(self):
        jogador = self.jogadores[self.time_index][self.jogador_index]
        time = self.times[self.time_index]
        
        # Atualiza as labels de instrução
        instrucao = self.root.get_screen('palavras').ids.instrucao
        jogador_info = self.root.get_screen('palavras').ids.jogador_info
        instrucao.text = "ESCOLHA UMA PALAVRA!"
        jogador_info.text = f"VEZ DE: {jogador} - ({time})"

        try:
            page = requests.get("https://www.palabrasaleatorias.com/palavras-aleatorias.php?fs=4&fs2=0&Submit=Nova+palavra")
            soup = BeautifulSoup(page.content, 'html.parser')
            divs = soup.find_all('div')
            self.palavras = [divs[i].get_text() for i in range(1, 5)]
        except Exception:
            self.palavras = ["Palavra 1", "Palavra 2", "Palavra 3", "Palavra 4"]
        
        box = self.root.get_screen('palavras').ids.palavras_box
        box.clear_widgets()
        for palavra in self.palavras:
            box.add_widget(MDFlatButton(
                text=palavra.upper(),
                font_size="18sp",
                size_hint_x=0.9,
                pos_hint={"center_x": .5},
                on_release=lambda x, p=palavra: self.selecionar_palavra(p)
            ))
        
        self.root.get_screen('palavras').ids.confirmar_btn.disabled = True
        self.palavra_escolhida = ""

    def selecionar_palavra(self, palavra):
        self.palavra_escolhida = palavra
        self.root.get_screen('palavras').ids.confirmar_btn.disabled = False

    def confirmar_palavra(self):
        if not self.palavra_escolhida:
            self.show_dialog("Escolha uma palavra")
            return
        box = self.root.get_screen('palavras').ids.palavras_box
        box.clear_widgets()
        from kivy.clock import Clock
        from kivymd.uix.label import MDLabel
        from kivymd.uix.button import MDRaisedButton

        self.mostrar = False

        def toggle_palavra(instance):
            self.mostrar = not self.mostrar
            if self.mostrar:
                palavra_btn.text = self.palavra_escolhida.upper()
            else:
                palavra_btn.text = "Clique para mostrar a palavra"

        palavra_btn = MDRaisedButton(
            text="Clique para mostrar a palavra",
            pos_hint={"center_x": 0.5},
            on_release=toggle_palavra
        )
        box.add_widget(palavra_btn)
        

        self.tempo = 6
        self.timer_label = MDLabel(text=f"Tempo restante: {self.tempo} segundos", halign="center")
        box.add_widget(self.timer_label)
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)
        self.root.get_screen('palavras').ids.confirmar_btn.disabled = True

    def update_timer(self, dt):
        self.tempo -= 1
        self.timer_label.text = f"Tempo restante: {self.tempo} segundos"
        if self.tempo <= 0:
            from kivy.clock import Clock
            Clock.unschedule(self.timer_event)
            self.root.current = 'resultado'
            self.carregar_resultado()

    def carregar_resultado(self):
        box = self.root.get_screen('resultado').ids.times_box
        box.clear_widgets()
        from kivymd.uix.selectioncontrol import MDCheckbox
        from kivymd.uix.boxlayout import MDBoxLayout
        self.vencedor = None
        for time in self.times:
            layout = MDBoxLayout(orientation="horizontal", spacing=8, size_hint_y=None, height="48dp")
            checkbox = MDCheckbox(group="vencedor")
            checkbox.bind(active=partial(self.on_checkbox_active, time))
            layout.add_widget(checkbox)
            layout.add_widget(MDLabel(text=time, valign="center"))
            box.add_widget(layout)
        # Ajusta a altura do times_box conforme o número de times
        box.height = len(self.times) * 48

    def on_checkbox_active(self, time, instance, value):
        if value:
            self.vencedor = time

    def confirmar_vencedor(self):
        if not self.vencedor:
            self.show_dialog("Selecione o time vencedor")
            return
        self.pontuacao[self.vencedor] += 1

        self.jogador_index += 1
        if self.jogador_index >= len(self.jogadores[self.time_index]):
            self.jogador_index = 0
            self.time_index = (self.time_index + 1) % len(self.times)
        self.vencedor = ""

        self.root.current = 'placar'
        self.carregar_placar()

    def carregar_placar(self):
        box = self.root.get_screen('placar').ids.placar_box
        box.clear_widgets()
        for time, pontos in self.pontuacao.items():
            box.add_widget(MDLabel(
                text=f"{time}: {pontos} ponto(s)",
                halign="center",
                size_hint_y=None,
                height="40dp"
            ))

    def proxima_rodada(self):
        self.root.current = 'palavras'
        self.carregar_palavras()

    def novo_jogo(self):
        self.times = []
        self.jogadores = []
        self.pontuacao = {}
        self.current_time = ""
        self.palavra_escolhida = ""
        self.palavras = []
        self.vencedor = ""
        self.time_index = 0
        self.jogador_index = 0
        self.root.current = 'menu'

    def show_dialog(self, text):
        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(text=text, buttons=[MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss())])
        self.dialog.open()

if __name__ == '__main__':
    MimicaApp().run()
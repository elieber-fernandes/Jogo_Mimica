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
    ConfiguracoesScreen:

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

            MDTextButton:
                text: "Configurações"
                pos_hint: {"center_x": .5}
                on_release: app.open_configuracoes()

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

<ConfiguracoesScreen>:
    name: "config"
    MDBoxLayout:
        orientation: "vertical"
        padding: [32, 48, 32, 48]
        spacing: 24

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

            MDLabel:
                text: "Configurações"
                halign: "center"
                font_style: "H5"
                theme_text_color: "Primary"

                
            MDTextField:
                id: duracao_input
                hint_text: "Duração da rodada (segundos)"
                text: str(app.duracao_rodada)
                mode: "rectangle"
                size_hint_x: 0.8
                pos_hint: {"center_x": .5}
                input_filter: "int"

            MDTextField:
                id: opcoes_input
                hint_text: "Número de opções de palavras"
                text: str(app.num_opcoes)
                mode: "rectangle"
                size_hint_x: 0.8
                pos_hint: {"center_x": .5}
                input_filter: "int"

            MDBoxLayout:
                orientation: "horizontal"
                size_hint_y: None
                height: "48dp"
                spacing: 12
                pos_hint: {"center_x": .5}
                MDLabel:
                    text: "Usar palavras online"
                    halign: "left"
                    theme_text_color: "Primary"
                MDSwitch:
                    id: online_switch
                    active: app.usar_online
                    pos_hint: {"center_y": .5}

            MDRaisedButton:
                text: "Salvar"
                pos_hint: {"center_x": .5}
                size_hint_x: 0.6
                radius: [16, 16, 16, 16]
                md_bg_color: app.theme_cls.primary_color
                on_release: app.salvar_configuracoes(duracao_input.text, opcoes_input.text, online_switch.active)

        MDTextButton:
            text: "Voltar"
            pos_hint: {"center_x": .5}
            on_release: app.root.current = "menu"
'''

class MenuScreen(MDScreen): pass
class JogadoresScreen(MDScreen): pass
class PalavrasScreen(MDScreen): pass
class ResultadoScreen(MDScreen): pass
class PlacarScreen(MDScreen): pass
class ConfiguracoesScreen(MDScreen): pass

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
        self.duracao_rodada = 60
        self.num_opcoes = 4
        self.usar_online = True
        self.selected_button = None
        # Lista offline de palavras para fallback
        self.offline_palavras = [
            "casa", "carro", "gato", "cachorro", "livro", "montanha", "praia", "telefone",
            "computador", "janela", "porta", "mesa", "cadeira", "floresta", "rio", "cidade",
            "avião", "bicicleta", "ônibus", "escola", "professor", "aluno", "bola", "música",
            "dança", "pintura", "relógio", "sol", "lua", "estrela", "chuva", "neve", "vento",
            "fogo", "água", "terra", "árvore", "flor", "fruta", "banana", "maçã", "laranja",
            "uva", "melancia", "moto", "camisa", "calça", "sapato", "chapéu", "óculos"
        ]
        return Builder.load_string(KV)

    def go_to_jogadores(self, nome_time):
        if not nome_time.strip():
            self.show_dialog("Digite o nome do time")
            return
        self.current_time = nome_time.strip()
        self.root.get_screen('jogadores').ids.time_label.text = f"Time: {self.current_time}"
        self.root.current = 'jogadores'

    def open_configuracoes(self):
        self.root.current = 'config'

    def salvar_configuracoes(self, duracao_str, opcoes_str, online_active):
        try:
            duracao = int(duracao_str) if duracao_str else self.duracao_rodada
            opcoes = int(opcoes_str) if opcoes_str else self.num_opcoes
        except ValueError:
            self.show_dialog("Valores inválidos. Use números inteiros.")
            return
        # Limites razoáveis
        if duracao < 5:
            duracao = 5
        if opcoes < 2:
            opcoes = 2
        if opcoes > 8:
            opcoes = 8
        self.duracao_rodada = duracao
        self.num_opcoes = opcoes
        self.usar_online = bool(online_active)
        self.show_dialog("Configurações salvas")
        self.root.current = 'menu'

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
        from kivy.clock import Clock
        import threading
        import random

        jogador = self.jogadores[self.time_index][self.jogador_index]
        time = self.times[self.time_index]

        # Atualiza as labels de instrução
        instrucao = self.root.get_screen('palavras').ids.instrucao
        jogador_info = self.root.get_screen('palavras').ids.jogador_info
        instrucao.text = "ESCOLHA UMA PALAVRA!"
        jogador_info.text = f"VEZ DE: {jogador} - ({time})"

        # Estado inicial da UI
        box = self.root.get_screen('palavras').ids.palavras_box
        box.clear_widgets()
        box.add_widget(MDLabel(text="Carregando...", halign="center", size_hint_y=None, height="40dp"))
        self.root.get_screen('palavras').ids.confirmar_btn.disabled = True
        self.palavra_escolhida = ""
        self.selected_button = None

        def fetch_words():
            words = []
            if self.usar_online:
                try:
                    page = requests.get("https://www.palabrasaleatorias.com/palavras-aleatorias.php?fs=4&fs2=0&Submit=Nova+palavra", timeout=5)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    divs = soup.find_all('div')
                    # Coleta textos visíveis e razoáveis
                    candidates = [d.get_text(strip=True) for d in divs if d.get_text(strip=True)]
                    # Remove duplicados mantendo ordem
                    seen = set()
                    for w in candidates:
                        lw = w.lower()
                        if lw not in seen and 2 <= len(lw) <= 20 and lw.isalpha():
                            words.append(lw)
                            seen.add(lw)
                            if len(words) >= self.num_opcoes:
                                break
                except Exception:
                    words = []

            # Complementa com offline se necessário
            if len(words) < self.num_opcoes:
                restantes = self.num_opcoes - len(words)
                offline_pool = [w for w in self.offline_palavras if w not in words]
                if offline_pool:
                    words.extend(random.sample(offline_pool, k=min(restantes, len(offline_pool))))
            # Se ainda faltar, preenche com placeholders
            while len(words) < self.num_opcoes:
                words.append(f"palavra {len(words)+1}")

            def update_ui(_dt):
                box.clear_widgets()
                self.palavras = words
                for palavra in words:
                    btn = MDFlatButton(
                        text=palavra.upper(),
                        font_size="18sp",
                        size_hint_x=0.9,
                        pos_hint={"center_x": .5},
                        on_release=lambda b, p=palavra: self.selecionar_palavra(p, b)
                    )
                    box.add_widget(btn)
                self.root.get_screen('palavras').ids.confirmar_btn.disabled = True
                self.palavra_escolhida = ""

            Clock.schedule_once(update_ui, 0)

        threading.Thread(target=fetch_words, daemon=True).start()

    def selecionar_palavra(self, palavra, btn):
        # Destaque visual simples: altera cor do texto do selecionado
        if getattr(self, 'selected_button', None) is not None:
            try:
                self.selected_button.theme_text_color = "Primary"
            except Exception:
                pass
        try:
            btn.theme_text_color = "Custom"
            btn.text_color = self.theme_cls.primary_color
        except Exception:
            pass
        self.selected_button = btn
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
        

        self.tempo = int(self.duracao_rodada)
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
        # Opção de ninguém acertou
        layout = MDBoxLayout(orientation="horizontal", spacing=8, size_hint_y=None, height="48dp")
        checkbox = MDCheckbox(group="vencedor")
        checkbox.bind(active=partial(self.on_checkbox_active, "__NINGUEM__"))
        layout.add_widget(checkbox)
        layout.add_widget(MDLabel(text="Ninguém acertou", valign="center"))
        box.add_widget(layout)
        # Ajusta a altura do times_box conforme o número de opções
        box.height = (len(self.times) + 1) * 48

    def on_checkbox_active(self, time, instance, value):
        if value:
            self.vencedor = time

    def confirmar_vencedor(self):
        if not self.vencedor:
            self.show_dialog("Selecione o time vencedor")
            return
        if self.vencedor != "__NINGUEM__":
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
        if not self.pontuacao:
            return
        itens_ordenados = sorted(self.pontuacao.items(), key=lambda kv: kv[1], reverse=True)
        max_pontos = itens_ordenados[0][1]
        for time, pontos in itens_ordenados:
            destaque = pontos == max_pontos and max_pontos > 0
            if destaque:
                box.add_widget(MDLabel(
                    text=f"{time}: {pontos} ponto(s)",
                    halign="center",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    size_hint_y=None,
                    height="40dp"
                ))
            else:
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
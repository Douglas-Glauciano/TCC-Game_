# Correções na classe CharacterNameCreator para resolver o problema da tela preta.
# O problema principal era na lógica de seleção de nome, que não estava exibindo
# o menu corretamente após a geração de um nome aleatório.

import curses
import time
import random
import sqlite3
import pyfiglet
from ..base_state import BaseState
from game.name_generator import NameGenerator
from game.config import culturas_comuns, culturas_fantasiosas

class CharacterNameCreator(BaseState):
    """
    Refatoração do CharacterNameCreator para curses e pyfiglet.
    Mantém toda a lógica, apenas muda a exibição/interação.
    """

    def __init__(self, stdscr, cultura_padrao='medieval'):
        self.stdscr = stdscr
        self.cultura_padrao = cultura_padrao
        self.generator = NameGenerator()

        # Mapas de gênero
        self.generos = {'1': 'masc', '2': 'fem', '3': 'neutro'}
        self.genero = None
        self.cultura_selecionada = None

        self.culturas_disponiveis = []
        self.culturas_comuns_filtradas = []
        self.culturas_fantasiosas_filtradas = []

        # Inicializa culturas disponíveis
        self.setup_cultures()

    def setup_cultures(self):
        """Preenche as listas de culturas disponíveis."""
        self.culturas_disponiveis = self.generator.listar_culturas()
        
        if not self.culturas_disponiveis:
            print("Nenhuma cultura encontrada no banco de dados. Usando padrão.")
            self.culturas_disponiveis = ['medieval']
        
        # Normalizar nomes para minúsculas para comparação
        culturas_disponiveis_lower = [c.lower() for c in self.culturas_disponiveis]
        
        def encontrar_nome_original(nome_base):
            for c in self.culturas_disponiveis:
                if c.lower() == nome_base.lower():
                    return c
            return nome_base
        
        # Filtrar e manter a capitalização original
        self.culturas_comuns_filtradas = []
        for c in culturas_comuns:
            if c.lower() in culturas_disponiveis_lower:
                self.culturas_comuns_filtradas.append(encontrar_nome_original(c))
        
        self.culturas_fantasiosas_filtradas = []
        for c in culturas_fantasiosas:
            if c.lower() in culturas_disponiveis_lower:
                self.culturas_fantasiosas_filtradas.append(encontrar_nome_original(c))
        
        # Adicionar culturas não classificadas como fantasiosas
        for c in self.culturas_disponiveis:
            c_lower = c.lower()
            if (c_lower not in [c2.lower() for c2 in self.culturas_comuns_filtradas] and 
                c_lower not in [c2.lower() for c2 in self.culturas_fantasiosas_filtradas]):
                self.culturas_fantasiosas_filtradas.append(c)

    def listar_culturas(self):
        """Retorna todas as culturas disponíveis no banco de dados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT DISTINCT culture FROM name_components")
            culturas = [row['culture'] for row in cursor.fetchall()]
            return culturas
        except sqlite3.Error as e:
            print(f"Erro ao buscar culturas: {e}")
            return ['medieval']  # Fallback padrão
        finally:
            # Não fechar a conexão aqui! 
            pass

    def center_text(self, text, y_offset=0):
        """Exibe texto centralizado na tela."""
        height, width = self.stdscr.getmaxyx()
        x = max((width - len(text)) // 2, 0)
        y = height // 2 + y_offset
        self.stdscr.addstr(y, x, text)
        self.stdscr.refresh()

    def display_title(self, title):
        """Exibe título em ASCII art centralizado (uma linha)"""
        self.stdscr.clear()
        ascii_lines = pyfiglet.figlet_format(title, font="slant", width=200).splitlines()
        height, width = self.stdscr.getmaxyx()
        max_width = max(len(line) for line in ascii_lines)
        start_x = max((width - max_width) // 2, 0)
        start_y = 1
        for i, line in enumerate(ascii_lines):
            if 0 <= start_y + i < height:
                self.stdscr.addstr(start_y + i, start_x, line)
        self.stdscr.refresh()

    def display_menu(self, options, highlight_idx):
        """Exibe lista de opções centralizadas, destacando a selecionada"""
        height, width = self.stdscr.getmaxyx()
        start_y = height // 2
        for idx, option in enumerate(options):
            x = max((width - len(option) - 4) // 2, 0)
            y = start_y + idx
            if idx == highlight_idx:
                self.stdscr.attron(curses.A_REVERSE)
                self.stdscr.addstr(y, x, f"> {option} <")
                self.stdscr.attroff(curses.A_REVERSE)
            else:
                self.stdscr.addstr(y, x, f"  {option}  ")
        self.stdscr.refresh()

    # --- Métodos refatorados para curses ---

    def run(self):
        """Orquestra o fluxo de criação do nome."""
        # Loop principal para a criação do nome
        while True:
            # 1. Seleciona Gênero
            result_gender = self.select_gender()
            if result_gender is False: # Clicou em voltar para o menu principal
                return None
            if result_gender is None: # Clicou em voltar para o passo anterior
                continue
            
            # 2. Seleciona Cultura
            result_culture = self.select_culture()
            if result_culture is False: # Clicou em voltar para o gênero
                continue
            if result_culture is None: # Clicou em voltar para o menu principal
                return None

            # 3. Seleciona o nome
            nome = self.select_name()
            if nome is not None:
                return nome
            
    def select_gender(self):
        """Seleciona gênero usando curses."""
        options = ["Masculino", "Feminino", "Não binário/Outro", "Voltar"]
        idx = 0

        while True:
            self.display_title("Escolha o Gênero")
            self.display_menu(options, idx)

            key = self.stdscr.getch()
            if key in (curses.KEY_UP, ord('w')):
                idx = (idx - 1) % len(options)
            elif key in (curses.KEY_DOWN, ord('s')):
                idx = (idx + 1) % len(options)
            elif key in (curses.KEY_ENTER, 10, 13):
                if idx == 3:  # Voltar
                    return None
                self.genero = self.generos.get(str(idx + 1))
                return True

    def select_culture(self):
        """Seleciona cultura usando curses."""
        options = [
            f"Usar cultura padrão ({self.cultura_padrao})",
            "Escolher cultura comum",
            "Escolher cultura fantástica",
            "Aleatório (qualquer cultura)",
            "Voltar (escolher outro gênero)"
        ]
        idx = 0

        while True:
            self.display_title("Escolha a Cultura")
            self.display_menu(options, idx)

            key = self.stdscr.getch()
            if key in (curses.KEY_UP, ord('w')):
                idx = (idx - 1) % len(options)
            elif key in (curses.KEY_DOWN, ord('s')):
                idx = (idx + 1) % len(options)
            elif key in (curses.KEY_ENTER, 10, 13):
                if idx == 0:
                    self.cultura_selecionada = self.cultura_padrao
                    return True
                elif idx == 1:
                    return self.handle_common_cultures()
                elif idx == 2:
                    return self.handle_fantasy_cultures()
                elif idx == 3:
                    self.cultura_selecionada = None
                    return True
                elif idx == 4:
                    return False

    def handle_common_cultures(self):
        """Seleciona cultura comum usando curses."""
        if not self.culturas_comuns_filtradas:
            self.center_text("Nenhuma cultura comum disponível", -2)
            self.stdscr.getch()
            return False

        options = self.culturas_comuns_filtradas + ["Voltar"]
        idx = 0
        while True:
            self.display_title("Culturas Comuns")
            self.display_menu(options, idx)

            key = self.stdscr.getch()
            if key in (curses.KEY_UP, ord('w')):
                idx = (idx - 1) % len(options)
            elif key in (curses.KEY_DOWN, ord('s')):
                idx = (idx + 1) % len(options)
            elif key in (curses.KEY_ENTER, 10, 13):
                if idx == len(options) - 1:
                    return False
                self.cultura_selecionada = self.culturas_comuns_filtradas[idx]
                return True

    def handle_fantasy_cultures(self):
        """Seleciona cultura fantástica usando curses."""
        if not self.culturas_fantasiosas_filtradas:
            self.center_text("Nenhuma cultura fantástica disponível", -2)
            self.stdscr.getch()
            return False

        options = self.culturas_fantasiosas_filtradas + ["Voltar"]
        idx = 0
        while True:
            self.display_title("Culturas Fantásticas")
            self.display_menu(options, idx)

            key = self.stdscr.getch()
            if key in (curses.KEY_UP, ord('w')):
                idx = (idx - 1) % len(options)
            elif key in (curses.KEY_DOWN, ord('s')):
                idx = (idx + 1) % len(options)
            elif key in (curses.KEY_ENTER, 10, 13):
                if idx == len(options) - 1:
                    return False
                self.cultura_selecionada = self.culturas_fantasiosas_filtradas[idx]
                return True

    def select_name(self):
        """Seleciona ou gera nome usando curses."""
        while True:
            self.stdscr.clear()
            self.display_title("Escolha o Nome")

            # Permite ao usuário digitar manualmente
            self.center_text("Digite o nome ou pressione ENTER para gerar um.", -2)
            height, width = self.stdscr.getmaxyx()
            self.stdscr.move(height//2 - 1, max((width - 40)//2, 0))
            self.stdscr.addstr("Nome: ")
            
            curses.echo()
            curses.curs_set(1)
            self.stdscr.refresh()
            entrada = self.stdscr.getstr().decode('utf-8').strip()
            curses.noecho()
            curses.curs_set(0)
            
            if entrada:
                return entrada

            # Se a entrada for vazia, gera um nome aleatório
            cultura_ativa = self.cultura_selecionada or random.choice(self.culturas_disponiveis)
            try:
                nome_base = self.generator.gerar_nome_base(self.genero, cultura_ativa)
            except Exception:
                nome_base = "Nome Desconhecido"

            # Exibe o menu para decidir o que fazer com o nome gerado
            options = [
                f"Usar este nome ({nome_base})",
                "Gerar outro nome",
                "Digitar nome manualmente"
            ]
            idx = 0
            
            while True:
                self.display_title("Nome Gerado")
                self.center_text(f"Cultura: {cultura_ativa.capitalize()}", -4)
                self.display_menu(options, idx)

                key = self.stdscr.getch()
                if key in (curses.KEY_UP, ord('w')):
                    idx = (idx - 1) % len(options)
                elif key in (curses.KEY_DOWN, ord('s')):
                    idx = (idx + 1) % len(options)
                elif key in (curses.KEY_ENTER, 10, 13):
                    if idx == 0:
                        return nome_base
                    elif idx == 1:
                        # Sai do loop interno e volta para o loop de seleção de nome para gerar outro
                        break
                    elif idx == 2:
                        # Retorna None para o loop externo para que o input manual seja solicitado
                        return None

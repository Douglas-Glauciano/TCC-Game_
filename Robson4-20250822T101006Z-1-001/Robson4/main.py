# main.py - Corrigido para funcionar com os estados atualizados
import curses
import os
import sys
import sqlite3
import traceback
from datetime import datetime
from game.config import get_db_path
from game.i18n.translator import translator as t
from states.system.main_menu_state import MainMenuState
from states.creation.character_creation_state import CharacterCreationState

# Adiciona o diretório raiz ao PATH do Python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# DEFINA O TAMANHO MÍNIMO REQUERIDO AQUI
MIN_LINHAS = 35
MIN_COLUNAS = 100

class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.running = True
        self.states = []
        self.player = None
        self.db_conn = None
        self.needs_render = True

        # Configurações do curses (uma vez só)
        curses.curs_set(0)
        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()

    def change_state(self, new_state):
        while self.states:
            state = self.states.pop()
            if hasattr(state, 'exit'):
                state.exit()
        self.push_state(new_state)

    def push_state(self, state):
        if self.states:
            current_state = self.states[-1]
            if hasattr(current_state, 'exit'):
                current_state.exit()
        self.states.append(state)
        if hasattr(state, 'enter'):
            state.enter()
        self.needs_render = True

    def pop_state(self):
        if self.states:
            state = self.states.pop()
            if hasattr(state, 'exit'):
                state.exit()
        if self.states:
            top_state = self.states[-1]
            if hasattr(top_state, 'enter'):
                top_state.enter()
        self.needs_render = True

    def current_state(self):
        return self.states[-1] if self.states else None

    def run(self):
        try:
            # VERIFICA O TAMANHO DA TELA ANTES DE QUALQUER COISA
            self.verificar_tamanho_tela()
            
            self.db_conn = sqlite3.connect(get_db_path())
            self.change_state(MainMenuState(self))

            while self.running:
                current_state = self.current_state()
                if not current_state:
                    continue

                if self.needs_render:
                    self.stdscr.clear()
                    current_state.render(self.stdscr) 
                    self.stdscr.refresh()
                    self.needs_render = False

                current_state.handle_input()

        except KeyboardInterrupt:
            self.running = False
        except Exception as e:
            self.stdscr.keypad(False)
            curses.endwin()
            print("\n" + t.t("critical_error_header"))
            print(t.t("critical_error_details", error=str(e)))
            print(t.t("check_log_message"))
            with open("error_log.txt", "a") as f:
                f.write(f"\n\n[{datetime.now()}] CRITICAL ERROR\n")
                f.write(f"Error: {str(e)}\n")
                f.write(traceback.format_exc())
                f.write("\n" + "="*50 + "\n")
            input(t.t("press_enter_exit"))
        finally:
            if self.db_conn:
                self.db_conn.close()
            print("\n" + t.t("goodbye_message"))

    def verificar_tamanho_tela(self):
        """Verifica se o terminal tem o tamanho mínimo necessário"""
        linhas, colunas = self.stdscr.getmaxyx()
        if linhas < MIN_LINHAS or colunas < MIN_COLUNAS:
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, "TAMANHO DE TELA INSUFICIENTE")
            self.stdscr.addstr(1, 0, f"Requerido: {MIN_COLUNAS}x{MIN_LINHAS}")
            self.stdscr.addstr(2, 0, f"Atual: {colunas}x{linhas}")
            self.stdscr.addstr(3, 0, "Por favor, aumente o tamanho do terminal")
            self.stdscr.addstr(4, 0, "ou diminua o zoom/fonte e reinicie o jogo.")
            self.stdscr.addstr(5, 0, "Pressione qualquer tecla para sair.")
            self.stdscr.refresh()
            self.stdscr.getch()
            sys.exit(1)

    def quit(self):
        self.running = False

def main(stdscr):
    game = Game(stdscr)
    game.run()

if __name__ == "__main__":
    curses.wrapper(main)
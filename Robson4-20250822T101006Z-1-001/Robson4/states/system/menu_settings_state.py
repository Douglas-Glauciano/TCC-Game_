# menu_settings_state.py - Versão simplificada e corrigida
import curses
import pyfiglet
from ..base_state import BaseState
from game.i18n.translator import translator as t

class SettingsState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.menu_options = [
            t.t('settings_language'),
            t.t('settings_back')
        ]
        self.language_options = [
            t.t('language_pt'),
            t.t('language_en')
        ]
        self.current_lang = t.get_current_language_name()
        self.is_language_menu = False

    def _render_title(self, stdscr, title_text):
        """Renderiza o título em ASCII art centralizado"""
        height, width = stdscr.getmaxyx()
        ascii_lines = pyfiglet.figlet_format(title_text, font="slant", width=200).splitlines()
        
        for i, line in enumerate(ascii_lines):
            x = max((width - len(line)) // 2, 0)
            if i < height:
                stdscr.addstr(i, x, line)
        
        return len(ascii_lines)

    def render(self, stdscr):
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if self.is_language_menu:
            # Renderiza o menu de idiomas
            title = f"{t.t('language_options')} | {t.t('current_language')}: {self.current_lang}"
            title_height = self._render_title(stdscr, title)
            
            # Renderiza as opções de idioma
            menu_start_y = title_height + 2
            for i, option in enumerate(self.language_options):
                x = (width - len(option)) // 2
                y = menu_start_y + i
                if y < height:
                    if i == self.current_selection:
                        stdscr.attron(curses.A_REVERSE)
                        stdscr.addstr(y, x, f"> {option} <")
                        stdscr.attroff(curses.A_REVERSE)
                    else:
                        stdscr.addstr(y, x, f"  {option}  ")
        else:
            # Renderiza o menu principal de configurações
            title = f"{t.t('settings_title')} | {t.t('current_language')}: {self.current_lang}"
            title_height = self._render_title(stdscr, title)
            
            # Renderiza as opções do menu
            menu_start_y = title_height + 2
            for i, option in enumerate(self.menu_options):
                x = (width - len(option)) // 2
                y = menu_start_y + i
                if y < height:
                    if i == self.current_selection:
                        stdscr.attron(curses.A_REVERSE)
                        stdscr.addstr(y, x, f"> {option} <")
                        stdscr.attroff(curses.A_REVERSE)
                    else:
                        stdscr.addstr(y, x, f"  {option}  ")

        stdscr.refresh()

    def handle_input(self):
        """Processa a entrada do usuário."""
        key = self.stdscr.getch()
        
        if self.is_language_menu:
            # Lógica para o menu de idiomas
            if key in (curses.KEY_UP, ord('w')):
                self.current_selection = (self.current_selection - 1) % len(self.language_options)
                self.game.needs_render = True
            elif key in (curses.KEY_DOWN, ord('s')):
                self.current_selection = (self.current_selection + 1) % len(self.language_options)
                self.game.needs_render = True
            elif key in (curses.KEY_ENTER, 10, 13):
                self.execute_choice()
                self.game.needs_render = True
            elif key == 27:  # ESC key
                self.is_language_menu = False
                self.current_selection = 0
                self.game.needs_render = True
        else:
            # Lógica para o menu principal
            if key in (curses.KEY_UP, ord('w')):
                self.current_selection = (self.current_selection - 1) % len(self.menu_options)
                self.game.needs_render = True
            elif key in (curses.KEY_DOWN, ord('s')):
                self.current_selection = (self.current_selection + 1) % len(self.menu_options)
                self.game.needs_render = True
            elif key in (curses.KEY_ENTER, 10, 13):
                self.execute_choice()
                self.game.needs_render = True
            elif key == 27:  # ESC key
                self.game.pop_state()

    def execute_choice(self):
        """Executa a escolha do menu com base na seleção atual."""
        if self.is_language_menu:
            # Menu de seleção de idioma
            if self.current_selection == 0:
                t.set_language("pt-br")
            elif self.current_selection == 1:
                t.set_language("en-us")
            
            # Atualiza o nome do idioma atual
            self.current_lang = t.get_current_language_name()
            
            # Atualiza as opções do menu com o novo idioma
            self.menu_options = [
                t.t('settings_language'),
                t.t('settings_back')
            ]
            self.language_options = [
                t.t('language_pt'),
                t.t('language_en')
            ]
            
            # Volta para o menu principal de configurações
            self.is_language_menu = False
            self.current_selection = 0
            
        else:
            # Menu principal de configurações
            if self.current_selection == 0:
                # Entra no menu de idiomas
                self.is_language_menu = True
                self.current_selection = 0
            elif self.current_selection == 1:
                # Volta ao menu anterior
                self.game.pop_state()
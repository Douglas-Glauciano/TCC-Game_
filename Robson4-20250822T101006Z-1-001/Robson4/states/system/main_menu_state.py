
# MainMenuState.py - Agora muito mais limpo!
# A lógica de navegação foi removida e o código ficou mais focado no menu em si.
import curses
from ..base_state import BaseState
from states.creation.character_creation_state import CharacterCreationState
from .save_manager_state import SaveManagerState
from .menu_settings_state import SettingsState
from game.i18n.translator import translator as t
import pyfiglet

class MainMenuState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        
        # As opções de menu ainda são específicas para este estado.
        self.menu_options = [
            t.t('main_menu_option_continue'),
            t.t('main_menu_option_new_game'),
            t.t('main_menu_option_saves'),
            t.t('main_menu_option_tutorial'),
            t.t('main_menu_option_credits'),
            t.t('main_menu_option_settings'),
            t.t('main_menu_option_exit')
        ]
        
        # O self.current_selection não precisa mais ser inicializado aqui,
        # pois o BaseState já cuida disso.

        text = "Rust Dice"
        self.ascii_art_lines = pyfiglet.figlet_format(text, font="slant", width=200).splitlines()

    def render(self, stdscr):
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        max_width = max(len(line) for line in self.ascii_art_lines)
        start_x = max((width - max_width) // 2, 0)
        start_y = 1
        for i, line in enumerate(self.ascii_art_lines):
            if 0 <= start_y + i < height:
                stdscr.addstr(start_y + i, start_x, line)

        menu_start_y = start_y + len(self.ascii_art_lines) + 2
        for i, option in enumerate(self.menu_options):
            x = max((width - len(option) - 4) // 2, 0)
            if i == self.current_selection:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(menu_start_y + i, x, f"> {option} <")
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(menu_start_y + i, x, f"  {option}  ")

        stdscr.refresh()

    def execute_choice(self):
        """Sobrescreve o método do BaseState para definir o comportamento de cada opção."""
        choice = self.current_selection
        if choice == 0:
            self.show_message_and_wait(t.t("feature_not_implemented", feature=t.t('main_menu_option_continue')))
        elif choice == 1:
            self.game.change_state(CharacterCreationState(self.game))
        elif choice == 2:
            self.game.change_state(SaveManagerState(self.game))
        elif choice == 3:
            from .tutorial_state import TutorialState
            self.game.push_state(TutorialState(self.game))
        elif choice == 4:  # Opção de créditos
            from .credits_state import CreditsState
            self.game.push_state(CreditsState(self.game))
        elif choice == 5:
            # Usa push_state em vez de change_state para adicionar à pilha
            self.game.push_state(SettingsState(self.game))
        elif choice == 6:
            self.show_message_and_wait(t.t("main_menu_exit_message"))
            self.game.quit()

    def show_message_and_wait(self, message):
        height, width = self.stdscr.getmaxyx()
        y = height // 2
        x = max((width - len(message)) // 2, 0)
        self.stdscr.addstr(y, x, message)
        self.stdscr.refresh()
        self.stdscr.getch()
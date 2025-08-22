# game/states/settings_state.py
from ..base_state import BaseState
from game.database import save_character
from game.i18n.translator import translator as t  # Importar tradutor
import os

class SettingsState(BaseState):
    def enter(self):
        # Opções traduzidas
        self.options = [
            (t.t("settings_change_difficulty"), "change_difficulty"),
            (t.t("settings_change_language"), "change_language"),  # Nova opção
            (t.t("settings_back"), "back"),
            (t.t("settings_save_continue"), "save_continue"),
            (t.t("settings_save_exit"), "save_exit"),
            (t.t("settings_delete_character"), "delete_character")
        ]
        
    def render(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*30)
        print(t.t("settings_title"))  # Título traduzido
        print("="*30)
        
        for i, (name, _) in enumerate(self.options, 1):
            print(f"{i}. {name}")
        
    def handle_input(self):
        choice = input("\n" + t.t("enter_choice_prompt")).strip()
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(self.options):
                action = self.options[index][1]
                if action == "change_difficulty":
                    self.change_difficulty()
                elif action == "change_language":  # Nova ação
                    self.change_language()
                elif action == "back":
                    from ..world.gameplay_state import GameplayState
                    self.game.change_state(GameplayState(self.game))
                elif action == "save_continue":
                    save_character(self.game.db_conn, self.game.player)
                    print("\n" + t.t("settings_save_success"))
                    input(t.t("press_enter_continue"))
                elif action == "save_exit":
                    save_character(self.game.db_conn, self.game.player)
                    print("\n" + t.t("settings_save_exit_message"))
                    from .main_menu_state import MainMenuState
                    self.game.change_state(MainMenuState(self.game))
                elif action == "delete_character":
                    from .delete_confirmation_state import DeleteConfirmationState
                    self.game.change_state(DeleteConfirmationState(self.game))
            else:
                print("\n" + t.t("invalid_option"))
                input(t.t("press_enter_continue"))
        except ValueError:
            print("\n" + t.t("invalid_input"))
            input(t.t("press_enter_continue"))
    
    def change_difficulty(self):
        from .difficulty_state import DifficultyState
        self.game.push_state(DifficultyState(self.game))
    
    def change_language(self):  # Nova função
        from .language_settings_state import LanguageSettingsState
        self.game.push_state(LanguageSettingsState(self.game))
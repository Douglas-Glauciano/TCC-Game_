# game/states/system/language_settings_state.py
from ..base_state import BaseState
from game.i18n.translator import translator as t

class LanguageSettingsState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
    
    def enter(self):
        self.game.needs_render = True
    
    def render(self):
        # Obter nome do idioma atual
        current_lang = t.get_current_language_name()
        title = f"{t.t('language_settings_title')} | {t.t('current_language')}: {current_lang}"
        
        print("\n" + "="*50)
        print(title)
        print("="*50)
        print(f"1. {t.t('language_pt')}")
        print(f"2. {t.t('language_en')}")
        print(f"3. {t.t('back')}")
        print("="*50)

    def handle_input(self):
        choice = input("\n" + t.t("enter_choice_prompt")).strip()
        
        if choice == "1":
            t.set_language("pt-br")
            self.game.needs_render = True
            print("\n" + t.t("language_changed"))
            input(t.t("press_enter_continue"))
            self.render()  # Re-renderizar com novo idioma
        elif choice == "2":
            t.set_language("en-us")
            self.game.needs_render = True
            print("\n" + t.t("language_changed"))
            input(t.t("press_enter_continue"))
            self.render()  # Re-renderizar com novo idioma
        elif choice == "3":
            self.game.pop_state()  # Volta para o menu anterior
        else:
            print("\n" + t.t("invalid_option"))
            input(t.t("press_enter_continue"))
            self.render()
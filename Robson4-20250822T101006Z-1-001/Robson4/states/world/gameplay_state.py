# game/states/gameplay_state.py
from ..base_state import BaseState
from game.database import save_character
from game.utils import get_display_name, calculate_enhanced_damage, calculate_enhanced_armor_bonus
import curses

class GameplayState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.menu_options = [
            "Explorar area (encontrar monstros e tesouros)",
            "Descansar (recuperar vida e mana)",
            "Viajar para outra regiao",
            "Ver Atributos detalhados",
            "Abrir inventario",
            "Configuracoes"
        ]
        self.scrollable = False  # Desativar rolagem pois não é necessária aqui

    def enter(self):
        """Executado ao entrar no estado Gameplay"""
        self.game.needs_render = True

    def render(self, stdscr):
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        player = self.game.player
        player.recalculate()
        
        # Cálculos para barras de HP e Mana
        hp_percent = min(100, int((player.hp / player.hp_max) * 100))
        mana_percent = min(100, int((player.mana / player.mana_max) * 100)) if player.mana_max > 0 else 0
        
        # Centralizar conteúdo
        content_width = min(60, width - 4)  # Largura máxima do conteúdo
        left_margin = (width - content_width) // 2
        
        # Informações básicas do personagem
        separator = "=" * content_width
        stdscr.addstr(0, left_margin, separator, curses.A_BOLD)
        title = f"AVENTURA DE {player.name.upper()}"
        stdscr.addstr(1, left_margin + (content_width - len(title)) // 2, title, curses.A_BOLD)
        stdscr.addstr(2, left_margin, separator, curses.A_BOLD)
        
        row = 3
        info_line = f"Raca: {player.race} | Classe: {player.char_class} | Nivel: {player.level}"
        stdscr.addstr(row, left_margin + (content_width - len(info_line)) // 2, info_line)
        row += 1
        
        exp_line = f"EXP: {player.exp}/{player.exp_max}"
        stdscr.addstr(row, left_margin + (content_width - len(exp_line)) // 2, exp_line)
        row += 1
        
        gold_line = f"Ouro: {player.gold}"
        stdscr.addstr(row, left_margin + (content_width - len(gold_line)) // 2, gold_line)
        row += 1
        
        # Barra de HP
        hp_text = f"Vida: {player.hp}/{player.hp_max}"
        stdscr.addstr(row, left_margin + (content_width - len(hp_text)) // 2, hp_text)
        row += 1
        
        bar_width = min(30, content_width)
        filled = (hp_percent * bar_width) // 100
        hp_bar_visual = "[" + "#" * filled + "." * (bar_width - filled) + f"] {hp_percent}%"
        bar_left_margin = left_margin + (content_width - len(hp_bar_visual)) // 2
        stdscr.addstr(row, bar_left_margin, hp_bar_visual)
        row += 1
        
        # Barra de Mana (se aplicável)
        if player.mana_max > 0:
            mana_text = f"Mana: {player.mana}/{player.mana_max}"
            stdscr.addstr(row, left_margin + (content_width - len(mana_text)) // 2, mana_text)
            row += 1
            
            filled_mana = (mana_percent * bar_width) // 100
            mana_bar_visual = "[" + "#" * filled_mana + "." * (bar_width - filled_mana) + f"] {mana_percent}%"
            bar_left_margin = left_margin + (content_width - len(mana_bar_visual)) // 2
            stdscr.addstr(row, bar_left_margin, mana_bar_visual)
            row += 1
        
        # Equipamentos
        equipped_items = player.get_equipped_items()
        weapon = next((item for item in equipped_items if item.get('category') == 'weapon' and item.get('equip_slot') == 'main_hand'), None)
        armor = next((item for item in equipped_items if item.get('category') == 'armor' and item.get('equip_slot') == 'body'), None)
        shield = next((item for item in equipped_items if item.get('category') == 'shield' and item.get('equip_slot') == 'off_hand'), None)
        
        physical_res = player.get_physical_resistance()
        magical_res = player.get_magical_resistance()
        dex_penalty = player.get_dexterity_penalty()
        
        row += 1
        stdscr.addstr(row, left_margin, "-" * content_width)
        row += 1
        equipment_title = "EQUIPAMENTO PRINCIPAL"
        stdscr.addstr(row, left_margin + (content_width - len(equipment_title)) // 2, equipment_title, curses.A_BOLD)
        row += 1
        stdscr.addstr(row, left_margin, "-" * content_width)
        row += 1
        
        # Arma
        if weapon:
            display_name = get_display_name(weapon)
            enhanced_damage_str = calculate_enhanced_damage(weapon)
            damage_info = f"{enhanced_damage_str} {weapon.get('damage_type', '')}"
            enhancement_level = weapon.get('enhancement_level', 0)
            enhancement_str = f" (+{enhancement_level})" if enhancement_level > 0 else ""
            weapon_line = f"Arma: {display_name} ({damage_info}{enhancement_str})"
            stdscr.addstr(row, left_margin + (content_width - len(weapon_line)) // 2, weapon_line)
        else:
            weapon_line = "Arma: Punhos (1d4 impacto)"
            stdscr.addstr(row, left_margin + (content_width - len(weapon_line)) // 2, weapon_line)
        row += 1
        
        # Armadura
        if armor:
            display_name = get_display_name(armor)
            physical = armor.get('physical_resistance', 0)
            magical = armor.get('magical_resistance', 0)
            penalty = armor.get('dexterity_penalty', 0)
            enhancement_level = armor.get('enhancement_level', 0)
            enhancement_str = f" (+{enhancement_level})" if enhancement_level > 0 else ""
            
            armor_line = f"Armadura: {display_name}{enhancement_str}"
            stdscr.addstr(row, left_margin + (content_width - len(armor_line)) // 2, armor_line)
            row += 1
            
            res_line = f"Resistencia Fisica: {physical} | Resistencia Magica: {magical}"
            stdscr.addstr(row, left_margin + (content_width - len(res_line)) // 2, res_line)
        else:
            armor_line = "Armadura: Nenhuma"
            stdscr.addstr(row, left_margin + (content_width - len(armor_line)) // 2, armor_line)
        row += 1
        
        # Escudo
        if shield:
            display_name = get_display_name(shield)
            shield_bonus = calculate_enhanced_armor_bonus(shield)
            enhancement_level = shield.get('enhancement_level', 0)
            enhancement_str = f" (+{enhancement_level})" if enhancement_level > 0 else ""
            shield_line = f"Escudo: {display_name} (CA +{shield_bonus}{enhancement_str})"
            stdscr.addstr(row, left_margin + (content_width - len(shield_line)) // 2, shield_line)
        else:
            shield_line = "Escudo: Nenhum"
            stdscr.addstr(row, left_margin + (content_width - len(shield_line)) // 2, shield_line)
        row += 1
        
        penalty_line = f"Penalidade Destreza Total: {dex_penalty}"
        stdscr.addstr(row, left_margin + (content_width - len(penalty_line)) // 2, penalty_line)
        row += 2
        
        # Localização atual
        location = self._get_current_location()
        stdscr.addstr(row, left_margin, separator)
        row += 1
        location_title = f"{location.upper()} - ACOES"
        stdscr.addstr(row, left_margin + (content_width - len(location_title)) // 2, location_title, curses.A_BOLD)
        row += 1
        stdscr.addstr(row, left_margin, separator)
        row += 1
        
        # Menu de opções
        for idx, option in enumerate(self.menu_options):
            option_text = f"> {option}" if idx == self.current_selection else f"  {option}"
            stdscr.addstr(row, left_margin + (content_width - len(option)) // 2 - 1, option_text, 
                         curses.A_REVERSE if idx == self.current_selection else curses.A_NORMAL)
            row += 1
        
        # Instruções de navegação
        instructions = "Seta Cima/Baixo ou W/S: Navegar  Enter: Selecionar  ESC: Voltar"
        stdscr.addstr(height - 1, (width - len(instructions)) // 2, instructions, curses.A_DIM)

    def handle_input(self):
        """Processa a entrada do usuário com suporte a setas e WASD."""
        key = self.stdscr.getch()
        
        # Navegação com setas ou WASD
        if key in (curses.KEY_UP, ord('w'), ord('W')):
            self.current_selection = (self.current_selection - 1) % len(self.menu_options)
            self.game.needs_render = True
        elif key in (curses.KEY_DOWN, ord('s'), ord('S')):
            self.current_selection = (self.current_selection + 1) % len(self.menu_options)
            self.game.needs_render = True
        elif key in (curses.KEY_ENTER, 10, 13):  # Enter
            self.execute_choice()
            self.game.needs_render = True
        elif key == 27:  # Tecla ESC
            self.handle_escape()
            self.game.needs_render = True

    def handle_escape(self):
        """Volta para o menu principal quando ESC é pressionado."""
        from ..system.main_menu_state import MainMenuState
        self.game.change_state(MainMenuState(self.game))

    def execute_choice(self):
        choice = self.current_selection
        
        if choice == 0:
            from .explore_state import ExploreState
            self.game.push_state(ExploreState(self.game))
        elif choice == 1:
            from .rest_state import RestState
            self.game.push_state(RestState(self.game))
        elif choice == 2:
            self._handle_travel()
        elif choice == 3:
            from ..character.attributes_state import AttributesState
            self.game.push_state(AttributesState(self.game))
        elif choice == 4:
            from ..character.inventory_state import InventoryState
            self.game.push_state(InventoryState(self.game))
        elif choice == 5:
            from ..system.ingame_settings_state import SettingsState
            self.game.push_state(SettingsState(self.game))

    def _handle_travel(self):
        from .travel_state import TravelState
        self.game.push_state(TravelState(self.game))

    def _get_current_location(self):
        locations = {
            "forest": "Floresta Sombria",
            "mountains": "Montanhas Gelidas",
            "plains": "Planicies Ventosas",
            "lindenrock": "Lindenrock",
            "vallengar": "Vallengar"
        }
        return locations.get(self.game.player.location, "Regiao Desconhecida")
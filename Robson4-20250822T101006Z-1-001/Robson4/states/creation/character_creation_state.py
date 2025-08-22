# character_creation_state.py - Refatorado para usar o BaseState corretamente
import os
import curses
import traceback
import pyfiglet
from game.character import Character
from game.config import DIFFICULTY_MODIFIERS
from game.database import save_character
from game.db_queries import (
    get_background_starting_skills,
    get_item_base_details,
    load_backgrounds,
    load_classes,
    load_races,
)
from game.utils import roll_attribute
from ..base_state import BaseState
from .character_name_creator_state import CharacterNameCreator
from game.i18n.translator import translator as t

# Mapeia as opções de entrada do usuário para os nomes dos atributos
attr_map = {
    "0": "back",
    "1": "strength", "for": "strength",
    "2": "dexterity", "des": "dexterity",
    "3": "constitution", "con": "constitution",
    "4": "intelligence", "int": "intelligence",
    "5": "wisdom", "sab": "wisdom",
    "6": "charisma", "car": "charisma"
}

# Mapeamento de títulos para cada etapa
STEP_TITLES = {
    "name": "Criar Nome",
    "difficulty": "Dificuldade",
     "difficulty_details": "Detalhes da Dificuldade",
    "permadeath": "Morte Permanente",
    "race": "Escolher Raça",
    "class": "Escolher Classe",
    "background": "Escolher Antecedente",
    "attributes": "Atributos",
    "attribute_reroll": "Rerolar Atributos",
    "complete": "Personagem Completo",
    "overview": "Visão Geral do Personagem"
}

class CharacterCreationState(BaseState):
    """
    Estado de jogo responsável por guiar o usuário através da criação de um novo personagem.
    Agora usa a lógica de menu da classe BaseState.
    """

    def __init__(self, game):
        super().__init__(game)
        self.step = "name"  # Começa com a criação de nome
        self.character_data = {}
        self.races = load_races()
        self.classes = load_classes()
        self.backgrounds = load_backgrounds(self.game.db_conn)
        self.temp_character = None
        self.db_conn = self.game.db_conn
        self.feedback_message = ""
        self.difficulty_options = [
            "Aventura Leve", "Desafio Justo", "Provação Maldita",
            "Caminho da Dor", "Maldição de Ferro", "Inferno Vivo"
        ]
        self.permadeath_options = [
            t.t('permadeath_on'), t.t('permadeath_off')
        ]
        self.permadeath = self.permadeath_options[0]
        self.difficulty = self.difficulty_options[1]
        self.name_creator = None
        self.menu_options = []  # A lista de opções será populada em render()
        
    # ================================
    # RENDERIZAÇÃO DE DETALHES
    # ================================
    def _render_simple_prompt(self, stdscr, text, height, width, offset_y=2):
        """Exibe um texto simples centralizado, sem ASCII art, acima do menu."""
        x = (width - len(text)) // 2
        y = offset_y
        if y < height:
            stdscr.addstr(y, x, text, curses.A_BOLD)

    # --- Atualizando métodos de renderização de detalhes ---

    def _render_character_overview(self, stdscr, height, width):
        """Renderiza uma visão geral completa do personagem com layout em colunas"""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Verifica se a tela é grande o suficiente
        if height < 30 or width < 80:
            error_msg = "Tela muito pequena. Redimensione para pelo menos 80x30."
            stdscr.addstr(0, 0, error_msg)
            return
        
        # Título em ASCII art
        title_text = "Visao Geral do Personagem"  # Removido caractere especial
        ascii_title_lines = pyfiglet.figlet_format(title_text, font="slant", width=min(200, width)).splitlines()
        title_height = len(ascii_title_lines)
        for i, line in enumerate(ascii_title_lines):
            x = max((width - len(line)) // 2, 0)
            if i < height:
                stdscr.addstr(i, x, line, curses.A_BOLD)
        
        # Calcula a divisão da tela em colunas
        col_width = width // 2 - 2  # Largura de cada coluna com margem
        
        # Coluna da esquerda - Informações básicas e atributos
        left_col_x = 2
        right_col_x = width // 2 + 2
        
        # Posição vertical inicial para o conteúdo
        content_start_y = title_height + 2
        
        # Informações básicas (coluna esquerda) - com verificações
        if content_start_y < height:
            stdscr.addstr(content_start_y, left_col_x, "INFORMACOES BASICAS", curses.A_BOLD | curses.A_UNDERLINE)
        
        info_lines = [
            f"Nome: {self.temp_character.name}",
            f"Raca: {self.temp_character.race}",  # Removido caractere especial
            f"Classe: {self.temp_character.char_class}",
            f"Antecedente: {self.temp_character.background}",
            f"Dificuldade: {self.difficulty}",
            f"Morte Permanente: {'Ativada' if self.permadeath == self.permadeath_options[0] else 'Desativada'}"
        ]
        
        for i, line in enumerate(info_lines):
            y = content_start_y + i + 1
            if y < height and left_col_x + len(line) < width:
                stdscr.addstr(y, left_col_x, line)
        
        # Atributos (coluna esquerda)
        attr_start_y = content_start_y + 8
        if attr_start_y < height:
            stdscr.addstr(attr_start_y, left_col_x, "ATRIBUTOS", curses.A_BOLD | curses.A_UNDERLINE)
        
        attr_lines = [
            f"Forca: {self.temp_character.strength} ({self.temp_character.strength_modifier:+#d})",  # Removido caractere especial
            f"Destreza: {self.temp_character.dexterity} ({self.temp_character.dexterity_modifier:+#d})",
            f"Constituicao: {self.temp_character.constitution} ({self.temp_character.constitution_modifier:+#d})",  # Removido caractere especial
            f"Inteligencia: {self.temp_character.intelligence} ({self.temp_character.intelligence_modifier:+#d})",  # Removido caractere especial
            f"Sabedoria: {self.temp_character.wisdom} ({self.temp_character.wisdom_modifier:+#d})",
            f"Carisma: {self.temp_character.charisma} ({self.temp_character.charisma_modifier:+#d})"
        ]
        
        for i, line in enumerate(attr_lines):
            y = attr_start_y + i + 1
            if y < height and left_col_x + len(line) < width:
                stdscr.addstr(y, left_col_x, line)
        
        # Coluna da direita - Combate, equipamento e perícias
        # Informações de combate
        combat_start_y = content_start_y
        if combat_start_y < height and right_col_x + len("COMBATE") < width:
            stdscr.addstr(combat_start_y, right_col_x, "COMBATE", curses.A_BOLD | curses.A_UNDERLINE)
        
        combat_lines = [
            f"HP: {self.temp_character.hp}/{self.temp_character.hp_max}",
            f"Mana: {self.temp_character.mana}/{self.temp_character.mana_max}" if self.temp_character.mana_max > 0 else None,
            f"CA: {self.temp_character.ac}",
            f"Res. Fisica: {self.temp_character.physical_resistance}",  # Removido caractere especial
            f"Res. Magica: {self.temp_character.magical_resistance}"  # Removido caractere especial
        ]
        
        combat_y = combat_start_y + 1
        for line in combat_lines:
            if line and combat_y < height and right_col_x + len(line) < width:
                stdscr.addstr(combat_y, right_col_x, line)
                combat_y += 1
        
        # Itens equipados
        equipment_start_y = combat_start_y + 7
        if equipment_start_y < height and right_col_x + len("EQUIPAMENTO") < width:
            stdscr.addstr(equipment_start_y, right_col_x, "EQUIPAMENTO", curses.A_BOLD | curses.A_UNDERLINE)
        
        equipped_items = self.temp_character.get_equipped_items()
        equip_y = equipment_start_y + 1
        if equipped_items:
            for item in equipped_items:
                enhancement_level = item.get('enhancement_level', 0)
                enh_text = f" +{enhancement_level}" if enhancement_level > 0 else ""
                item_text = f"{item['name']}{enh_text} ({item['category']})"
                
                # Trunca o texto se for muito longo
                if len(item_text) > col_width - 2:
                    item_text = item_text[:col_width - 5] + "..."
                
                if equip_y < height and right_col_x + len(item_text) < width:
                    stdscr.addstr(equip_y, right_col_x, item_text)
                    equip_y += 1
        else:
            if equip_y < height and right_col_x + len("Nenhum item equipado") < width:
                stdscr.addstr(equip_y, right_col_x, "Nenhum item equipado")
                equip_y += 1
        
        # Perícias
        skills_start_y = equip_y + 2
        if skills_start_y < height and right_col_x + len("PERICIAS") < width:
            stdscr.addstr(skills_start_y, right_col_x, "PERICIAS", curses.A_BOLD | curses.A_UNDERLINE)  # Removido caractere especial
        
        skills = self.temp_character.get_all_skills()
        skill_y = skills_start_y + 1
        if skills:
            for skill in skills:
                if skill['level'] > 0:
                    skill_text = f"{skill['skill_name']}: Nivel {skill['level']}"  # Removido caractere especial
                    
                    # Trunca o texto se for muito longo
                    if len(skill_text) > col_width - 2:
                        skill_text = skill_text[:col_width - 5] + "..."
                    
                    if skill_y < height and right_col_x + len(skill_text) < width:
                        stdscr.addstr(skill_y, right_col_x, skill_text)
                        skill_y += 1
                    
                    # Limita o número de perícias exibidas para não ultrapassar a tela
                    if skill_y >= height - 3:
                        break
        
        # Botão de continuar (centralizado na parte inferior)
        continue_text = "Pressione ENTER para começar a jogar"
        continue_y = height - 3
        continue_x = max((width - len(continue_text)) // 2, 0)
        
        if continue_y < height and continue_x + len(continue_text) < width:
            stdscr.addstr(continue_y, continue_x, continue_text, curses.A_REVERSE)
        
        self.menu_options = []
        
    def _render_attribute_options_curses(self, stdscr, height, width):
        self.menu_options = [
            t.t('attributes_keep_and_finalize'),
            t.t('attributes_reroll_all'),
            t.t('attributes_reroll_one'),
            t.t('back_to_background')
        ]
        
        if self.temp_character:
            # Obtém a string de atributos
            attr_str = self.temp_character.show_attributes_string()
            
            # Divide a string em linhas
            attr_lines = attr_str.split('\n')
            
            # Calcula a posição para centralizar
            start_y = 5
            for i, line in enumerate(attr_lines):
                if start_y + i < height - len(self.menu_options) - 2:  # Deixa espaço para o menu
                    x = max((width - len(line)) // 2, 0)
                    stdscr.addstr(start_y + i, x, line)

    def _render_difficulty_details(self, stdscr, height, width):
        self._render_simple_prompt(stdscr, "Selecione uma Dificuldade para ver detalhes:", height, width)
        self.menu_options = self.difficulty_options + [t.t('back')]

    def _render_difficulty_detail_view(self, stdscr, difficulty_name):
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Título em ASCII art
        ascii_title_lines = pyfiglet.figlet_format("Detalhes da Dificuldade", font="slant", width=min(200, width)).splitlines()
        title_height = len(ascii_title_lines)
        for i, line in enumerate(ascii_title_lines):
            x = max((width - len(line)) // 2, 0)
            if i < height:
                stdscr.addstr(i, x, line, curses.A_BOLD)
        
        # Dados da dificuldade
        difficulty_data = DIFFICULTY_MODIFIERS[difficulty_name]
        
        # Quebra a descrição em várias linhas
        desc_lines = []
        desc = difficulty_data['description']
        max_line_width = width - 4  # Margem de 2 caracteres em cada lado
        while len(desc) > max_line_width:
            # Encontra o último espaço dentro do limite
            break_index = desc.rfind(' ', 0, max_line_width)
            if break_index == -1:
                break_index = max_line_width
            desc_lines.append(desc[:break_index])
            desc = desc[break_index:].strip()
        desc_lines.append(desc)
        
        lines = [
            f"Dificuldade: {difficulty_name}",
            "Descrição:"
        ]
        lines.extend(desc_lines)
        lines.extend([
            "",
            "Modificadores:",
            f"  - Multiplicador de EXP: {difficulty_data['exp_multiplier']}x",
            f"  - Multiplicador de Ouro: {difficulty_data['gold_multiplier']}x",
            f"  - Dano Recebido: {difficulty_data['damage_received']}x",
            f"  - Dano Causado: {difficulty_data['damage_dealt']}x",
            f"  - Cura Recebida: {difficulty_data['healing_received']}x",
            f"  - Redução de Atributos: {difficulty_data['attribute_reduction']}",
            f"  - Multiplicador de HP dos Monstros: {difficulty_data['monster_hp_multiplier']}x"
        ])
        
        # Adiciona chance crítica de inimigos se existir
        if 'enemy_crit_chance_bonus' in difficulty_data:
            lines.append(f"  - Bônus de Chance Crítica dos Inimigos: +{difficulty_data['enemy_crit_chance_bonus']*100}%")
        
        # Renderiza as linhas com verificação de limites
        content_start_y = title_height + 2
        for i, line in enumerate(lines):
            y = content_start_y + i
            # Verifica se a linha está dentro dos limites da tela
            if y >= height - 2:
                break  # Para de renderizar se ultrapassar a tela
            x = max((width - len(line)) // 2, 0)
            stdscr.addstr(y, x, line)
        
        # Botão de voltar - verifica se há espaço suficiente
        back_text = t.t('back')
        back_y = content_start_y + len(lines) + 2
        if back_y < height - 1:  # Verifica se há espaço para o botão
            back_x = (width - len(back_text) - 4) // 2
            stdscr.addstr(back_y, back_x, f"> {back_text} <", curses.A_REVERSE)
        
        self.menu_options = [t.t('back')]

    def _render_race_details(self, stdscr, height, width):
        self._render_simple_prompt(stdscr, "Selecione uma Raça para ver detalhes:", height, width)
        self.menu_options = [f"{i+1}. {race.get('name', 'Raça Desconhecida')}" for i, race in enumerate(self.races)]
        self.menu_options.append(t.t('back'))

    def _render_class_details(self, stdscr, height, width):
        self._render_simple_prompt(stdscr, "Selecione uma Classe para ver detalhes:", height, width)
        self.menu_options = [f"{i+1}. {cls.get('name', 'Classe Desconhecida')}" for i, cls in enumerate(self.classes)]
        self.menu_options.append(t.t('back'))

    def _render_background_details(self, stdscr, height, width):
        self._render_simple_prompt(stdscr, "Selecione um Antecedente para ver detalhes:", height, width)
        self.menu_options = [f"{i+1}. {bg.get('name', 'Antecedente Desconhecido')}" for i, bg in enumerate(self.backgrounds)]
        self.menu_options.append(t.t('back'))

    def _resolve_item_name(self, item_id):
        if item_id is None:
            return "Nenhum"
        item = get_item_base_details(self.db_conn, item_id)
        return item.get("name", f"Item {item_id}") if item else f"Item {item_id}"

    def _render_detail_view(self, stdscr, data, title="Detalhes"):
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # --- Título em ASCII art ---
        ascii_title_lines = pyfiglet.figlet_format(title, font="slant", width=min(200, width)).splitlines()
        title_height = len(ascii_title_lines)
        for i, line in enumerate(ascii_title_lines):
            x = max((width - len(line)) // 2, 0)
            if i < height:
                stdscr.addstr(i, x, line, curses.A_BOLD)

        # --- Conteúdo detalhado centralizado ---
        lines = []
        for k, v in data.items():
            if v and k != "id":
                key_str = f"{k.capitalize()}: "

                # Se o campo for um ID de item, converte para nome
                if k in ("starting_weapon_id", "starting_armor_id"):
                    value_str = self._resolve_item_name(v)
                else:
                    value_str = str(v)

                # Quebra a linha se ultrapassar largura da tela
                while len(value_str) > width - len(key_str) - 4:
                    part = value_str[:width - len(key_str) - 4]
                    lines.append(key_str + part)
                    value_str = value_str[len(part):]
                    key_str = " " * len(key_str)
                lines.append(key_str + value_str)

        # Calcula posição inicial vertical para centralizar
        content_start_y = title_height + 2
        for i, line in enumerate(lines):
            y = content_start_y + i
            x = max((width - len(line)) // 2, 0)
            if y < height - 2:
                stdscr.addstr(y, x, line)

        # --- Botão de voltar mais abaixo ---
        back_text = t.t('back')
        back_y = content_start_y + len(lines) + 5  # deixa 2 linhas de espaço
        back_x = (width - len(back_text) - 4) // 2
        stdscr.addstr(back_y, back_x, f"> {back_text} <", curses.A_REVERSE)

        self.menu_options = [t.t('back')]

    def _render_name_creation(self, stdscr, height, width):
        self.menu_options = [t.t('start_name_creation'), t.t('back_to_main_menu')]

    def _handle_name_input(self):
        if self.current_selection == 0:
            # Inicia a criação de nome
            self.name_creator = CharacterNameCreator(self.game.stdscr)
            nome = self.name_creator.run()
            if nome:
                self.character_data["name"] = nome
                self.step = "difficulty"
            else:
                self.step = "name"
        elif self.current_selection == 1:
            from ..system.main_menu_state import MainMenuState
            self.game.change_state(MainMenuState(self.game))

    def _render_title(self, stdscr, title_text):
        """Renderiza o título em ASCII art centralizado"""
        height, width = stdscr.getmaxyx()
        ascii_lines = pyfiglet.figlet_format(title_text, font="slant", width=200).splitlines()
        
        for i, line in enumerate(ascii_lines):
            x = max((width - len(line)) // 2, 0)
            if i < height:  # Verifica se não ultrapassa a tela
                stdscr.addstr(i, x, line)
        
        return len(ascii_lines)  # Retorna a altura do título

    def render(self, stdscr):
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # --- Renderiza o título em ASCII para a etapa atual ---
        title_text = STEP_TITLES.get(self.step, "Rust Dice")
        title_height = self._render_title(stdscr, title_text)

        # --- Feedback de mensagem ---
        if self.feedback_message:
            message = self.feedback_message
            stdscr.addstr(title_height + 1, (width - len(message)) // 2, message)
            self.feedback_message = ""

        # --- Renderiza o menu baseado na etapa atual ---
        if self.step == "name":
            self._render_name_creation(stdscr, height, width)
        elif self.step == "difficulty":
            self._render_difficulty_options(stdscr, height, width)
        elif self.step == "difficulty_details":
            self._render_difficulty_details(stdscr, height, width)
        elif self.step == "difficulty_detail_view":
            self._render_difficulty_detail_view(stdscr, self.current_difficulty)
        elif self.step == "permadeath":
            self._render_permadeath_options(stdscr, height, width)
        elif self.step == "race":
            self._render_race_options_curses(stdscr, height, width)
        elif self.step == "class":
            self._render_class_options_curses(stdscr, height, width)
        elif self.step == "background":
            self._render_background_options_curses(stdscr, height, width)
        elif self.step == "attributes":
            self._render_attribute_options_curses(stdscr, height, width)
        elif self.step == "attribute_reroll":
            self._render_attribute_reroll_options_curses(stdscr, height, width)
        elif self.step == "complete":
            self._render_completion_message(stdscr, height, width)
        elif self.step == "overview":  # NOVO
            self._render_character_overview(stdscr, height, width)
            
        elif self.step == "race_details":
            self._render_race_details(stdscr, height, width)
        elif self.step == "class_details":
            self._render_class_details(stdscr, height, width)
        elif self.step == "background_details":
            self._render_background_details(stdscr, height, width)
        elif self.step == "detail_view":
            self._render_detail_view(stdscr, self.current_detail, "Detalhes")


        self._display_menu(stdscr, height, width, title_height)
        stdscr.refresh()


    def execute_choice(self):
        """Executa a escolha do menu com base na etapa e na seleção atual."""
        if self.step == "start":
            self._handle_start_input()
        elif self.step == "name":
            self._handle_name_input()
        elif self.step == "difficulty":
            self._handle_difficulty_input()
        elif self.step == "difficulty_details":
            if self.current_selection < len(self.difficulty_options):
                self.current_difficulty = self.difficulty_options[self.current_selection]
                self.step = "difficulty_detail_view"
            else:
                self.step = "difficulty"
        elif self.step == "difficulty_detail_view":
            self.step = "difficulty_details"
        elif self.step == "permadeath":
            self._handle_permadeath_input()

        elif self.step == "race":
            self._handle_race_input_curses()
        elif self.step == "class":
            self._handle_class_input_curses()
        elif self.step == "background":
            self._handle_background_input_curses()
        elif self.step == "attributes":
            self._handle_attributes_input_curses()
        elif self.step == "attribute_reroll":
            self._handle_attribute_reroll_input_curses()
        elif self.step == "complete":
            self._handle_complete_input()
        elif self.step == "overview":
            from ..world.gameplay_state import GameplayState
            self.game.change_state(GameplayState(self.game))
        
        elif self.step == "race_details":
            if self.current_selection < len(self.races):
                self.current_detail = self.races[self.current_selection]
                self.step = "detail_view"
            else:
                self.step = "race"

        elif self.step == "class_details":
            if self.current_selection < len(self.classes):
                self.current_detail = self.classes[self.current_selection]
                self.step = "detail_view"
            else:
                self.step = "class"

        elif self.step == "background_details":
            if self.current_selection < len(self.backgrounds):
                self.current_detail = self.backgrounds[self.current_selection]
                self.step = "detail_view"
            else:
                self.step = "background"

        elif self.step == "detail_view":
            self.step = (
                "race_details" if "strength_bonus" in self.current_detail
                else "class_details" if "hit_dice" in self.current_detail
                else "background_details"
            )
        
        # Resetar seleção sempre no fim
        self.current_selection = 0

        
    def _display_menu(self, stdscr, height, width, title_height):
        """Método auxiliar para renderizar as opções do menu no Curses."""
        if self.step == "detail_view":
            return  # já desenhamos o menu de back no _render_detail_view

        # Posiciona o menu um pouco abaixo do título ASCII
        extra_spacing = 2
        menu_start_y = title_height + extra_spacing

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

    # --- Métodos de Renderização ---
    def _render_start_options(self, stdscr, height, width):
        self.menu_options = [t.t('start_creation'), t.t('back_to_main_menu')]
    
    def _render_difficulty_options(self, stdscr, height, width):
        self.menu_options = self.difficulty_options + [t.t('difficulty_details'), t.t('back_to_main_menu')]

    def _render_permadeath_options(self, stdscr, height, width):
        self.menu_options = self.permadeath_options + [t.t('back_to_difficulty')]

    def _render_race_options_curses(self, stdscr, height, width):
        self.menu_options = [f"{i+1}. {race.get('name', 'Raça Desconhecida')}" for i, race in enumerate(self.races)]
        self.menu_options.append(t.t('race_details'))
        self.menu_options.append(t.t('back_to_permadeath'))

    def _render_class_options_curses(self, stdscr, height, width):
        self.menu_options = [f"{i+1}. {cls.get('name', 'Classe Desconhecida')}" for i, cls in enumerate(self.classes)]
        self.menu_options.append(t.t('class_details'))
        self.menu_options.append(t.t('back_to_race'))

    def _render_background_options_curses(self, stdscr, height, width):
        self.menu_options = [f"{i+1}. {bg.get('name', 'Antecedente Desconhecido')}" for i, bg in enumerate(self.backgrounds)]
        self.menu_options.append(t.t('background_details'))
        self.menu_options.append(t.t('back_to_class'))

    def _render_attribute_options_curses(self, stdscr, height, width):
        self.menu_options = [
            t.t('attributes_keep_and_finalize'),
            t.t('attributes_reroll_all'),
            t.t('attributes_reroll_one'),
            t.t('back_to_background')
        ]
        if self.temp_character:
            stdscr.addstr(5, 2, self.temp_character.show_attributes_string())
    
    def _render_attribute_reroll_options_curses(self, stdscr, height, width):
        self.menu_options = [
            f"{t.t('strength')}", f"{t.t('dexterity')}",
            f"{t.t('constitution')}", f"{t.t('intelligence')}",
            f"{t.t('wisdom')}", f"{t.t('charisma')}",
            t.t('back')
        ]

    def _render_completion_message(self, stdscr, height, width):
        # Lógica de renderização da mensagem de conclusão
        self.menu_options = [t.t('press_enter_to_continue')]
        stdscr.addstr(5, (width - len(t.t('creation_complete'))) // 2, t.t('creation_complete'))
        stdscr.addstr(6, (width - len(t.t('new_character_created', name=self.temp_character.name))) // 2, t.t('new_character_created', name=self.temp_character.name))


    # --- Métodos de Manipulação de Escolha ---
    def _handle_start_input(self):
        if self.current_selection == 0:
            self.step = "difficulty"
        elif self.current_selection == 1:
            from ..system.main_menu_state import MainMenuState
            self.game.change_state(MainMenuState(self.game))
    
    def _handle_difficulty_input(self):
        if self.current_selection < len(self.difficulty_options):
            self.difficulty = self.difficulty_options[self.current_selection]
            self.character_data["difficulty"] = self.difficulty
            self.feedback_message = f"Dificuldade definida como: {self.difficulty}"
            self.step = "permadeath"
        elif self.current_selection == len(self.difficulty_options):  # Opção de detalhes
            self.step = "difficulty_details"
        else:  # Voltar
            self.step = "name"

    def _handle_permadeath_input(self):
        if self.current_selection == 0:
            self.character_data["permadeath"] = 1
            self.feedback_message = "Morte Permanente ATIVADA!"
            self.step = "race"
        elif self.current_selection == 1:
            self.character_data["permadeath"] = 0
            self.feedback_message = "Morte Permanente DESATIVADA!"
            self.step = "race"
        else:  # Voltar (terceira opção)
            self.step = "difficulty"
    
    def _handle_race_input_curses(self):
        if self.current_selection < len(self.races):
            race = self.races[self.current_selection]
            self.character_data["race"] = race.get('name', 'Humano')
            self.feedback_message = f"Raça escolhida: {self.character_data['race']}"
            self.step = "class"
        elif self.current_selection == len(self.races):
            self.step = "race_details"   # <-- agora entra nos detalhes
        elif self.current_selection == len(self.races) + 1:
            self.step = "permadeath"

    def _handle_class_input_curses(self):
        if self.current_selection < len(self.classes):
            cls = self.classes[self.current_selection]
            self.character_data["char_class"] = cls.get('name', 'Guerreiro')
            self.feedback_message = f"Classe escolhida: {self.character_data['char_class']}"
            self.step = "background"
        elif self.current_selection == len(self.classes):
            self.step = "class_details"  # <-- entra nos detalhes
        elif self.current_selection == len(self.classes) + 1:
            self.step = "race"

    def _handle_background_input_curses(self):
        if self.current_selection < len(self.backgrounds):
            background = self.backgrounds[self.current_selection]
            self.character_data["background"] = background.get('name', 'Nenhum')
            self.feedback_message = f"Antecedente escolhido: {self.character_data['background']}"
            self._create_temp_character()
            self.step = "attributes"
        elif self.current_selection == len(self.backgrounds):
            self.step = "background_details"  # <-- entra nos detalhes
        elif self.current_selection == len(self.backgrounds) + 1:
            self.step = "class"


    def _handle_attributes_input_curses(self):
        if self.current_selection == 0:
            self._finalize_character()
        elif self.current_selection == 1:
            self._reroll_all_attributes()
        elif self.current_selection == 2:
            self.step = "attribute_reroll"
        elif self.current_selection == 3:
            self.step = "background"

    def _handle_attribute_reroll_input_curses(self):
        if self.current_selection == 6:
            self.step = "attributes"
        elif 0 <= self.current_selection < 6:
            attribute_name = list(attr_map.values())[self.current_selection + 1] # +1 para pular a opção de back
            old_value = getattr(self.temp_character, attribute_name)
            new_value = roll_attribute()
            setattr(self.temp_character, attribute_name, new_value)
            self.temp_character.recalculate()
            self.feedback_message = f"Atributo '{attribute_name.capitalize()}' rerolado de {old_value} para {new_value}."
            self.step = "attributes"

    def _create_temp_character(self):
        """Cria o objeto Character temporário."""
        self.temp_character = Character(
            db_connection=self.game.db_conn,
            name=self.character_data.get("name", "Sem Nome"),
            race=self.character_data["race"],
            char_class=self.character_data["char_class"],
            background=self.character_data["background"],
            difficulty=self.difficulty,
            permadeath=1 if self.permadeath == self.permadeath_options[0] else 0,
        )
        self.temp_character.recalculate()

    def _finalize_character(self):
        """Salva o personagem, aplica perícias e itens iniciais."""
        try:
            if not save_character(self.db_conn, self.temp_character):
                self.feedback_message = "Falha ao salvar o personagem inicial."
                return

            loaded_char = Character.load_character(self.db_conn, self.temp_character.id)
            if not loaded_char:
                self.feedback_message = "Falha ao carregar personagem salvo."
                return

            self.temp_character = loaded_char
            self.temp_character.apply_background_skills()
            self.temp_character.equip_starting_items()
            self.game.player = self.temp_character
            self.step = "complete"
        except Exception as e:
            self.feedback_message = f"Erro ao finalizar personagem: {str(e)}"
            traceback.print_exc()

    def _reroll_all_attributes(self):
        """Rerola todos os atributos do personagem temporário."""
        self.temp_character.strength = roll_attribute()
        self.temp_character.dexterity = roll_attribute()
        self.temp_character.constitution = roll_attribute()
        self.temp_character.intelligence = roll_attribute()
        self.temp_character.wisdom = roll_attribute()
        self.temp_character.charisma = roll_attribute()
        self.temp_character.recalculate()
        self.feedback_message = "Atributos rerolados!"

    def _handle_complete_input(self):
        self.step = "overview"

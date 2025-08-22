# game/states/attributes_state.py
from ..base_state import BaseState
from game.utils import modifier, get_display_name
import curses
from prettytable import PrettyTable
import pyfiglet
import textwrap

class AttributesState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.tabs = ['Resumo', 'Atributos', 'Equipamentos', 'Perícias', 'Dificuldade']
        self.current_tab = 0
        self.tab_changed = True
        self.scrollable = True
        self.title_art = None
        self.content_height = 0
        
        # Inicializar o título com pyfiglet
        try:
            self.title_art = pyfiglet.Figlet(font='big', width=80).renderText("ATRIBUTOS")
        except:
            # Fallback se pyfiglet não estiver disponível
            self.title_art = "📊 ATRIBUTOS 📊"

    def enter(self):
        self.tab_changed = True
        self.scroll_offset = 0
        self.current_selection = 0

    def render(self, stdscr):
        # Sempre renderizar, não apenas quando tab_changed for True
        stdscr.clear()
        
        # Obter dimensões da tela
        height, width = stdscr.getmaxyx()
        
        # Renderizar título especial com pyfiglet
        title_lines = self.title_art.split('\n')
        for i, line in enumerate(title_lines):
            if i < height - 1:
                stdscr.addstr(i, (width - len(line)) // 2, line[:width-1], curses.A_BOLD)
        
        # Navegação por abas
        y_pos = len(title_lines) + 1
        tab_bar = " | ".join(
            [f"{'▶ ' + tab + ' ◀' if i == self.current_tab else tab}" 
             for i, tab in enumerate(self.tabs)]
        )
        
        stdscr.addstr(y_pos, (width - len(tab_bar)) // 2, tab_bar[:width-1])
        y_pos += 2
        
        # Área de conteúdo principal (aplicar scroll aqui)
        content_start_y = y_pos
        content_height = height - content_start_y - 1  # Reservar espaço para instruções
        
        # Renderização da aba atual com suporte a scroll
        if self.current_tab == 0:
            self._render_summary_tab(stdscr, content_start_y, width, height)
        elif self.current_tab == 1:
            self._render_attributes_tab(stdscr, content_start_y, width, height)
        elif self.current_tab == 2:
            self._render_equipment_tab(stdscr, content_start_y, width, height)
        elif self.current_tab == 3:
            self._render_skills_tab(stdscr, content_start_y, width, height)
        elif self.current_tab == 4:
            self._render_difficulty_tab(stdscr, content_start_y, width, height)
        
        # Instruções de navegação
        instructions = "Navegação: [←→] Mudar Aba | [↑↓] Scroll | [Enter] Voltar"
        if height > 1:
            stdscr.addstr(height-1, (width - len(instructions)) // 2, instructions[:width-1])
        
        # Indicador de scroll se necessário
        if self.max_scroll > 0:
            scroll_indicator = f"↑↓ {self.scroll_offset+1}/{self.max_scroll+1}"
            stdscr.addstr(height-1, 2, scroll_indicator[:width-5])
        
        stdscr.refresh()
        self.tab_changed = False

    def handle_input(self):
        """Método para lidar com a entrada do usuário para navegação de menu."""
        key = self.stdscr.getch()
        
        # Primeiro verifica se é um evento de rolagem
        if self.scrollable and self.handle_scroll_input(key):
            self.game.needs_render = True
            return
            
        # Navegação entre abas
        if key in (curses.KEY_RIGHT, ord('d'), ord('D')):
            self.current_tab = (self.current_tab + 1) % len(self.tabs)
            self.tab_changed = True
            self.scroll_offset = 0
            self.game.needs_render = True
        elif key in (curses.KEY_LEFT, ord('a'), ord('A')):
            self.current_tab = (self.current_tab - 1) % len(self.tabs)
            self.tab_changed = True
            self.scroll_offset = 0
            self.game.needs_render = True
        elif key in (curses.KEY_ENTER, 10, 13):  # Tecla Enter
            self.game.pop_state()
            self.game.needs_render = True
        elif key == 27:  # Tecla Escape
            self.game.pop_state()
            self.game.needs_render = True

    # =======================================================================
    # Métodos de renderização de abas (atualizados para suportar scroll)
    # =======================================================================
    
    def _render_summary_tab(self, stdscr, start_y, width, screen_height):
        player = self.game.player
        y_pos = start_y
        content_lines = []
        
        # Criar tabela para informações básicas
        info_table = PrettyTable()
        info_table.field_names = ["Informação", "Valor"]
        info_table.align = "l"
        info_table.header = False
        info_table.border = False
        info_table.hrules = False
        
        info_table.add_row(["Raça", player.race])
        info_table.add_row(["Classe", player.char_class])
        info_table.add_row(["Nível", f"{player.level}"])
        info_table.add_row(["Experiência", f"{player.exp}/{player.exp_max}"])
        info_table.add_row(["Dificuldade", player.difficulty])
        info_table.add_row(["Ouro", f"{player.gold}"])
        
        table_str = info_table.get_string()
        content_lines.extend(table_str.split('\n'))
        content_lines.append("")  # Linha vazia
        
        # Barras de recursos
        content_lines.extend(self._get_resource_bar_lines("HP", player.hp, player.hp_max, "❤️"))
        if player.mana_max > 0:
            content_lines.extend(self._get_resource_bar_lines("Mana", player.mana, player.mana_max, "🔵"))
        content_lines.append("")
        
        # Resumo de combate
        content_lines.append("⚔️ RESUMO DE COMBATE")
        content_lines.append("")
        
        combat_table = PrettyTable()
        combat_table.field_names = ["Atributo", "Valor"]
        combat_table.align = "l"
        combat_table.header = False
        combat_table.border = False
        
        weapon = next((item for item in player.get_equipped_items() if item['category'] == 'weapon'), None)
        weapon_name = get_display_name(weapon) if weapon else "Nenhuma"
        weapon_damage = f"{player.weapon_dice} {player.damage_type}" if weapon else "1d4 impacto"
        
        combat_table.add_row(["Arma", weapon_name])
        combat_table.add_row(["Dano", weapon_damage])
        combat_table.add_row(["CA", f"{player.ac}"])
        combat_table.add_row(["Res. Física", f"{player.get_physical_resistance()}"])
        combat_table.add_row(["Res. Mágica", f"{player.get_magical_resistance()}"])
        
        combat_str = combat_table.get_string()
        content_lines.extend(combat_str.split('\n'))
        content_lines.append("")
        
        # Resumo de atributos
        content_lines.append("📈 ATRIBUTOS")
        content_lines.append("")
        
        attributes = [
            ("💪 Força", player.get_effective_strength(), modifier(player.get_effective_strength())),
            ("🏹 Destreza", player.get_effective_dexterity(), modifier(player.get_effective_dexterity())),
            ("❤️ Constituição", player.get_effective_constitution(), modifier(player.get_effective_constitution())),
            ("📚 Inteligência", player.get_effective_intelligence(), modifier(player.get_effective_intelligence())),
            ("🔮 Sabedoria", player.get_effective_wisdom(), modifier(player.get_effective_wisdom())),
            ("✨ Carisma", player.get_effective_charisma(), modifier(player.get_effective_charisma()))
        ]
        
        attr_table = PrettyTable()
        attr_table.field_names = ["Atributo", "Valor", "Mod"]
        attr_table.align = "l"
        attr_table.header = False
        attr_table.border = False
        
        for i in range(0, len(attributes), 2):
            attr1 = attributes[i]
            if i+1 < len(attributes):
                attr2 = attributes[i+1]
                attr_table.add_row([attr1[0], f"{attr1[1]} ({attr1[2]:+})", f"{attr2[0]}: {attr2[1]} ({attr2[2]:+})"])
            else:
                attr_table.add_row([attr1[0], f"{attr1[1]} ({attr1[2]:+})", ""])
        
        attr_str = attr_table.get_string()
        content_lines.extend(attr_str.split('\n'))
        
        # Renderizar linhas visíveis considerando o scroll
        self._render_content_with_scroll(stdscr, start_y, width, screen_height, content_lines)

    def _render_attributes_tab(self, stdscr, start_y, width, screen_height):
        player = self.game.player
        content_lines = []
        
        attributes = [
            ("💪 Força", 
             player.strength, 
             player.get_effective_strength(),
             modifier(player.get_effective_strength()), 
             ["Ataque corpo a corpo", "Testes de força"]),
            
            ("🏹 Destreza", 
             player.dexterity, 
             player.get_effective_dexterity(),
             modifier(player.get_effective_dexterity()), 
             ["CA", "Ataque à distância", "Iniciativa"]),
            
            ("❤️ Constituição", 
             player.constitution, 
             player.get_effective_constitution(),
             modifier(player.get_effective_constitution()), 
             ["Pontos de vida", "Resistência"]),
            
            ("📚 Inteligência", 
             player.intelligence, 
             player.get_effective_intelligence(),
             modifier(player.get_effective_intelligence()), 
             ["Conhecimento", "Magias arcanas"]),
            
            ("🔮 Sabedoria", 
             player.wisdom, 
             player.get_effective_wisdom(),
             modifier(player.get_effective_wisdom()), 
             ["Percepção", "Magias divinas"]),
            
            ("✨ Carisma", 
             player.charisma, 
             player.get_effective_charisma(),
             modifier(player.get_effective_charisma()), 
             ["Persuasão", "Intimidação"])
        ]
        
        for name, base_value, effective_value, mod, uses in attributes:
            reduction = base_value - effective_value
            reduction_text = f" (🔻 Redução: -{reduction})" if reduction > 0 else ""
            
            content_lines.append(f"{name}:")
            content_lines.append(f"  Base: {base_value}{reduction_text} | Efetivo: {effective_value} | Mod: {mod:+}")
            content_lines.append(f"  🔹 Usos: {', '.join(uses)}")
            
            # Barra visual do atributo
            bar_length = min(20, max(0, (effective_value - 8) // 2))
            filled = "█" * bar_length
            empty = "░" * (20 - bar_length)
            
            rating = {
                20: "Lendário", 18: "Heróico", 16: "Excepcional",
                14: "Muito Bom", 12: "Bom", 10: "Médio",
                8: "Abaixo da Média", 0: "Fraco"
            }
            rating_desc = next((v for k, v in rating.items() if effective_value >= k), "Fraco")
            
            content_lines.append(f"[{filled}{empty}] {rating_desc}")
            content_lines.append("")
        
        # Renderizar linhas visíveis considerando o scroll
        self._render_content_with_scroll(stdscr, start_y, width, screen_height, content_lines)

    def _render_equipment_tab(self, stdscr, start_y, width, screen_height):
        player = self.game.player
        equipped_items = player.get_equipped_items()
        content_lines = []
        
        # Arma
        weapon = next((item for item in equipped_items if item['category'] == 'weapon'), None)
        if weapon:
            weapon_name = get_display_name(weapon)
            damage_info = f"{weapon.get('damage_dice', '1d4')} {weapon.get('damage_type', 'impacto')}"
            enhancement = weapon.get('enhancement_level', 0)
            enhancement_str = f" (Aprimoramento +{enhancement})" if enhancement > 0 else ""
            
            content_lines.append("⚔️ ARMA PRINCIPAL:")
            content_lines.append(f"  {weapon_name}{enhancement_str}")
            content_lines.append(f"  Dano: {damage_info}")
            content_lines.append(f"  Atributo: {weapon.get('main_attribute', 'força').capitalize()}")
            content_lines.append("")
        else:
            content_lines.append("⚔️ ARMA PRINCIPAL: Nenhuma equipada")
            content_lines.append("")
        
        # Armadura
        armor = next((item for item in equipped_items if item['category'] == 'armor'), None)
        if armor:
            armor_name = get_display_name(armor)
            enhancement = armor.get('enhancement_level', 0)
            enhancement_str = f" (Aprimoramento +{enhancement})" if enhancement > 0 else ""
            
            content_lines.append("🛡️ ARMADURA:")
            content_lines.append(f"  {armor_name}{enhancement_str}")
            content_lines.append(f"  Tipo: {armor.get('armor_class', 'leve').capitalize()}")
            content_lines.append(f"  Bônus de CA: +{armor.get('armor_bonus', 0)}")
            content_lines.append(f"  Res. Física: +{armor.get('physical_resistance', 0)}")
            content_lines.append(f"  Res. Mágica: +{armor.get('magical_resistance', 0)}")
            content_lines.append("")
        else:
            content_lines.append("🛡️ ARMADURA: Nenhuma equipada")
            content_lines.append("")
        
        # Escudo
        shield = next((item for item in equipped_items if item['category'] == 'shield'), None)
        if shield:
            shield_name = get_display_name(shield)
            enhancement = shield.get('enhancement_level', 0)
            enhancement_str = f" (Aprimoramento +{enhancement})" if enhancement > 0 else ""
            
            content_lines.append("🔰 ESCUDO:")
            content_lines.append(f"  {shield_name}{enhancement_str}")
            content_lines.append(f"  Bônus de CA: +{shield.get('armor_bonus', 0)}")
            content_lines.append(f"  Penalidade Destreza: {shield.get('dexterity_penalty', 0)}")
            content_lines.append("")
        
        # Acessórios
        accessories = [item for item in equipped_items 
                      if item['category'] in ['ring', 'amulet', 'belt', 'boots']]
        
        if accessories:
            content_lines.append("💍 ACESSÓRIOS:")
            
            for item in accessories:
                item_name = get_display_name(item)
                slot = item.get('equipped_slot_friendly', 'Equipado')
                effects = []
                
                if 'armor_bonus' in item and item['armor_bonus'] != 0:
                    effects.append(f"CA +{item['armor_bonus']}")
                if 'physical_resistance' in item and item['physical_resistance'] != 0:
                    effects.append(f"Res.Fis +{item['physical_resistance']}")
                if 'magical_resistance' in item and item['magical_resistance'] != 0:
                    effects.append(f"Res.Mag +{item['magical_resistance']}")
                
                effects_str = " | ".join(effects) if effects else "Sem efeitos especiais"
                
                content_lines.append(f"  {item_name} ({slot}) {effects_str}")
            content_lines.append("")
        else:
            content_lines.append("💍 ACESSÓRIOS: Nenhum equipado")
            content_lines.append("")
        
        # Renderizar linhas visíveis considerando o scroll
        self._render_content_with_scroll(stdscr, start_y, width, screen_height, content_lines)

    def _render_skills_tab(self, stdscr, start_y, width, screen_height):
        player = self.game.player
        content_lines = []
        
        try:
            skills = player.get_all_skills()
            if not skills:
                content_lines.append("❌ Nenhuma perícia disponível")
                # Renderizar linhas visíveis considerando o scroll
                self._render_content_with_scroll(stdscr, start_y, width, screen_height, content_lines)
                return
                
            # Agrupar por atributo
            skills_by_attribute = {}
            for skill in skills:
                attribute = skill.get('attribute', 'none').lower()
                if attribute not in skills_by_attribute:
                    skills_by_attribute[attribute] = []
                skills_by_attribute[attribute].append(skill)
            
            # Ordem de exibício
            attribute_order = ['for', 'des', 'con', 'int', 'sab', 'car', 'none']
            attribute_names = {
                'for': '💪 Força',
                'des': '🏹 Destreza',
                'con': '❤️ Constituição',
                'int': '📚 Inteligência',
                'sab': '🔮 Sabedoria',
                'car': '✨ Carisma',
                'none': '🛠️ Gerais'
            }
            
            for attr in attribute_order:
                if attr in skills_by_attribute and skills_by_attribute[attr]:
                    content_lines.append(f"{attribute_names.get(attr, '🛠️ Gerais')}:")
                    
                    for skill in skills_by_attribute[attr]:
                        skill_name = skill.get('skill_name', 'Desconhecida')
                        level = skill.get('level', 0)
                        current_xp = skill.get('current_xp', 0)
                        max_xp = skill.get('max_xp', 50)
                        
                        percent = min(100, int((current_xp / max_xp) * 100)) if max_xp > 0 else 0
                        bar_length = min(20, percent // 5)
                        bar = f"[{'█' * bar_length}{'░' * (20 - bar_length)}]"
                        
                        content_lines.append(f"  {skill_name} (Nv {level}):")
                        content_lines.append(f"    XP: {current_xp}/{max_xp} {bar} {percent}%")
                        content_lines.append("")
        
        except Exception as e:
            content_lines.append(f"❌ Erro ao carregar perícias: {str(e)}")
        
        # Renderizar linhas visíveis considerando o scroll
        self._render_content_with_scroll(stdscr, start_y, width, screen_height, content_lines)

    def _render_difficulty_tab(self, stdscr, start_y, width, screen_height):
        player = self.game.player
        difficulty_modifiers = player.get_difficulty_modifiers()
        content_lines = []
        
        # Título
        content_lines.append("CONFIGURAÇÃO ATUAL DE DIFICULDADE")
        content_lines.append("")
        
        # Tabela de modificadores
        table = PrettyTable()
        table.field_names = ["Modificador", "Efeito"]
        table.align = "l"
        table.header = True
        table.border = True
        
        for key, value in difficulty_modifiers.items():
            name = {
                'exp_multiplier': 'Multiplicador de EXP',
                'gold_multiplier': 'Multiplicador de Ouro',
                'damage_received': 'Dano Recebido',
                'damage_dealt': 'Dano Causado',
                'healing_received': 'Cura Recebida',
                'attribute_reduction': 'Redução de Atributos',
                'permadeath': 'Morte Permanente'
            }.get(key, key)
            
            # Formatação dos valores
            if key in ['exp_multiplier', 'gold_multiplier', 'damage_received', 
                      'damage_dealt', 'healing_received']:
                effect = f"{int((value-1)*100)}%"
                effect = f"+{effect}" if value > 1 else effect
            elif key == 'attribute_reduction':
                effect = f"-{value}"
            elif key == 'permadeath':
                effect = "✅ Ativo" if value else "❌ Inativo"
            else:
                effect = str(value)
            
            table.add_row([name, effect])
        
        table_str = table.get_string()
        content_lines.extend(table_str.split('\n'))
        
        # Renderizar linhas visíveis considerando o scroll
        self._render_content_with_scroll(stdscr, start_y, width, screen_height, content_lines)

    # =======================================================================
    # Métodos auxiliares
    # =======================================================================
    
    def _get_resource_bar_lines(self, name, current, max_value, icon):
        """Retorna as linhas de uma barra de recurso (HP ou Mana)"""
        if max_value <= 0:
            return []
            
        percent = min(100, int((current / max_value) * 100))
        filled = percent // 5
        empty = 20 - filled
        
        bar = f"[{'█' * filled}{'░' * empty}] {percent}%"
        
        return [f"{icon} {name}: {current}/{max_value}", bar, ""]
    
    def _render_content_with_scroll(self, stdscr, start_y, width, screen_height, content_lines):
        """Renderiza o conteúdo com suporte a scroll"""
        # Calcular a rolagem máxima
        self.calculate_max_scroll(len(content_lines), screen_height, header_lines=start_y, footer_lines=1)
        
        # Renderizar apenas as linhas visíveis
        visible_height = screen_height - start_y - 1  # Reservar espaço para instruções
        
        for i, line in enumerate(content_lines):
            screen_y = start_y + i - self.scroll_offset
            
            # Só renderizar se estiver na área visível
            if 0 <= screen_y < screen_height - 1:
                # Truncar a linha se for muito longa
                truncated_line = line[:width-3] + "..." if len(line) > width else line
                stdscr.addstr(screen_y, 2, truncated_line)

# Adicione esta linha ao final do arquivo para garantir que a classe seja exportada
__all__ = ['AttributesState']
# game/states/inventory_state.py
from ..base_state import BaseState
from game.utils import get_display_name, calculate_enhanced_damage, calculate_enhanced_value
import curses
import pyfiglet

class InventoryState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self._player = game.player
        self.current_menu = "main"
        self.feedback_message = ""
        self.selected_item = None
        self.previous_menu = None
        self.scrollable = True # Habilita a rolagem via BaseState
        self.title_art = None
        self.item_icons = {
            'weapon': '⚔️',
            'armor': '🛡️',
            'shield': '🔰',
            'consumable': '🧪',
            'ammo': '🏹',
            'misc': '📦',
            'other': '❓'
        }
        
        # Inicializar o título com pyfiglet
        try:
            self.title_art = pyfiglet.Figlet(font='big', width=80).renderText("INVENTARIO")
        except:
            # Fallback se pyfiglet não estiver disponível
            self.title_art = "🎒 INVENTÁRIO 🎒"

    def enter(self):
        """Método chamado ao entrar neste estado."""
        self.feedback_message = ""
        self.scroll_offset = 0
        self.current_selection = 0
        self.game.needs_render = True

    def render(self, stdscr):
        stdscr.clear()
        
        height, width = stdscr.getmaxyx()
        
        # Renderizar título
        title_lines = self.title_art.split('\n')
        for i, line in enumerate(title_lines):
            if i < height - 1:
                # Garante que a linha não exceda a largura da tela
                safe_line = line[:width-1]
                stdscr.addstr(i, (width - len(safe_line)) // 2, safe_line, curses.A_BOLD)
        
        y_pos = len(title_lines) + 1
        
        # Exibir mensagem de feedback
        if self.feedback_message and y_pos < height - 1:
            centered_msg = f">>> {self.feedback_message} <<<".center(width)
            stdscr.addstr(y_pos, 0, centered_msg[:width-1], curses.A_REVERSE)
            y_pos += 2
        
        # Renderizar menu atual
        if self.current_menu == "main":
            self._render_main_menu(stdscr, y_pos, width, height)
        elif self.current_menu == "equip":
            self._render_equip_menu(stdscr, y_pos, width, height)
        elif self.current_menu == "unequip":
            self._render_unequip_menu(stdscr, y_pos, width, height)
        elif self.current_menu == "item_list":
            self._render_item_list_menu(stdscr, y_pos, width, height)
        elif self.current_menu == "item_detail":
            self._render_item_detail(stdscr, y_pos, width, height)
        
        # Instruções de navegação
        instructions = self._get_instructions()
        if height > 1:
            centered_instructions = instructions.center(width)
            # Correção para evitar erro de escrita na última célula
            stdscr.addstr(height - 1, 0, centered_instructions[:width - 1])
        
        # Indicador de scroll
        if self.max_scroll > 0:
            scroll_indicator = f"Scroll: {self.scroll_offset+1}/{self.max_scroll+1}"
            stdscr.addstr(height - 1, width - len(scroll_indicator) - 2, scroll_indicator)
        
        stdscr.refresh()

    def handle_input(self):
        """Lida com a entrada do usuário, unificando a navegação."""
        key = self.stdscr.getch()
        
        # A rolagem de tela é tratada primeiro (herdado de BaseState)
        if self.scrollable and self.handle_scroll_input(key):
            self.game.needs_render = True
            return
            
        # Navegação unificada para cima/baixo
        if key in (curses.KEY_UP, ord('w'), ord('W')):
            max_options = self._get_current_menu_options_count()
            if max_options > 0:
                self.current_selection = (self.current_selection - 1) % max_options
        elif key in (curses.KEY_DOWN, ord('s'), ord('S')):
            max_options = self._get_current_menu_options_count()
            if max_options > 0:
                self.current_selection = (self.current_selection + 1) % max_options
        
        # Ações
        elif key in (curses.KEY_ENTER, 10, 13):
            self._handle_enter_key()
        elif key == 27:  # Escape
            self._handle_escape_key()
        
        # Atalhos numéricos para o menu principal
        elif ord('1') <= key <= ord('4') and self.current_menu == "main":
            self._handle_number_key(chr(key))
        
        self.game.needs_render = True

    def _handle_enter_key(self):
        """Lida com a tecla Enter baseado no menu atual."""
        self.feedback_message = "" # Limpa a mensagem anterior ao executar uma ação
        
        if self.current_menu == "main":
            menu_actions = ["equip", "unequip", "item_list"]
            if 0 <= self.current_selection < 3:
                self.current_menu = menu_actions[self.current_selection]
                self.current_selection = 0
            elif self.current_selection == 3:
                self.game.pop_state()

        elif self.current_menu == "equip":
            equipable_items = self._get_equipable_items()
            if 0 <= self.current_selection < len(equipable_items):
                self._equip_selected_item(equipable_items[self.current_selection])
            elif self.current_selection == len(equipable_items):  # Voltar
                self.current_menu = "main"
                self.current_selection = 0

        elif self.current_menu == "unequip":
            equipped_items = self._player.get_equipped_items()
            if 0 <= self.current_selection < len(equipped_items):
                self._unequip_selected_item(equipped_items[self.current_selection])
            elif self.current_selection == len(equipped_items):  # Voltar
                self.current_menu = "main"
                self.current_selection = 1

        elif self.current_menu == "item_list":
            inventory = self._player.get_inventory()
            if 0 <= self.current_selection < len(inventory):
                self.selected_item = inventory[self.current_selection]
                self.previous_menu = "item_list"
                self.current_menu = "item_detail"
                self.current_selection = 0
            elif self.current_selection == len(inventory):  # Voltar
                self.current_menu = "main"
                self.current_selection = 2

        elif self.current_menu == "item_detail":
            is_equipped = any(eq['inventory_id'] == self.selected_item['inventory_id'] for eq in self._player.get_equipped_items())
            is_equipable = self.selected_item.get('equip_slot') and not is_equipped

            if self.current_selection == 0 and is_equipable:
                self._equip_selected_item(self.selected_item)
            else: # Opção Voltar
                self.current_menu = self.previous_menu or "main"
                self.current_selection = 0

    def _handle_escape_key(self):
        """Lida com a tecla Escape."""
        self.feedback_message = "" # Limpa a mensagem anterior
        if self.current_menu == "main":
            self.game.pop_state()
        else:
            self.current_menu = "main"
            self.current_selection = 0

    def _handle_number_key(self, key):
        """Lida com teclas numéricas no menu principal."""
        if self.current_menu == "main":
            option = int(key) - 1
            if 0 <= option <= 3:
                self.current_selection = option
                self._handle_enter_key()

    def _get_current_menu_options_count(self):
        """Retorna o número de opções selecionáveis para o menu atual."""
        if self.current_menu == "main":
            return 4
        elif self.current_menu == "equip":
            return len(self._get_equipable_items()) + 1  # Itens + Voltar
        elif self.current_menu == "unequip":
            return len(self._player.get_equipped_items()) + 1  # Itens + Voltar
        elif self.current_menu == "item_list":
            return len(self._player.get_inventory()) + 1  # Itens + Voltar
        elif self.current_menu == "item_detail":
            if not self.selected_item: return 1
            is_equipped = any(eq['inventory_id'] == self.selected_item['inventory_id'] for eq in self._player.get_equipped_items())
            is_equipable = self.selected_item.get('equip_slot') and not is_equipped
            return 2 if is_equipable else 1 # Equipar + Voltar ou só Voltar
        return 0

    def _get_instructions(self):
        """Retorna as instruções de navegação baseado no menu atual."""
        # A navegação agora é a mesma para todos os menus
        return "Navegação: [↑↓] Selecionar | [Enter] Confirmar | [ESC] Voltar"

    def _render_main_menu(self, stdscr, start_y, width, height):
        """Renderiza o menu principal do inventário."""
        content_lines = []
        
        # --- Seção de Equipamento Atual ---
        content_lines.append("⚔️ EQUIPAMENTO ATUAL")
        content_lines.append("-" * (width // 2))
        equipped_items = self._player.get_equipped_items()
        if not equipped_items:
            content_lines.append("Nenhum item equipado.")
        else:
            equipped_slots = {item['equipped_slot_technical']: item for item in equipped_items}
            display_order = [
                ('main_hand_inventory_id', "⚔️ Arma"), ('off_hand_inventory_id', "🛡️ Mão Secundária"),
                ('head_inventory_id', "🎩 Cabeça"), ('body_inventory_id', "👕 Corpo"),
                ('hands_inventory_id', "🧤 Mãos"), ('feet_inventory_id', "👟 Pés"),
                ('ring1_inventory_id', "💍 Anel 1"), ('ring2_inventory_id', "💍 Anel 2"),
                ('amulet_inventory_id', "💎 Amuleto")
            ]
            for slot_tech, label in display_order:
                item = equipped_slots.get(slot_tech)
                if item:
                    content_lines.append(f"{label}: {get_display_name(item)}")
                else:
                    content_lines.append(f"{label}: Vazio")
        content_lines.append("")

        # --- Seção de Opções ---
        content_lines.append("OPÇÕES")
        content_lines.append("-" * (width // 2))
        options = [
            "🧥 Equipar item",
            "🧺 Desequipar item",
            "🔍 Ver detalhes de item",
            "↩️ Voltar ao jogo"
        ]
        for i, option in enumerate(options):
            prefix = "> " if i == self.current_selection else "  "
            suffix = " <" if i == self.current_selection else ""
            content_lines.append(f"{prefix}{option}{suffix}")
        
        self._render_centered_content_with_scroll(stdscr, start_y, width, height, content_lines)

    def _render_equip_menu(self, stdscr, start_y, width, height):
        """Renderiza o menu para equipar itens."""
        content_lines = ["🧥 ESCOLHA UM ITEM PARA EQUIPAR", ""]
        equipable_items = self._get_equipable_items()
        
        if not equipable_items:
            content_lines.append("Você não tem itens equipáveis na mochila.")
        else:
            for i, item in enumerate(equipable_items):
                display_name = get_display_name(item)
                icon = self.item_icons.get(item.get('category', 'other'), '📦')
                slot = item.get('equip_slot', 'N/A').replace('_', ' ').capitalize()
                prefix = "> " if i == self.current_selection else "  "
                suffix = " <" if i == self.current_selection else ""
                content_lines.append(f"{prefix}{icon} {display_name} (Slot: {slot}){suffix}")
        
        content_lines.append("")
        prefix = "> " if len(equipable_items) == self.current_selection else "  "
        suffix = " <" if len(equipable_items) == self.current_selection else ""
        content_lines.append(f"{prefix}↩️ Voltar{suffix}")
        
        self._render_centered_content_with_scroll(stdscr, start_y, width, height, content_lines)

    def _render_unequip_menu(self, stdscr, start_y, width, height):
        """Renderiza o menu para desequipar itens."""
        content_lines = ["🧺 ESCOLHA UM ITEM PARA DESEQUIPAR", ""]
        equipped_items = self._player.get_equipped_items()

        if not equipped_items:
            content_lines.append("Você não tem itens equipados.")
        else:
            for i, item in enumerate(equipped_items):
                display_name = get_display_name(item)
                icon = self.item_icons.get(item.get('category', 'other'), '📦')
                slot_name = item.get('equipped_slot_friendly', 'N/A')
                prefix = "> " if i == self.current_selection else "  "
                suffix = " <" if i == self.current_selection else ""
                content_lines.append(f"{prefix}{icon} {display_name} ({slot_name}){suffix}")
        
        content_lines.append("")
        prefix = "> " if len(equipped_items) == self.current_selection else "  "
        suffix = " <" if len(equipped_items) == self.current_selection else ""
        content_lines.append(f"{prefix}↩️ Voltar{suffix}")
        
        self._render_centered_content_with_scroll(stdscr, start_y, width, height, content_lines)

    def _render_item_list_menu(self, stdscr, start_y, width, height):
        """Renderiza a lista de itens para ver detalhes."""
        content_lines = ["🔍 ESCOLHA UM ITEM PARA VER DETALHES", ""]
        inventory = self._player.get_inventory()
        
        if not inventory:
            content_lines.append("Sua mochila está vazia.")
        else:
            for i, item in enumerate(inventory):
                display_name = get_display_name(item)
                icon = self.item_icons.get(item.get('category', 'other'), '📦')
                prefix = "> " if i == self.current_selection else "  "
                suffix = " <" if i == self.current_selection else ""
                content_lines.append(f"{prefix}{icon} {display_name} x{item['quantity']}{suffix}")
        
        content_lines.append("")
        prefix = "> " if len(inventory) == self.current_selection else "  "
        suffix = " <" if len(inventory) == self.current_selection else ""
        content_lines.append(f"{prefix}↩️ Voltar{suffix}")

        self._render_centered_content_with_scroll(stdscr, start_y, width, height, content_lines)

    def _render_item_detail(self, stdscr, start_y, width, height):
        """Renderiza os detalhes de um item."""
        if not self.selected_item:
            self.feedback_message = "Item não encontrado!"
            self.current_menu = self.previous_menu or "main"
            return
            
        item = self.selected_item
        content_lines = []
        
        icon = self.item_icons.get(item.get('category', 'other'), '📦')
        content_lines.append(f"{icon} DETALHES: {get_display_name(item).upper()} {icon}")
        content_lines.append("-" * (width // 2))
        
        content_lines.append(f"Tipo: {item['category'].capitalize()}")
        content_lines.append(f"Quantidade: x{item['quantity']}")
        content_lines.append(f"Valor: {calculate_enhanced_value(item)} ouro")
        content_lines.append(f"Peso: {item.get('weight', 0):.1f} kg")
        
        if item.get('enhancement_level', 0) > 0:
            content_lines.append(f"⭐ Aprimoramento: +{item['enhancement_level']}")
        
        content_lines.append("")
        content_lines.append("📝 Descrição:")
        desc_lines = self._wrap_text(item.get('description', 'N/A'), width - 10)
        content_lines.extend([f"  {line}" for line in desc_lines])
        
        content_lines.append("")
        content_lines.append("⚙️ Atributos:")
        if item['category'] == 'weapon':
            content_lines.append(f"  Dano: {calculate_enhanced_damage(item)} {item.get('damage_type', '')}")
        elif item['category'] == 'armor':
            content_lines.append(f"  Resistência Física: +{item.get('physical_resistance', 0)}")
            content_lines.append(f"  Resistência Mágica: +{item.get('magical_resistance', 0)}")
        elif item['category'] == 'shield':
            content_lines.append(f"  Bônus de CA: +{item.get('armor_bonus', 0)}")
        
        content_lines.append("")
        content_lines.append("OPÇÕES")
        content_lines.append("-" * (width // 2))
        
        is_equipped = any(eq['inventory_id'] == item['inventory_id'] for eq in self._player.get_equipped_items())
        is_equipable = item.get('equip_slot') and not is_equipped

        options = []
        if is_equipable:
            options.append("🧥 Equipar este item")
        options.append("↩️ Voltar")

        for i, option in enumerate(options):
            prefix = "> " if i == self.current_selection else "  "
            suffix = " <" if i == self.current_selection else ""
            content_lines.append(f"{prefix}{option}{suffix}")
        
        self._render_centered_content_with_scroll(stdscr, start_y, width, height, content_lines)

    def _render_centered_content_with_scroll(self, stdscr, start_y, width, screen_height, content_lines):
        """Renderiza o conteúdo centralizado com suporte a scroll."""
        self.calculate_max_scroll(len(content_lines), screen_height, header_lines=start_y, footer_lines=1)
        
        for i, line in enumerate(content_lines):
            screen_y = start_y + i - self.scroll_offset
            
            if start_y <= screen_y < screen_height - 1:
                # Usa try-except para evitar crash ao redimensionar a janela
                try:
                    centered_line = line.center(width)
                    attr = curses.A_REVERSE if line.strip().startswith(">") and line.strip().endswith("<") else curses.A_NORMAL
                    stdscr.addstr(screen_y, 0, centered_line[:width-1], attr)
                except curses.error:
                    pass # Ignora erros de escrita fora da tela, comuns ao redimensionar

    def _wrap_text(self, text, max_width):
        """Quebra texto longo em várias linhas."""
        if max_width <= 0: return [text]
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 > max_width:
                lines.append(current_line)
                current_line = word
            else:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    def _get_equipable_items(self):
        """Retorna itens equipáveis que não estão equipados."""
        return [
            item for item in self._player.get_inventory() 
            if item.get('equip_slot') and not any(
                eq_item['inventory_id'] == item['inventory_id'] 
                for eq_item in self._player.get_equipped_items()
            )
        ]

    def _equip_selected_item(self, item_to_equip):
        """Equipa o item selecionado."""
        success, message = self._player.equip_item(item_to_equip['inventory_id'])
        display_name = get_display_name(item_to_equip)
        
        if success:
            self.feedback_message = f"{display_name} equipado com sucesso! ✅"
            self.current_menu = "main"
            self.current_selection = 0
        else:
            self.feedback_message = f"❌ Falha: {message}"

    def _unequip_selected_item(self, item_to_unequip):
        """Desequipa o item selecionado."""
        slot_tech = item_to_unequip.get('equipped_slot_technical')
        success, message = self._player.unequip_item(slot_tech)
        display_name = get_display_name(item_to_unequip)
        
        if success:
            self.feedback_message = f"{display_name} desequipado! ✅"
        else:
            self.feedback_message = f"❌ Falha: {message}"
        
        # Volta para o menu de desequipar e reseta a seleção
        self.current_selection = 0

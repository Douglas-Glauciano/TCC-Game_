# game/states/save_manager_state.py
import curses
import pyfiglet
from prettytable import PrettyTable
from ..base_state import BaseState
from game.database import load_characters, delete_character, rename_character
from game.i18n.translator import translator as t
from states.world.gameplay_state import GameplayState
from states.creation.character_creation_state import CharacterCreationState

class SaveManagerState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.step = "main"
        self.message = None
        self.characters = load_characters(self.game.db_conn)
        self.selected_char_id = None
        self.selected_char_name = None
        self.pending_action = None
        self.menu_options = []
        self.scrollable = True  # Ativar rolagem
        self.table_height = 0
        self.visible_table_rows = 0
        self._update_menu_options()

    def _update_menu_options(self):
        if not self.characters:
            self.menu_options = [
                t.t('back_to_main_menu'),
                t.t('create_new_character')
            ]
        else:
            self.menu_options = [
                t.t('load_game'),
                t.t('delete_save'),
                t.t('rename_character'),
                t.t('back_to_main_menu')
            ]

    def _reload_characters(self):
        self.characters = load_characters(self.game.db_conn)
        self.selected_char_id = None
        self.selected_char_name = None
        self.pending_action = None
        self._update_menu_options()
        self.current_selection = 0
        self.scroll_offset = 0  # Resetar scroll ao recarregar

    def _render_title(self, stdscr, title_text):
        """Renderiza o título em ASCII art centralizado"""
        height, width = stdscr.getmaxyx()
        ascii_lines = pyfiglet.figlet_format(title_text, font="slant", width=200).splitlines()
        
        for i, line in enumerate(ascii_lines):
            x = max((width - len(line)) // 2, 0)
            if i < height:
                stdscr.addstr(i, x, line)
        
        return len(ascii_lines)

    def _render_character_table(self, stdscr, start_y, highlight_index=None):
        """Renderiza a tabela de personagens usando PrettyTable com destaque para seleção"""
        if not self.characters:
            return start_y
            
        # Cria a tabela
        table = PrettyTable()
        table.field_names = [t.t('id'), t.t('name'), t.t('race'), t.t('class'), 
                        t.t('level'), t.t('gold'), t.t('difficulty')]
        table.align = 'l'
        table.header = True
        
        for i, char in enumerate(self.characters):
            table.add_row([
                char.id,
                char.name,
                char.race,
                char.char_class,
                char.level,
                char.gold,
                char.difficulty
            ])
        
        # Renderiza a tabela com suporte a rolagem
        table_str = str(table)
        table_lines = table_str.split('\n')
        self.table_height = len(table_lines)
        
        height, width = stdscr.getmaxyx()
        
        # Calcular quantas linhas da tabela são visíveis
        available_height = height - start_y - 5  # Deixa espaço para o menu e instruções
        self.visible_table_rows = min(self.table_height, available_height)
        
        # Calcular máximo de scroll
        self.calculate_max_scroll(self.table_height, height, start_y, 5)
        
        # Renderizar apenas as linhas visíveis
        for i in range(self.visible_table_rows):
            line_idx = i + self.scroll_offset
            if line_idx >= len(table_lines):
                break
                
            y = start_y + i
            if y >= height - 5:  # Não escrever além da tela
                break
                
            line = table_lines[line_idx]
            x = max((width - len(line)) // 2, 0)
            
            # Destacar a linha selecionada se estivermos na etapa de seleção
            # A linha de dados começa no índice 3 (data_start_line)
            data_start_line = 3
            if (highlight_index is not None and 
                line_idx == data_start_line + highlight_index):
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, line)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, line)
        
        return start_y + self.visible_table_rows + 1

    def render(self, stdscr):
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Renderiza o título baseado na etapa atual
        if self.step == "main":
            title = t.t('save_manager_title')
        elif self.step == "select_character":
            if self.pending_action == "load":
                title = t.t('select_character_to_load')
            elif self.pending_action == "delete":
                title = t.t('select_character_to_delete')
            elif self.pending_action == "rename":
                title = t.t('select_character_to_rename')
        elif self.step == "delete":
            title = t.t('confirm_delete', name=self.selected_char_name)
        elif self.step == "rename":
            title = t.t('enter_new_name_for', name=self.selected_char_name)
            
        title_height = self._render_title(stdscr, title)

        # Renderiza mensagem de feedback
        if self.message:
            msg_y = title_height + 1
            x = max((width - len(self.message)) // 2, 0)
            if msg_y < height:
                stdscr.addstr(msg_y, x, self.message)
            self.message = None

        # Renderiza conteúdo baseado na etapa atual
        content_start_y = title_height + 2
        
        if self.step == "main":
            if self.characters:
                menu_start_y = self._render_character_table(stdscr, content_start_y)
            else:
                no_chars_msg = t.t('no_saved_characters')
                x = max((width - len(no_chars_msg)) // 2, 0)
                if content_start_y < height:
                    stdscr.addstr(content_start_y, x, no_chars_msg)
                menu_start_y = content_start_y + 2
                
            # Renderiza o menu de opções
            for i, option in enumerate(self.menu_options):
                x = max((width - len(option)) // 2, 0)
                y = menu_start_y + i
                if y < height:
                    if i == self.current_selection:
                        stdscr.attron(curses.A_REVERSE)
                        stdscr.addstr(y, x, f"> {option} <")
                        stdscr.attroff(curses.A_REVERSE)
                    else:
                        stdscr.addstr(y, x, f"  {option}  ")
                        
        elif self.step == "select_character":
            # Renderiza a tabela com destaque para o personagem selecionado
            menu_start_y = self._render_character_table(stdscr, content_start_y, self.current_selection)
            
            # Instruções para o usuário
            instructions = t.t('use_arrows_select_enter_confirm_esc_cancel')
            if self.max_scroll > 0:
                instructions += " | PgUp/PgDn: Scroll"
            x = max((width - len(instructions)) // 2, 0)
            if menu_start_y < height:
                stdscr.addstr(menu_start_y, x, instructions)
            
        elif self.step == "delete":
            # Mensagem de confirmação
            confirm_msg = t.t('press_s_confirm_n_cancel')
            x = max((width - len(confirm_msg)) // 2, 0)
            if content_start_y < height:
                stdscr.addstr(content_start_y, x, confirm_msg)
            
        elif self.step == "rename":
            # Instruções para entrada de texto
            instructions = t.t('type_new_name_press_enter')
            x = max((width - len(instructions)) // 2, 0)
            if content_start_y < height:
                stdscr.addstr(content_start_y, x, instructions)

        # Mostrar indicador de scroll se necessário
        if self.step == "select_character" and self.max_scroll > 0:
            scroll_indicator = f"Scroll: {self.scroll_offset + 1}-{min(self.scroll_offset + self.visible_table_rows, self.table_height)}/{self.table_height}"
            x = max((width - len(scroll_indicator)) // 2, 0)
            if height - 2 >= 0:
                stdscr.addstr(height - 2, x, scroll_indicator, curses.A_DIM)

        stdscr.refresh()

    def handle_input(self):
        """Processa a entrada do usuário."""
        key = self.stdscr.getch()
        
        # Primeiro verifica se é um evento de rolagem
        if self.scrollable and self.step == "select_character" and self.handle_scroll_input(key):
            self.game.needs_render = True
            return
            
        if self.step == "main":
            if key in (curses.KEY_UP, ord('w'), ord('W')):
                self.current_selection = (self.current_selection - 1) % len(self.menu_options)
                self.game.needs_render = True
            elif key in (curses.KEY_DOWN, ord('s'), ord('S')):
                self.current_selection = (self.current_selection + 1) % len(self.menu_options)
                self.game.needs_render = True
            elif key in (curses.KEY_ENTER, 10, 13):
                self._handle_main_input()
            elif key == 27:  # ESC key
                from .main_menu_state import MainMenuState
                self.game.change_state(MainMenuState(self.game))
        
        elif self.step == "select_character":
            self._handle_select_character_input(key)
        
        elif self.step == "delete":
            self._handle_delete_input(key)
        
        elif self.step == "rename":
            self._handle_rename_input(key)

    def _handle_main_input(self):
        choice = self.current_selection
        
        if not self.characters:
            if choice == 0:
                from .main_menu_state import MainMenuState
                self.game.change_state(MainMenuState(self.game))
            elif choice == 1:
                self.game.change_state(CharacterCreationState(self.game))
            return
        
        if choice == 0:  # Carregar
            self.step = "select_character"
            self.pending_action = "load"
            self.current_selection = 0
            self.scroll_offset = 0  # Resetar scroll ao entrar na seleção
        elif choice == 1:  # Excluir
            self.step = "select_character"
            self.pending_action = "delete"
            self.current_selection = 0
            self.scroll_offset = 0  # Resetar scroll ao entrar na seleção
        elif choice == 2:  # Renomear
            self.step = "select_character"
            self.pending_action = "rename"
            self.current_selection = 0
            self.scroll_offset = 0  # Resetar scroll ao entrar na seleção
        elif choice == 3:  # Voltar
            from .main_menu_state import MainMenuState
            self.game.change_state(MainMenuState(self.game))
        
        self.game.needs_render = True

    def _handle_select_character_input(self, key):
        if key in (curses.KEY_UP, ord('w'), ord('W')):
            self.current_selection = (self.current_selection - 1) % len(self.characters)
            # Ajustar scroll se necessário
            if self.current_selection < self.scroll_offset:
                self.scroll_offset = max(0, self.current_selection)
            self.game.needs_render = True
        elif key in (curses.KEY_DOWN, ord('s'), ord('S')):
            self.current_selection = (self.current_selection + 1) % len(self.characters)
            # Ajustar scroll se necessário
            if self.current_selection >= self.scroll_offset + self.visible_table_rows - 3:  # -3 para compensar o cabeçalho
                self.scroll_offset = min(self.max_scroll, self.current_selection - self.visible_table_rows + 4)
            self.game.needs_render = True
        elif key in (curses.KEY_ENTER, 10, 13):
            selected_char = self.characters[self.current_selection]
            self.selected_char_id = selected_char.id
            self.selected_char_name = selected_char.name
            
            if self.pending_action == "load":
                self._load_character(selected_char)
            elif self.pending_action == "delete":
                self.step = "delete"
                self.game.needs_render = True
            elif self.pending_action == "rename":
                self.step = "rename"
                self.game.needs_render = True
        elif key == 27:  # ESC key
            self.step = "main"
            self.current_selection = 0
            self.scroll_offset = 0
            self.game.needs_render = True

    def _handle_delete_input(self, key):
        if key in (ord('s'), ord('S'), ord('y'), ord('Y')):
            if delete_character(self.game.db_conn, self.selected_char_id):
                self.message = t.t('character_deleted', name=self.selected_char_name)
                self._reload_characters()
                self.step = "main"
            else:
                self.message = t.t('delete_failed')
                self.step = "main"
        elif key in (ord('n'), ord('N'), 27):  # ESC or N
            self.step = "main"
            self.message = t.t('delete_cancelled')
        
        self.game.needs_render = True

    def _handle_rename_input(self, key):
        if key == 27:  # ESC key
            self.step = "main"
            self.message = t.t('rename_cancelled')
            self.game.needs_render = True
            return
        
        # Habilita a entrada de texto
        curses.echo()
        curses.curs_set(1)
        
        height, width = self.stdscr.getmaxyx()
        prompt = t.t('enter_new_name_prompt', name=self.selected_char_name)
        x = max((width - len(prompt)) // 2, 0)
        y = height // 2
        
        self.stdscr.addstr(y, x, prompt)
        self.stdscr.refresh()
        
        # Obtém a entrada do usuário
        new_name = self.stdscr.getstr(y + 1, x, 30).decode('utf-8').strip()
        
        # Desabilita a entrada de texto
        curses.noecho()
        curses.curs_set(0)
        
        if new_name:
            if rename_character(self.game.db_conn, self.selected_char_id, new_name):
                self.message = t.t('character_renamed', old_name=self.selected_char_name, new_name=new_name)
                self._reload_characters()
            else:
                self.message = t.t('rename_failed')
        else:
            self.message = t.t('rename_cancelled')
        
        self.step = "main"
        self.game.needs_render = True

    def _load_character(self, character):
        """Carrega o personagem e inicia o jogo"""
        if character.hp <= 0:
            character.hp = character.hp_max
        
        self.game.player = character
        self.game.change_state(GameplayState(self.game))
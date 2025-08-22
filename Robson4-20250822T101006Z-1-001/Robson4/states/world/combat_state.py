# game/states/combat_state.py
import curses
import pyfiglet
from ..base_state import BaseState
from game.combat import Combat
from game.database import save_character

class CombatState(BaseState):
    """
    Gerencia a interface de usuário e o fluxo do combate usando Curses.
    """
    def __init__(self, game, db_conn):
        super().__init__(game)
        self.conn = db_conn
        self.combat_phase = "player_turn" # Fases: player_turn, monster_turn, end_screen
        self.menu_options = ["Atacar", "Fugir"]
        self.current_selection = 0
        self.title_art = pyfiglet.Figlet(font='slant').renderText("COMBATE!")
        self.scrollable = True
        self.scroll_offset = 0
        self.combat = None
        self.result = None  # Adicionado para armazenar o resultado do combate

    def enter(self):
        """Prepara o estado de combate, criando uma nova instância de Combat."""
        self.combat = Combat(self.game.player, self.conn, self.stdscr)
        self.game.needs_render = True

    def render(self, stdscr):
        """Renderiza a tela de combate usando Curses."""
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Renderizar título
        title_lines = self.title_art.split('\n')
        for i, line in enumerate(title_lines):
            if i < height - 1:
                safe_line = line[:width-1]
                stdscr.addstr(i, (width - len(safe_line)) // 2, safe_line, curses.A_BOLD)
        
        y_pos = len(title_lines)

        # Se o combate não foi inicializado, mostrar mensagem de erro
        if self.combat is None:
            error_msg = "Erro: Combate não inicializado!"
            stdscr.addstr(y_pos + 1, (width - len(error_msg)) // 2, error_msg, curses.A_BOLD)
            stdscr.refresh()
            return

        # Renderizar status do jogador e monstro
        player_table, monster_table = self.combat.get_status_tables()
        
        # Converter as tabelas em strings e depois dividir em linhas
        player_str = player_table.get_string()
        monster_str = monster_table.get_string()
        
        player_lines = player_str.split('\n')
        monster_lines = monster_str.split('\n')
        
        table_y = y_pos + 1
        
        # Calcular a posição horizontal para centralizar as tabelas
        # Tabela do jogador à esquerda
        player_width = len(player_lines[0]) if player_lines else 0
        player_x = (width // 4) - (player_width // 2)
        if player_x < 0:
            player_x = 0
        
        # Tabela do monstro à direita
        monster_width = len(monster_lines[0]) if monster_lines else 0
        monster_x = (3 * width // 4) - (monster_width // 2)
        if monster_x < 0:
            monster_x = 0

        # Renderizar tabela do jogador
        for i, line in enumerate(player_lines):
            if table_y + i < height - 1:
                # Truncar a linha se for muito longa
                truncated_line = line[:width-1]
                stdscr.addstr(table_y + i, player_x, truncated_line)
        
        # Renderizar tabela do monstro
        for i, line in enumerate(monster_lines):
            if table_y + i < height - 1:
                truncated_line = line[:width-1]
                stdscr.addstr(table_y + i, monster_x, truncated_line)

        # Renderizar log de combate
        log_y = table_y + max(len(player_lines), len(monster_lines)) + 2
        if log_y < height - 1:
            stdscr.addstr(log_y, (width - 20) // 2, "--- LOG DE COMBATE ---", curses.A_UNDERLINE)
        
        # Calcular rolagem do log
        log_height = height - log_y - 4
        if log_height > 0:
            self.calculate_max_scroll(len(self.combat.combat_log), log_height)
            
            # Mostrar apenas as mensagens visíveis
            visible_log = self.combat.combat_log[self.scroll_offset:self.scroll_offset + log_height]
            
            for i, log_msg in enumerate(visible_log):
                line_pos = log_y + i + 1
                if line_pos < height - 2:
                    # Centralizar a mensagem
                    msg_x = max(2, (width - len(log_msg)) // 2)
                    # Truncar a mensagem para caber na tela
                    truncated_msg = log_msg[:width-4]
                    stdscr.addstr(line_pos, msg_x, truncated_msg)

        # Renderizar menu de ações
        menu_y = height - 4
        if self.combat_phase == "player_turn" and menu_y < height:
            for i, option in enumerate(self.menu_options):
                x = (width - len(option)) // 2
                line_pos = menu_y + i
                if line_pos < height:
                    attr = curses.A_REVERSE if i == self.current_selection else curses.A_NORMAL
                    stdscr.addstr(line_pos, x, option, attr)

        # Instruções de rolagem
        if self.max_scroll > 0 and height - 1 < height:
            scroll_info = "↑/↓ para rolar, PgUp/PgDn para rolar rápido"
            stdscr.addstr(height - 1, (width - len(scroll_info)) // 2, scroll_info, curses.A_DIM)

        stdscr.refresh()

    def handle_input(self):
        """Lida com a entrada do usuário e controla o fluxo dos turnos."""
        key = self.stdscr.getch()
        
        # Primeiro verifica se é um evento de rolagem
        if self.scrollable and self.handle_scroll_input(key):
            self.game.needs_render = True
            return
            
        # Depois verifica navegação normal do menu
        if self.combat_phase == "player_turn":
            if key in (curses.KEY_UP, ord('w'), ord('W')):
                self.current_selection = (self.current_selection - 1) % len(self.menu_options)
                self.game.needs_render = True
            elif key in (curses.KEY_DOWN, ord('s'), ord('S')):
                self.current_selection = (self.current_selection + 1) % len(self.menu_options)
                self.game.needs_render = True
            elif key in (curses.KEY_ENTER, 10, 13, ord(' ')):  # Incluindo espaço como Enter
                if self.current_selection == 0:  # Atacar
                    monster_dead = self.combat.player_attack()
                    if monster_dead:
                        self.combat.victory()
                        self.combat_phase = "end_screen"
                        self.result = "victory"  # Definir resultado
                    else:
                        # Monstro ataca
                        player_dead = self.combat.monster_attack()
                        if player_dead:
                            permadeath = self.combat.defeat()
                            self.combat_phase = "end_screen"
                            self.result = "permadeath" if permadeath else "defeat"  # Definir resultado
                else:  # Fugir
                    fled = self.combat.attempt_flee()
                    if fled:
                        self.combat_phase = "end_screen"
                        self.result = "fled"  # Definir resultado
                    else:
                        # Se não fugiu, monstro ataca
                        player_dead = self.combat.monster_attack()
                        if player_dead:
                            permadeath = self.combat.defeat()
                            self.combat_phase = "end_screen"
                            self.result = "permadeath" if permadeath else "defeat"  # Definir resultado
                
                self.game.needs_render = True

        elif self.combat_phase == "end_screen":
            if key in (curses.KEY_ENTER, 10, 13):
                self._exit_combat()

    def _exit_combat(self):
        """Muda para o estado apropriado após o combate."""
        from states.system.main_menu_state import MainMenuState

        if self.result == "permadeath":
            self.game.change_state(MainMenuState(self.game))
        else:
            # Para vitória, derrota ou fuga, volta ao gameplay usando pop_state
            save_character(self.conn, self.game.player)
            self.game.pop_state()
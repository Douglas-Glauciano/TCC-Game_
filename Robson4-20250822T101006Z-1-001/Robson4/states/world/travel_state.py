# game/states/travel_state.py
from ..base_state import BaseState
from game.database import save_character
import curses

class TravelState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.menu_options = [
            "Lindenrock (Vila nas Montanhas)",
            "Vallengar (Cidade Portuaria)",
            "Cancelar"
        ]

    def render(self, stdscr):
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Centralizar conteúdo
        content_width = min(50, width - 4)
        left_margin = (width - content_width) // 2
        
        # Garantir que não tentamos escrever além dos limites da tela
        separator = "=" * content_width
        stdscr.addstr(0, left_margin, separator, curses.A_BOLD)
        
        title = "DESTINOS DISPONIVEIS"
        title_x = left_margin + (content_width - len(title)) // 2
        if 1 < height:
            stdscr.addstr(1, title_x, title, curses.A_BOLD)
        
        if 2 < height:
            stdscr.addstr(2, left_margin, separator, curses.A_BOLD)
        
        # Menu de opções
        row = 3
        for idx, option in enumerate(self.menu_options):
            if row >= height - 1:  # Não escrever além da tela
                break
                
            option_text = f"> {option}" if idx == self.current_selection else f"  {option}"
            option_x = left_margin + (content_width - len(option)) // 2 - 1
            if option_x + len(option_text) > width:
                option_text = option_text[:width - option_x]
                
            attr = curses.A_REVERSE if idx == self.current_selection else curses.A_NORMAL
            stdscr.addstr(row, option_x, option_text, attr)
            row += 1
        
        # Instruções de navegação (só se houver espaço)
        instructions = "Seta Cima/Baixo: Navegar  Enter: Selecionar"
        if height - 1 >= 0 and len(instructions) <= width:
            instructions_x = (width - len(instructions)) // 2
            stdscr.addstr(height - 1, instructions_x, instructions, curses.A_DIM)

    def execute_choice(self):
        if self.current_selection == 0:
            self._travel_to("lindenrock")
        elif self.current_selection == 1:
            self._travel_to("vallengar")
        
        self.game.pop_state()

    def _travel_to(self, city_name):
        self.game.player.last_wilderness = self.game.player.location
        self.game.player.location = city_name
        save_character(self.game.db_conn, self.game.player)
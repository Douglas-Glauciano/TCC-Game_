# BaseState.py - Modificado para suportar rolagem avançada
import curses

class BaseState:
    """Classe base para todos os estados do jogo."""
    
    def __init__(self, game):
        self.game = game
        self.stdscr = self.game.stdscr
        self.current_selection = 0
        self.menu_options = []
        
        # Sistema de rolagem
        self.scroll_offset = 0
        self.max_scroll = 0
        self.scrollable = False  # Estados devem definir isso como True se precisarem de rolagem

    def render(self, stdscr):
        stdscr.clear()
        
    def handle_input(self):
        """Método para lidar com a entrada do usuário para navegação de menu."""
        key = self.stdscr.getch()
        
        # Primeiro verifica se é um evento de rolagem
        if self.scrollable and self.handle_scroll_input(key):
            self.game.needs_render = True
            return
            
        # Depois verifica navegação normal do menu
        if key in (curses.KEY_UP, ord('w'), ord('W')):
            self.current_selection = (self.current_selection - 1) % len(self.menu_options)
            self.game.needs_render = True
        elif key in (curses.KEY_DOWN, ord('s'), ord('S')):
            self.current_selection = (self.current_selection + 1) % len(self.menu_options)
            self.game.needs_render = True
        elif key in (curses.KEY_LEFT, ord('a'), ord('A')):
            self.handle_left_key()
            self.game.needs_render = True
        elif key in (curses.KEY_RIGHT, ord('d'), ord('D')):
            self.handle_right_key()
            self.game.needs_render = True
        elif key in (curses.KEY_ENTER, 10, 13, ord(' ')):  # Incluindo espaço como Enter
            self.execute_choice()
            self.game.needs_render = True
        elif key == 27:  # Tecla Escape
            self.handle_escape()
            self.game.needs_render = True
            
    def handle_scroll_input(self, key):
        """Processa entrada de rolagem. Retorna True se a tecla foi usada para rolagem."""
        # Detectar Ctrl+setas (códigos podem variar por terminal)
        try:
            # Tentativa de detectar Ctrl+setas (depende do terminal)
            if key == curses.KEY_CTRL_UP or key == 566:  # Ctrl+Up
                self.scroll_offset = max(0, self.scroll_offset - 5)
                return True
            elif key == curses.KEY_CTRL_DOWN or key == 525:  # Ctrl+Down
                self.scroll_offset = min(self.max_scroll, self.scroll_offset + 5)
                return True
            elif key == curses.KEY_CTRL_LEFT or key == 545:  # Ctrl+Left
                # Alguns estados podem usar rolagem horizontal
                return False
            elif key == curses.KEY_CTRL_RIGHT or key == 560:  # Ctrl+Right
                # Alguns estados podem usar rolagem horizontal
                return False
        except:
            # Se as constantes não existirem, continuar com outras verificações
            pass
            
        # Verificações padrão
        if key == curses.KEY_UP:
            self.scroll_offset = max(0, self.scroll_offset - 1)
            return True
        elif key == curses.KEY_DOWN:
            self.scroll_offset = min(self.max_scroll, self.scroll_offset + 1)
            return True
        elif key == curses.KEY_PPAGE:  # Page Up
            self.scroll_offset = max(0, self.scroll_offset - 10)
            return True
        elif key == curses.KEY_NPAGE:  # Page Down
            self.scroll_offset = min(self.max_scroll, self.scroll_offset + 10)
            return True
        elif key == 337:  # Shift + Up (alguns terminais)
            self.scroll_offset = max(0, self.scroll_offset - 3)
            return True
        elif key == 336:  # Shift + Down (alguns terminais)
            self.scroll_offset = min(self.max_scroll, self.scroll_offset + 3)
            return True
            
        # Tentativa de detectar roda do mouse (depende do terminal)
        try:
            if key == curses.KEY_MOUSE:
                _, mx, my, _, bstate = curses.getmouse()
                if bstate & curses.BUTTON4_PRESSED:  # Roda para cima
                    self.scroll_offset = max(0, self.scroll_offset - 3)
                    return True
                elif bstate & curses.BUTTON5_PRESSED:  # Roda para baixo
                    self.scroll_offset = min(self.max_scroll, self.scroll_offset + 3)
                    return True
                elif bstate & curses.BUTTON1_PRESSED:  # Clique do mouse
                    self.handle_mouse_click(mx, my)
                    return True
        except:
            # Mouse não suportado ou erro ao acessar
            pass
            
        return False
        
    def handle_left_key(self):
        """Método para lidar com a tecla esquerda. Estados podem sobrescrever."""
        pass
        
    def handle_right_key(self):
        """Método para lidar com a tecla direita. Estados podem sobrescrever."""
        pass
        
    def handle_escape(self):
        """Método para lidar com a tecla Escape. Estados podem sobrescrever."""
        # Comportamento padrão: voltar ao estado anterior
        if hasattr(self.game, 'state_stack') and len(self.game.state_stack) > 1:
            self.game.pop_state()
        
    def handle_mouse_click(self, x, y):
        """Método para lidar com cliques do mouse. Estados podem sobrescrever."""
        # Comportamento padrão: verificar se o clique foi em uma opção de menu
        if not self.menu_options:
            return
            
        # Calcular a posição do menu (depende da implementação do render)
        # Estados devem sobrescrever este método para implementar clique no menu
        pass
        
    def calculate_max_scroll(self, content_height, screen_height, header_lines=0, footer_lines=0):
        """Calcula o máximo de rolagem possível baseado no conteúdo e tamanho da tela."""
        visible_area = screen_height - header_lines - footer_lines
        self.max_scroll = max(0, content_height - visible_area)
        # Garante que o offset atual não exceda o máximo
        self.scroll_offset = min(self.scroll_offset, self.max_scroll)
        
    def execute_choice(self):
        """Método para executar a escolha do menu."""
        pass
        
    def enter(self):
        """Método opcional para executar ao entrar no estado."""
        pass
        
    def exit(self):
        """Método opcional para executar ao sair do estado."""
        pass
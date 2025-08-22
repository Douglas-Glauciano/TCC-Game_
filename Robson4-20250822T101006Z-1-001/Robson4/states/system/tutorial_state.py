# states/system/tutorial_state.py
import curses
from ..base_state import BaseState
import pyfiglet

class TutorialState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.pages = self._create_tutorial_pages()
        self.current_page = 0
        self.menu_options = ["Próxima Página", "Voltar ao Menu"]

    def _create_tutorial_pages(self):
        """Cria todas as páginas do tutorial com seus conteúdos"""
        return [
            {
                "title": "Introdução ao Rust Dice",
                "content": [
                    "Bem-vindo ao Rust Dice, um jogo inspirado no D&D 5e!",
                    "",
                    "Neste jogo de RPG baseado em texto, você criará um",
                    "personagem, explorará um mundo perigoso, enfrentará",
                    "monstros e completará missões.",
                    "",
                    "Use as setas para navegar e Enter para selecionar.",
                    "Pressione ESC a qualquer momento para voltar."
                ]
            },
            {
                "title": "Atributos e Modificadores",
                "content": [
                    "Seu personagem possui 6 atributos principais:",
                    "",
                    "- Força (FOR): Ataques físicos e capacidade de carga",
                    "- Destreza (DES): CA, iniciativa e ataques à distância",
                    "- Constituição (CON): Pontos de vida e resistência",
                    "- Inteligência (INT): Magias e perícias de conhecimento",
                    "- Sabedoria (SAB): Percepção, intuição e vontade",
                    "- Carisma (CAR): Persuasão e liderança",
                    "",
                    "Modificadores:",
                    "10-11: +0, 12-13: +1, 14-15: +2",
                    "16-17: +3, 18-19: +4, 20: +5"
                ]
            },
            {
                "title": "Sistema de Combate",
                "content": [
                    "O combate é por turnos com as seguintes mecânicas:",
                    "",
                    "1. Iniciativa: determina a ordem de combate (1d20 + DES)",
                    "2. Ataque: rolagem de ataque vs CA do alvo",
                    "   Ataque = 1d20 + modificador + bônus de proficiência",
                    "3. Dano: valor da arma - resistência do alvo",
                    "",
                    "Tipos de dano:",
                    "- Físico: reduzido pela resistência física",
                    "- Mágico: reduzido pela resistência mágica",
                    "",
                    "Crítico: natural 20 dobra os dados de dano"
                ]
            },
            {
                "title": "Perícias e Progressão",
                "content": [
                    "As perícias estão vinculadas aos atributos:",
                    "",
                    "- Força: Atletismo",
                    "- Destreza: Acrobacia, Furtividade, Prestidigitação",
                    "- Inteligência: Arcanismo, História, Investigação",
                    "         Natureza, Religião",
                    "- Sabedoria: Intuição, Medicina, Percepção, Sobrevivência",
                    "- Carisma: Atuação, Enganação, Intimidação, Persuasão",
                    "",
                    "Sistema de progressão:",
                    "- Perícias melhoram com o uso",
                    "- Níveis mais altos desbloqueiam perks especiais"
                ]
            },
            {
                "title": "Cidades e Serviços",
                "content": [
                    "Vallengar e Lindenrock oferecem serviços:",
                    "",
                    "Lojas:",
                    "- Armas: equipamento de combate",
                    "- Armaduras: proteção adicional",
                    "- Poções: itens de recuperação",
                    "",
                    "Estalagem:",
                    "- Cura completa por uma taxa",
                    "- Local seguro para descansar",
                    "",
                    "Ferraria:",
                    "- Melhoria de equipamentos existentes",
                    "- Aumenta dano e durabilidade"
                ]
            },
            {
                "title": "Dificuldade e Morte",
                "content": [
                    "O jogo oferece vários níveis de dificuldade:",
                    "",
                    "- Aventura Leve: para iniciantes",
                    "- Desafio Justo: equilíbrio recomendado",
                    "- Provação Maldita: para veteranos",
                    "- Caminho da Dor: apenas para os corajosos",
                    "- Maldição de Ferro: desafio extremo",
                    "- Inferno Vivo: praticamente impossível",
                    "",
                    "Morte permanente:",
                    "- Se ativada, a morte é definitiva",
                    "- Se desativada, perde itens e ouro ao morrer"
                ]
            },
            {
                "title": "Dicas de Jogabilidade",
                "content": [
                    "Dicas para sobreviver em Rust Dice:",
                    "",
                    "1. Equilibre seu grupo de atributos",
                    "2. Mantenha poções de cura sempre à mão",
                    "3. Melhore equipamentos na ferraria",
                    "4. Descanse regularmente para recuperar HP",
                    "5. Fuja de combates muito difíceis",
                    "6. Use perícias apropriadas para cada situação",
                    "",
                    "Lembre-se: a estratégia é tão importante",
                    "quanto a força bruta!"
                ]
            }
        ]

    def render(self, stdscr):
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Renderiza o título da página atual
        title = self.pages[self.current_page]["title"]
        ascii_title = pyfiglet.figlet_format(title, font="small", width=width)
        ascii_lines = ascii_title.splitlines()
        
        # Encontra a altura real do título (ignorando linhas vazias)
        title_height = 0
        for i, line in enumerate(ascii_lines):
            if line.strip():
                x = max((width - len(line)) // 2, 0)
                if i < height:
                    stdscr.addstr(i, x, line, curses.A_BOLD)
                title_height = i + 1
        
        # Renderiza o conteúdo da página
        content = self.pages[self.current_page]["content"]
        content_start_y = title_height + 1
        
        for i, line in enumerate(content):
            y = content_start_y + i
            if y < height - 3:  # Deixa espaço para o menu de navegação
                x = max((width - len(line)) // 2, 0)
                stdscr.addstr(y, x, line)
        
        # Renderiza o menu de navegação
        nav_y = height - 2
        
        # Indicador de página
        page_info = f"Página {self.current_page + 1}/{len(self.pages)}"
        stdscr.addstr(nav_y, (width - len(page_info)) // 2, page_info)
        
        # Opções de navegação
        if self.current_page < len(self.pages) - 1:
            next_text = "Próxima Página"
            next_x = width - len(next_text) - 2
            if self.current_selection == 0:
                stdscr.addstr(nav_y, next_x, next_text, curses.A_REVERSE)
            else:
                stdscr.addstr(nav_y, next_x, next_text)
        
        back_text = "Voltar ao Menu"
        back_x = 2
        if self.current_selection == 1 or (self.current_page == len(self.pages) - 1 and self.current_selection == 0):
            stdscr.addstr(nav_y, back_x, back_text, curses.A_REVERSE)
        else:
            stdscr.addstr(nav_y, back_x, back_text)
        
        stdscr.refresh()

    def handle_input(self):
        key = self.stdscr.getch()
        
        if key in (curses.KEY_LEFT, ord('a')):
            self.current_selection = (self.current_selection - 1) % 2
            self.game.needs_render = True
            
        elif key in (curses.KEY_RIGHT, ord('d')):
            self.current_selection = (self.current_selection + 1) % 2
            self.game.needs_render = True
            
        elif key in (curses.KEY_ENTER, 10, 13):
            if self.current_selection == 0 and self.current_page < len(self.pages) - 1:
                # Próxima página
                self.current_page += 1
                self.current_selection = 0
                self.game.needs_render = True
            else:
                # Voltar ao menu
                self.game.pop_state()
                self.game.needs_render = True
                
        elif key == 27:  # ESC
            self.game.pop_state()
            self.game.needs_render = True

    def execute_choice(self):
        # Não é usado neste estado, mas precisa estar presente
        pass
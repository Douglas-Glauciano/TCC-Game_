# states/system/credits_state.py
import curses
from ..base_state import BaseState
import pyfiglet

# states/system/team_details_state.py
import curses
from ..base_state import BaseState
import pyfiglet

class TeamDetailsState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.members = self._create_team_members()
        self.current_member = 0
        self.scrollable = True
        self.menu_options = ["Membro Anterior", "Voltar", "Próximo Membro"]

    def _create_team_members(self):
        return [
            {
                "name": "Hannah",
                "easier_read": "",
                "role": "Desenvolvedora Principal",
                "fun_fact": "Programou 99,999999% do jogo sozinha 💻"
            },
            {
                "name": "Colegas de curso",
                "easier_read": "",
                "role": "Testadores & Ideias",
                "fun_fact": "São responsáveis por bugs... digo, *features*! 🐛"
            },
            {
                "name": "Professores (Renan, Lyniker, Piero)",
                "easier_read": "(Renan, Lyniker, Piero)",
                "role": "Orientação Acadêmica",
                "fun_fact": "Sempre pediam documentação extra 📚"
            }
        ]

    def render(self, stdscr):
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        member = self.members[self.current_member]

        # Renderiza título
        ascii_title = pyfiglet.figlet_format(member["name"], font="small", width=width)
        for i, line in enumerate(ascii_title.splitlines()):
            x = max((width - len(line)) // 2, 0)
            try:
                stdscr.addstr(i, x, line, curses.A_BOLD)
            except curses.error:
                pass

        y = len(ascii_title.splitlines()) + 2
        info = [
            f"{member['easier_read']}",
            "",
            f"Função: {member['role']}",
            "",
            f"Curiosidade: {member['fun_fact']}"
        ]

        for line in info:
            x = max((width - len(line)) // 2, 0)
            try:
                stdscr.addstr(y, x, line)
            except curses.error:
                pass
            y += 1

        # Barra inferior
        nav_text = f"Membro {self.current_member + 1}/{len(self.members)}"
        stdscr.addstr(height - 2, (width - len(nav_text)) // 2, nav_text)

        # Opções
        option_spacing = width // (len(self.menu_options) + 1)
        for i, option in enumerate(self.menu_options):
            x = option_spacing * (i + 1) - len(option) // 2
            if i == self.current_selection:
                stdscr.addstr(height - 1, x, option, curses.A_REVERSE)
            else:
                stdscr.addstr(height - 1, x, option)

        stdscr.refresh()

    def handle_input(self):
        key = self.stdscr.getch()

        if key in (curses.KEY_LEFT, ord('a')):
            self.current_selection = (self.current_selection - 1) % len(self.menu_options)
            self.game.needs_render = True
        elif key in (curses.KEY_RIGHT, ord('d')):
            self.current_selection = (self.current_selection + 1) % len(self.menu_options)
            self.game.needs_render = True
        elif key in (curses.KEY_ENTER, 10, 13):
            selected = self.menu_options[self.current_selection]

            if selected == "Próximo Membro":
                self.current_member = (self.current_member + 1) % len(self.members)
            elif selected == "Membro Anterior":
                self.current_member = (self.current_member - 1) % len(self.members)
            elif selected == "Voltar":
                self.game.pop_state()

            self.current_selection = 0
            self.game.needs_render = True

        elif key == 27:  # ESC
            self.game.pop_state()
            self.game.needs_render = True


class CreditsState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.pages = self._create_credits_pages()
        self.current_page = 0
        self.menu_options = self._get_navigation_options()
        self.scrollable = True  # Ativa o sistema de rolagem

    def _get_navigation_options(self):
        """Retorna as opções de navegação baseadas na página atual"""
        if self.current_page == 0:
            return ["Próxima Página", "Voltar ao Menu"]
        elif self.current_page == len(self.pages) - 1:
            return ["Página Anterior", "Voltar ao Menu"]
        elif self.current_page == 4:  # Página "Agradecimentos"
            return ["Página Anterior", "Ver Equipe com Detalhes", "Voltar ao Menu", "Próxima Página"]
        else:
            return ["Página Anterior", "Voltar ao Menu", "Próxima Página"]

    def _create_credits_pages(self):
        """Cria todas as páginas de créditos/documentação"""
        return [
            {
                "title": "Créditos - Rust Dice",
                "content": [
                    "Rust Dice - Um RPG baseado em texto",
                    "Inspirado no D&D 5ª Edição",
                    "",
                    "Desenvolvido como projeto de TCC (Durante 6 meses)",
                    "Curso de Ciência da Computação",
                    "Ano: 2025",
                    "",
                    "Este jogo demonstra conceitos de:",
                    "- Programação orientada a objetos",
                    "- Design patterns",
                    "- Persistência de dados",
                    "- Interface baseada em terminal",
                    "",
                    "Desenvolvido por:",
                    "- Hannah"
                ]
            },
            {
                "title": "Tecnologias Utilizadas",
                "content": [
                    "Linguagem: Python 3.12.10",
                    "Interface: Biblioteca curses",
                    "Banco de dados: SQLite3",
                    "",
                    "Bibliotecas principais:",
                    "- curses: Interface terminal",
                    "- pyfiglet: ASCII art",
                    "- pandas: Manipulação de dados",
                    "- prettytable: Formatação de tabelas",
                    "- SQLite3: Armazenamento e manipulação de dados",
                    "",
                    "Arquitetura:",
                    "- Padrão State para gerenciamento de telas",
                    "- Sistema modular e expansível",
                    "",
                    "Ferramentas:",
                    "- Visual Studio Code: Editor de código",
                    "- Git, GitHub e Drive: Controle de versão",
                    "- DB Browser for SQLite: Gerenciamento do BD",
                    "- Venv: Ambiente virtual Python",
                    "",
                    "Sistema Operacional: Windows 10/11"
                ]
            },
            {
                "title": "Recursos e Inspirações",
                "content": [
                    "Inspirado no D&D 5ª Edição da Wizards of the Coast",
                    "",
                    "Sistema de atributos baseado em D&D:",
                    "- Força, Destreza, Constituição,",
                    "- Inteligência, Sabedoria, Carisma",
                    "",
                    "Sistema de combate inspirado em RPGs clássicos",
                    "",
                    "Elementos de progressão de personagem:",
                    "- Sistema de níveis e experiência",
                    "- Perícias baseadas em atributos",
                    "- Equipamentos e melhorias"
                ]
            },
            {
                "title": "Características do Projeto",
                "content": [
                    "Principais funcionalidades implementadas:",
                    "",
                    "✓ Sistema completo de criação de personagem",
                    "✓ Sistema de combate baseado em turnos",
                    "✓ Sistema de inventário e equipamentos",
                    "✓ Mecânicas de exploração e descanso",
                    "✓ Sistema de cidades com serviços",
                    "✓ Diferentes níveis de dificuldade",
                    "✓ Sistema de salvamento e carregamento",
                    "✓ Interface localizável (pt-BR/en-US)"
                ]
            },
            {
                "title": "Agradecimentos",
                "content": [
                    "Agradecimentos Especiais:",
                    "",
                    "À Universidade e Orientadores:",
                    "(Especialmente aos Docentes Renan, Lyniker e Piero)",
                    "- Pelo suporte técnico e acadêmico",
                    "- Pela orientação durante o desenvolvimento",
                    "",
                    "Aos Colegas de Curso:",
                    "- Pelo feedback e testes durante o desenvolvimento",
                    "- Pelo compartilhamento de conhecimentos",
                    "",
                    "À Comunidade de Desenvolvimento:",
                    "- Pelos recursos e tutoriais disponíveis",
                    "- Pelo código aberto que inspirou soluções",
                    "",
                    "Aos Jogadores de RPG:",
                    "- Pelas ideias e sugestões de gameplay",
                    "- Pelo entusiasmo que motivou o projeto",
                    "",
                    "E a todos que apoiaram este projeto!",
                ]
            },









            #____________________________________________________________________________________
            #(separacao das paginas serias e das memes)
            {
                "title": "Extra Secreto",
                "content": [
                    "O quê...? Você ainda está aqui?",
                    "",
                    "Os créditos já acabaram faz tempo!",
                    "Não tem mais nada pra ver, juro 😅"
                ]
            },
            {
                "title": "Ainda Aqui?",
                "content": [
                    "Sério mesmo?",
                    "",
                    "Tá bom então, aqui vai um coelho fofo:",
                    "(\\_._/) ",
                    "( •_• ) ",
                    "/ >❤️   ",
                    "",
                    "Pronto, agora pode ir!"
                ]
            },
            {
                "title": "Ok, Última Página",
                "content": [
                    "Eu já não tenho mais o que colocar aqui...",
                    "",
                    "Talvez uma curiosidade inútil:",
                    "Sabia que em D&D um dado d20 tem icosaedro como nome técnico?",
                    "",
                    "Impressionante, né? Não? 😅"
                ]
            },
            {
                "title": "Chega!",
                "content": [
                    "Agora é sério!",
                    "Se você ainda está rolando, você oficialmente:",
                    "",
                    "GANHOU +1 de Paciência",
                    "GANHOU +1 de Carisma",
                    "",
                    "Obrigado de verdade por jogar 💖"
                ]
            },
            {
                "title": "Fim de Verdade!",
                "content": [
                    "Tá... agora acabou MESMO.",
                    "",
                    "Desliga o jogo e vá tomar uma água! 💧",
                    "",
                    "Até a próxima aventura!",
                    "– Hannah"
                ]
            }

        ]

    def render(self, stdscr):
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Atualiza as opções de navegação baseadas na página atual
        self.menu_options = self._get_navigation_options()
        
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
                    try:
                        stdscr.addstr(i, x, line, curses.A_BOLD)
                    except curses.error:
                        pass
                title_height = i + 1
        
        # Renderiza o conteúdo da página com suporte a rolagem
        content = self.pages[self.current_page]["content"]
        content_start_y = title_height + 1
        
        # Calcula a rolagem máxima para esta página
        self.calculate_max_scroll(
            content_height=len(content),
            screen_height=height,
            header_lines=title_height + 1,
            footer_lines=2 +1 # Barra de navegação
        )
        
        # Renderiza apenas as linhas visíveis
        for i, line in enumerate(content):
            # Pula linhas que estão acima da área visível devido à rolagem
            if i < self.scroll_offset:
                continue
                
            y = content_start_y + i - self.scroll_offset
            # Para de renderizar se ultrapassar a área visível
            if y >= height - 2:
                break
                
            x = max((width - len(line)) // 2, 0)
            try:
                stdscr.addstr(y, x, line)
            except curses.error:
                # Ignora erros de renderização fora da tela
                pass
        
        # Renderiza o menu de navegação
        nav_y = height - 2
        
        # Indicador de página e posição de rolagem
        scroll_info = f"Página {self.current_page + 1}/{len(self.pages)}"
        if self.max_scroll > 0:
            scroll_info += f" | Pos: {self.scroll_offset + 1}-{min(len(content), self.scroll_offset + height - title_height - 3)}/{len(content)}"
        stdscr.addstr(nav_y, (width - len(scroll_info)) // 2, scroll_info)
        
        # Opções de navegação - distribuídas horizontalmente
        option_spacing = width // (len(self.menu_options) + 1)
        
        for i, option in enumerate(self.menu_options):
            x = option_spacing * (i + 1) - len(option) // 2
            if i == self.current_selection:
                stdscr.addstr(nav_y, x, option, curses.A_REVERSE)
            else:
                stdscr.addstr(nav_y, x, option)
        
        stdscr.refresh()

    def handle_input(self):
        # Primeiro tenta processar rolagem (herdado do BaseState)
        key = self.stdscr.getch()
        if self.handle_scroll_input(key):
            self.game.needs_render = True
            return
            
        # Depois processa navegação entre páginas
        if key in (curses.KEY_LEFT, ord('a')):
            self.current_selection = (self.current_selection - 1) % len(self.menu_options)
            self.game.needs_render = True
            
        elif key in (curses.KEY_RIGHT, ord('d')):
            self.current_selection = (self.current_selection + 1) % len(self.menu_options)
            self.game.needs_render = True
            
        elif key in (curses.KEY_ENTER, 10, 13):
            selected_option = self.menu_options[self.current_selection]
            
            if selected_option == "Próxima Página":
                self.current_page = min(self.current_page + 1, len(self.pages) - 1)
                self.scroll_offset = 0  # Reseta a rolagem ao mudar de página
                self.current_selection = 0
                self.game.needs_render = True
                
            elif selected_option == "Página Anterior":
                self.current_page = max(self.current_page - 1, 0)
                self.scroll_offset = 0  # Reseta a rolagem ao mudar de página
                self.current_selection = 0
                self.game.needs_render = True
                
            elif selected_option == "Voltar ao Menu":
                self.game.pop_state()
                self.game.needs_render = True
            
            elif selected_option == "Ver Equipe com Detalhes":
                self.game.push_state(TeamDetailsState(self.game))

        elif key == 27:  # ESC
            self.game.pop_state()
            self.game.needs_render = True


    def execute_choice(self):
        # Não é usado neste estado, mas precisa estar presente
        pass
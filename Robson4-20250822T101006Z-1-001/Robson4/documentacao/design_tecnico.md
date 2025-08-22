# Design Técnico — Rust Dice: Echoes of Prometheus

---

## 1. Ficha Técnica

* **Nome do Projeto:** Rust Dice: Echoes of Prometheus
* **Plataforma:** Terminal (Windows, com executável `.exe`)
* **Gênero:** RPG por Turnos
* **Linguagem:** Python 3.x
* **Principais Bibliotecas:** `json`, `sqlite3`, `random`
* **Formato de Save:** Banco de dados SQLite

---

## 2. Equipe e Responsabilidades

* **Game Design & Narrativa:**
* **Programação Backend:**
* **Programação Frontend:**
* **Programação SQL:**
* **Arte & Assets:**
* **Sons:**
* **Testes:**

---

## 3. Estrutura Geral do Projeto

```text
├── README.md
├── build.bat
├── main.py
├── requirements.txt
├── build/
├── data/
│   ├── __init__.py
│   ├── data_tuples.py
│   ├── database.db
│   └── populate_db.py
├── dist/
│   ├── Rust_Dice.exe
│   ├── data/
│   │   └── database.db
│   └── documentacao/
├── documentacao/
│   ├── change_log.md
│   ├── design.md
│   ├── design_tecnico.md
│   ├── historia.md
│   ├── planejamento.md
│   ├── referencias.md
│   └── tutorial.md
├── game/
│   ├── __init__.py
│   ├── character.py
│   ├── combat.py
│   ├── config.py
│   ├── database.py
│   ├── db_queries.py
│   ├── menus.py
│   ├── monster.py
│   ├── name_generator.py
│   └── utils.py
└── states/
    ├── __init__.py
    ├── base_state.py
    ├── character/
    │   ├── __init__.py
    │   ├── attributes_state.py
    │   └── inventory_state.py
    ├── city/
    │   ├── __init__.py
    │   ├── blacksmith_state.py
    │   ├── city_hub_base.py
    │   ├── inn_state.py
    │   ├── shop_state.py
    │   ├── lindenrock/
    │   │   └── hub.py
    │   └── vallengar/
    │       └── hub.py
    ├── creation/
    │   ├── __init__.py
    │   ├── character_creation_state.py
    │   └── character_name_creator_state.py
    ├── system/
    │   ├── __init__.py
    │   ├── delete_confirmation_state.py
    │   ├── difficulty_state.py
    │   ├── main_menu_state.py
    │   ├── save_manager_state.py
    │   └── settings_state.py
    └── world/
        ├── __init__.py
        ├── combat_state.py
        ├── explore_state.py
        ├── gameplay_state.py
        └── rest_state.py
```
Usamos do modelo de desenovlvimento de jogos Concept → Identificar riscos → Prototipar → Testar → Refinar criado por Jesse Schell no livro "A arte do game design", além de outros exemplos, como;

Visão Holística do Design:
O livro aborda o jogo como um sistema integrado, onde mecânicas, narrativa, tecnologia e estética devem reforçar um tema central 4. Por exemplo:

"Em 'Don't Starve', a ausência de tutoriais reforça a temática de sobrevivência" 4.
Isso ajuda a criar experiências coesas, algo crucial para um projeto acadêmico bem-avaliado.

---

## 4. Descrição dos Módulos e Principais Arquivos

### Diretório `game/`

* **character.py:** Implementa a lógica da criação e atributos do personagem.
* **combat.py:** Contém regras e mecânicas do sistema de combate por turnos.
* **config.py:** Configurações gerais do jogo, constantes e parâmetros.
* **database.py:** Manipulação do banco SQLite e abstração das operações.
* **db\_queries.py:** Consultas específicas ao banco, centralizando SQL.
* **menus.py:** Menus interativos do jogo, controle de navegação.
* **monster.py:** Definição e geração de monstros inimigos.
* **name\_generator.py:** Geração procedural de nomes com base em cultura e gênero.
* **utils.py:** Funções utilitárias e auxiliares usadas por vários módulos.

### Diretório `states/`

Arquivos que controlam os estados do jogo, cada pasta segmenta uma área de atuação:

* **base\_state.py:** Classe base para estados, controle geral do fluxo.
* **character/**: Estados relacionados ao personagem (atributos, inventário).
* **city/**: Estados que representam as cidades e suas funcionalidades (lojas, estalagem, ferraria).
* **creation/**: Estados dedicados à criação do personagem e nome.
* **system/**: Estados do sistema geral (menu principal, gerenciamento de saves, configurações).
* **world/**: Estados do mundo aberto (combate, exploração, descanso, gameplay).

---

## 5. Fluxo Geral do Jogo

```ascii
main.py
   │
   ├── Inicializa configurações e banco de dados
   │
   ├── Entra no estado Main Menu (states/system/main_menu_state.py)
   │
   ├── Criação ou carregamento do personagem (states/creation/)
   │
   ├── Transição para exploração e gameplay (states/world/gameplay_state.py)
   │
   ├── Eventos de exploração, combate (states/world/explore_state.py, combat_state.py)
   │
   ├── Interação com cidades e NPCs (states/city/)
   │
   └── Gerenciamento do inventário e atributos (states/character/)
```

Este fluxo é gerenciado por uma máquina de estados (State Machine), permitindo controle modular e escalável.

---

## 6. Bibliotecas Utilizadas e Justificativas

| Biblioteca         | Uso Principal                                         | Justificativa                                              |
| ------------------ | ----------------------------------------------------- | ---------------------------------------------------------- |
| `json`             | Serialização e leitura de configurações e dados       | Simplicidade e padrão para dados estruturados              |
| `sqlite3`          | Banco de dados para saves e tabelas do jogo           | Leve, embutido no Python, permite consultas SQL eficientes |
| `random`           | Geração de números aleatórios para eventos e combates | Elemento fundamental para RPGs clássicos                   |
| `Textual` (futuro) | Interface gráfica baseada em terminal                 | Modernizar UI, maior interatividade e estética             |

---

## 7. Banco de Dados SQLite

### Estrutura e Relações Principais

* **Tabela `characters`**: Armazena dados básicos do personagem (nome, atributos, classe, nível).
* **Tabela `items`**: Definição dos itens disponíveis no jogo (armas, armaduras, consumíveis).
* **Tabela `inventory`**: Relação entre personagens e itens em posse.
* **Tabela `monsters`**: Dados dos monstros para encontros aleatórios.
* **Tabela `saves`**: Gerenciamento de múltiplos saves de jogadores.

As tabelas são relacionadas principalmente via IDs, garantindo integridade referencial e eficiência nas consultas.

---
## 8. Ferramentas Utilizadas no Desenvolvimento

* **Visual Studio Code** — Editor de código-fonte principal.
* **DB Browser for SQLite** — Ferramenta para manipulação visual do banco de dados SQLite.
* **Drive** — Controle de versão e colaboração.
* **Python 3.10+** — Linguagem de programação do projeto.
* **PyInstaller** — Criação do executável `.exe`.
* **Notion / Google Docs** — Documentação e organização do projeto.


## 9. Considerações Finais

O design técnico do Rust Dice foi estruturado para promover modularidade, escalabilidade e facilidade de manutenção. A escolha por Python e SQLite visa agilidade no desenvolvimento e portabilidade. A implementação futura da biblioteca Textual representa o compromisso com a evolução da interface, mantendo a experiência de terminal com alta qualidade.
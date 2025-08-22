# Rust Dice: Echoes of Prometheus - RPG por Turnos (Com exe funcional)

## Ficha Técnica
- **Nome do Projeto:** Rust Dice: Echoes of Prometheus
- **Plataforma:** Terminal (Windows, com .exe)
- **Gênero:** RPG por Turnos
- **Linguagem:** Python 3.x
- **Bibliotecas Principais:** json, sqlite3, random
- **Formato de Save:** SQLite

## Equipe e Responsabilidades
- **Game Design & Narrativa:**
- **Programação back:**
- **Programação front:**
- **Programação SQL:**
- **Arte & Assets:**
- **Sons:**
- **Testes:**

## Visão Geral
Rust Dice é um RPG clássico por turnos, que mistura exploração, combate tático e criação profunda de personagens, tudo rodando no terminal. Inspirado em clássicos como D&D e Skyrim.

## Como Executar

### Pelo terminal
```bash
python main.py


## Visão Geral
Rust Dice é um RPG por turnos em terminal que recria a experiência clássica de RPGs de mesa e videogame. O jogo oferece criação de personagem profunda, combate tático baseado em atributos, exploração de mundo e progressão de personagem.

## Funcionalidades Implementadas

### 🧙 Sistema de Criação de Personagem
- **Gênero e Nome**: 
  - Escolha manual ou geração aleatória baseada em gênero e cultura
- **Raças**: 
  - Modificadores nos 6 atributos básicos: Força, Destreza, Constituição, Inteligência, Sabedoria, Carisma
- **Classes**: 
  - Valores iniciais de Vida/Mana
  - Armadura e item inicial
- **Antecedentes**: 
  - Modificadores em perícias (sistema em desenvolvimento)
- **Rolagem de Atributos**:
  - Rerolagem total ou individual
- **Dificuldade**: 
  - Vinculada ao permadeath (opções futuras: separação)

### 🎮 Menu Principal
- Gerenciamento de Saves:
  - Carregar, Deletar, Renomear personagens
- Opções: 
  - Novo Jogo, Sair

### 🌍 Gameplay Principal
- **Exploração**:
  - Encontros aleatórios com inimigos
  - Eventos de "nada acontece"
- **Descanso**:
  - Recuperação de vida com modificadores de atributos
  - Risco de emboscada
- **Viagem**:
  - Movimento entre cidades (Vallengar e Lindenrock)

### 📊 Menu do Personagem (Sempre Acessível)
1. **Atributos**: Visualização detalhada
2. **Inventário**:
   - Visualização de itens equipados
   - Sistema de equipar/desequipar
3. **Opções**:
   - Alterar dificuldade
   - Salvar e continuar
   - Salvar e sair
   - Deletar personagem

### ⚔️ Sistema de Combate (Turn-based)
- **Mecânicas**:
  - X1 contra monstros nivelados
  - Ataque = Atributo da arma + modificador vs CA do monstro
  - Dano = Valor da arma - Defesa física
  - Opções: Atacar ou Fugir
- **Consequências**:
  - **Vitória**: Ouro, XP + chance de item aleatório
  - **Derrota**: Perda de ouro + chance de perder item + revive com 1 HP

### 🏙️ Cidades (Vallengar & Lindenrock)
- **Lojas**:
  - 3 tipos com itens especializados
- **Estalagem**:
  - Cura completa mediante pagamento
- **Ferraria**:
  - Melhoria de equipamentos

(Updates feitos que precisam ser atualizados no indice acima
Sistema atualizado de resistencia fisica e magica, funcional
Permadeath separado da dificuldade
)
## História Geral
A narrativa completa do mundo de **Eledrathor** e das Expedições está no arquivo [historia.md](documentacao/historia.md).  
Abaixo um resumo introdutório:
> Eledrathor é um cadáver cósmico que ainda respira. Uma terra onde magia ancestral se mistura com tecnologia rústica...


## Como Executar

### Para executar pelo terminal:
```bash
python main.py
```

### Para criar o executável:
```bash
.\build.bat
```

### Outros comandos úteis:
```bash
# Gerar árvore de diretórios
python gerate_tree.py

# Popular banco de dados (apaga todos os dados ja existentes para os sobreescrever)
python data/populate_db.py
```
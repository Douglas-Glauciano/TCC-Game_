# 📜 Changelog

Este documento registra todas as alterações significativas, melhorias e correções aplicadas ao projeto.  
As versões seguem o padrão semântico adaptado para o contexto de desenvolvimento do TCC, conforme a estrutura abaixo.

---

## 📌 Padrão de Versionamento

O versionamento é composto por três dígitos, seguindo a lógica **`[Estrutural].[Ajuste].[Novos Recursos]`**:

- **Primeiro dígito (Estrutural)** → Alterações que impactam a arquitetura ou base do projeto.  
- **Segundo dígito (Ajuste)** → Ajustes, correções de bugs ou refatorações.  
- **Terceiro dígito (Novos Recursos)** → Inclusão de novas funcionalidades ou melhorias visuais.  

---

## 🔖 Versão 1.0.0 — 1 de agosto de 2025
### 🏗️ Estrutura Inicial
- Criação da base do projeto em **Python**.  
- Implementação do **sistema de estados** (`MainMenu`, `CharacterCreation`, `Combat`, etc.).  
- Integração com **curses** para futura interface visual em terminal.  
- Estruturação do **sistema de personagens** (atributos básicos, HP, MP, equipamentos iniciais).  
- Sistema de **dados persistentes em SQLite** (personagens, itens, raças, classes, monstros).  
- Adicionado **fluxo inicial de criação de personagem**.  

---

## 🔖 Versão 1.0.1 — 8 de agosto de 2025
### ✨ Novos Recursos
- **Sistema de Combate:**  
  - Adicionada **resistência mágica** para personagens e inimigos.  
  - Agora parte do **dano mágico é mitigado** com base em atributos e equipamentos.  
  - Expande a variedade de **builds possíveis**.  

---

## 🔖 Versão 1.1.0 — 10 de agosto de 2025
### 🏗️ Alterações Estruturais
- **Migração gradual** da interface tradicional em terminal → **curses**.  
- **Refatoração da estrutura de pastas**, separando **lógica do jogo** e **camadas de interface**.  
- Criação de **`BaseState`** para unificar comportamento dos estados do jogo.  

---

## 🔖 Versão 1.1.1 — 11 de agosto de 2025
### ⚙️ Ajustes e Otimizações
- **Sistema de Dificuldade:**  
  - Separada a mecânica de **morte permanente (`permadeath`)** das opções de dificuldade.  
  - Agora pode ser **ativado ou desativado independentemente**.  
  - Aumenta a **personalização** e **liberdade** do jogador.  

---

## 🔖 Versão 1.2.0 — 14 de agosto de 2025
### 🏗️ Alterações Estruturais
- **Refatoração de Interface:**  
  - Transição de menus e exibições para **curses** (bordas, cores, navegação com setas e números).  
  - Substituição do **Colorama/PrettyTable** antigos.  

- **Sistema de Inventário e Equipamentos:**  
  - Itens agora podem ser **equipados/desequipados** corretamente, retornando ao inventário quando removidos.  
  - Integração do inventário com **banco de dados**.  

---

## 🔖 Versão 1.2.1 — 15 de agosto de 2025
### ⚙️ Ajustes e Otimizações
- **Sistema de Idiomas:**  
  - Criação de **variáveis centralizadas** para textos exibidos.  
  - Implementação da **troca dinâmica** entre **Português** e **Inglês** (parcial).  
  - Primeira etapa do **sistema multilíngue** concluída.  

---

## 🔖 Versão 1.2.2 — 20 de agosto de 2025
### ✨ Novos Recursos
- **Menus Iniciais:**  
  - Adicionados menus de **Tutorial** e **Créditos** no menu principal.  
  - Totalmente adaptados para **curses** (navegação por setas, números e enter).  
  - Auxiliam o jogador e documentam o projeto de forma **profissional**.  



  
## Cronograma e Priorização
Level = prioridade (🟥 alta, 🟧 média, 🟩 baixa)
Hard = quao dificil
| Módulo           | Tarefa                                       | Level | Hard | Prazo Estimado | Status      |
|------------------|----------------------------------------------|-------|------|----------------|------------ |
| Sistema Perícias | Aplicar ingame, com funcao e forma de upar   | 🟥   | 3    | xx/xx/2025     | 🔲 Pendente |
| Combate          | Implementar resistência mágica               | 🟧   | 2    | xx/xx/2025     | ✅ Concluído|
| Dificuldade      | Separar permadeath de dificuldade            | 🟧   | 2    | xx/xx/2025     | ✅ Concluído|
| NPCs             | Implementar diálogos básicos                 | 🟩   | 1    | xx/xx/2025     | 🔲 Pendente |
| Linguagem        | Implementar troca de idioma in-game          | 🟥   | 4    | xx/xx/2025     | ✅ Concluído|
| Linguagem        | Portar todos textos visuais para variaveis   | 🟩   | 3    | xx/xx/2025     | 🔲 Pendente |
| Som              | Criar sons básicos, trilha sonora e efeitos  | 🟩   | 4    | xx/xx/2025     | 🔲 Pendente |
| Documentação     | Organizar toda a documentação do TCC         | 🟩   | 4    | xx/xx/2025     | 🔲 Pendente |
| Trabalgho word   | Escrever todo o TCC no word, com ABNT        | 🟩   | 5    | xx/xx/2025     | 🔲 Pendente |

### **Legenda e Critérios de Classificação**

Para padronizar a avaliação de cada tarefa no cronograma, utilizamos uma escala de **1 a 4** para a **Prioridade** e a **Dificuldade**.
---


#### **Prioridade (level)**
Este valor indica a **urgência e o impacto estratégico** da tarefa para o projeto. Tarefas com prioridade mais alta devem ser a principal meta do ciclo de desenvolvimento atual.

* **1 (Baixa):** Tarefa com baixo impacto na funcionalidade principal ou na apresentação do TCC. Sua execução pode ser adiada, sendo ideal para momentos de tempo livre. Exemplo: melhorias estéticas ou funcionalidades extras.
* **2 (Média):** Tarefa importante para a qualidade ou a experiência do usuário, mas não é um bloqueador para o desenvolvimento de outros sistemas. Requer atenção, mas pode ser planejada com flexibilidade.
* **3 (Alta):** Tarefa **crucial** para o avanço do projeto. Sua conclusão é necessária para que outras etapas possam ser iniciadas. O progresso deve ser monitorado de perto.
* **4 (Urgente):** Tarefa **crítica** que exige atenção imediata. Geralmente, são *bugs* que impedem o funcionamento de sistemas essenciais ou funcionalidades necessárias para a apresentação final do projeto. Sua execução deve ser priorizada sobre qualquer outra tarefa.
---


#### **Dificuldade (hard)**
Este valor reflete o **esforço e a complexidade técnica estimados** para a conclusão da tarefa. É uma métrica essencial para o planejamento e a alocação de tempo da equipe.

* **1 (Baixa):** Tarefa simples e direta, com uma solução conhecida. O tempo de execução é curto, geralmente levando poucas horas.
* **2 (Média):** Tarefa moderadamente complexa. Pode exigir a integração de componentes existentes ou uma pequena refatoração, mas a solução é clara e viável em um prazo de dias.
* **3 (Alta):** Tarefa que demanda um esforço significativo. Envolve desafios técnicos, a necessidade de pesquisa ou um tempo de desenvolvimento prolongado.
* **4 (Muito Alta):** Tarefa de **altíssima complexidade e imprevisibilidade**. Pode envolver a exploração de novas tecnologias, a criação de um sistema do zero ou a solução de problemas sem precedentes, exigindo um planejamento robusto e um tempo considerável de dedicação.
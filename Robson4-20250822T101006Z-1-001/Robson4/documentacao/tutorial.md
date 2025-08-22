- [ ] Guia básico para começar a jogar.
- [ ] Explicação dos menus e opções.
- [ ] Conceitos-chave (CA, modificadores, perícias).
- [ ] Atalhos ou comandos no terminal.
- [ ] Futuro tutorial integrado no jogo (explicar como será).




exemplo para abnt
### **Estrutura Proposta para a Documentação**

**1. Elementos Pré-Textuais (As Partes Iniciais)**
*   **Capa e Folha de Rosto:** Seguem modelos rigidamente definidos pela ABNT.  A Eliana deveria fornecer um.
*   **Titulo e subtitulo:** obrigatorios,
*   **Resumo e Abstract:** Descreva brevemente o problema (ex: "Falta de jogos complexos para rodar em máquinas simples"), a metodologia (desenvolvimento em Python), os principais resultados (um jogo funcional com sistema de batalha por turnos) e conclusões.
*   **Sumário:** Gerado automaticamente pelo Word depois que você aplicar os estilos de título.

**2. Elementos Textuais (O Corpo do Trabalho)**

**INTRODUÇÃO (Capítulo 1)**
*   **Contexto:** Fale sobre a indústria de games, a relevância de RPGs e o nicho de jogos em terminal (performance, acessibilidade, desafio puro de programação).
*   **Problema:** Qual foi a dificuldade técnica ou de design que motivou o projeto? (ex: "Como implementar um sistema de combate estratégico e balanceado usando apenas interfaces de texto?")
*   **Objetivo Geral:** Desenvolver um protótipo de RPG por turnos funcional em Python rodando em terminal.
*   **Objetivos Específicos:**
    *   Modelar as classes e entidades do jogo (Personagem, Inimigo, Habilidade).
    *   Implementar um sistema de batalha baseado em turnos com opções estratégicas.
    *   Criar um sistema de progressão (nível, experiência, itens).
    *   Testar e balancear os valores numéricos do jogo (dano, vida, custo de habilidades).
*   **Justificativa:** Por que esse projeto é válido? (Aprendizado profundo em POO, lógica de game, Python; é um projeto viável para o tempo do TCC).
*   **Escopo e Limitações:** Deixe claro que o foco é na mecânica, não na história ou gráficos. A limitação é o terminal.

**REFERENCIAL TEÓRICO (Capítulo 2)**
*Aqui você mostra que pesquisou e entende os conceitos por trás do seu trabalho.*
*   **Conceitos de Game Design:** O que é um RPG? O que define um jogo por turnos? Fale sobre elementos como HP, MP, Dano, Defesa, Estado Alterado (Status Effect).
*   **Programação Orientada a Objetos (POO):** Explique os pilares (Encapsulamento, Herança, Polimorfismo) e como eles se aplicam ao seu projeto (ex: a classe `Personagem` é herdada por `Guerreiro` e `Mago`).
*   **Linguagem Python:** Por que ela foi escolhida? Fale sobre sua simplicidade, legibilidade e bibliotecas úteis (como `random` para cálculos de chance).
*   **Design Patterns (Opcional, mas MUITO valorizado):** Se você usou algum padrão de projeto, como Factory para criar inimigos ou Singleton para gerenciar o estado do jogo, essa é a hora de explicá-lo.

**METODOLOGIA (Capítulo 3)**
*Como vocês fizeram o trabalho. Isso é crucial.*
*   **Tipo de Pesquisa:** Pesquisa aplicada, de natureza qualitativa (avaliação da jogabilidade) e quantitativa (teste de balanceamento), procedimento técnico-laboratorial (desenvolvimento).
*   **Ferramentas Utilizadas:**
    *   **Software:** Visual Studio Code (editor), Python (linguagem), Git (controle de versão - **USE ISSO!**).
    *   **Hardware:** Computadores com Windows.
*   **Etapas de Desenvolvimento:** Descreva o processo. Provavelmente foi uma adaptação de Agile/Scrum para um grupo pequeno.
    *   **Planejamento:** Definição de mecânicas, criação de diagramas.
    *   **Implementação:** Divisão de tarefas (ex: "João fez a classe de combate, Maria fez o sistema de itens").
    *   **Testes:** Como foi feito o teste e balanceamento? (ex: "Foram realizados combates de teste e ajustados os valores de dano e vida iterativamente").

**DESENVOLVIMENTO DO JOGO (Capítulo 4 - O Mais Importante)**
*O coração do seu TCC. Use muitos diagramas, pseudocódigos e prints do terminal.*
*   **Arquitetura do Sistema:** Mostre um diagrama de como as partes se conectam.
    *   **Diagrama de Classes:** **ESSENCIAL.** Mostre as classes (`Personagem`, `Inimigo`, `Habilidade`, `Item`) e seus atributos e métodos.
*   **Fluxo do Jogo:** Um diagrama de atividade mostrando o loop principal: "Inicio -> Exibir Menu -> Combate -> Processar Turno -> Fim de Combate -> Fim".
*   **Mecânicas Principais:**
    *   **Sistema de Combate:** Detalhe o algoritmo de um turno. Como o jogador escolhe a ação, como o alvo é selecionado, como o dano é calculado (`dano = ataque - defesa * random(0.8, 1.2)`).
    *   **Sistema de Progressão:** Como ganha experiência? Como sobe de nível? Como os atributos são aumentados?
    *   **Sistema de Itens/Habilidades:** Como eles são armazenados e seus efeitos aplicados.
*   **Implementação de Trechos de Código Cruciais:** Não coloque o código inteiro aqui. Selecione as partes mais importantes, como a função principal de cálculo de dano ou a máquina de estados do turno, e comente-as.

**RESULTADOS E DISCUSSÕES (Capítulo 5)**
*O que vocês conseguiram fazer e uma análise crítica disso.*
*   **Apresentação do Produto:** Inclua prints do jogo em funcionamento: menu inicial, tela de combate, tela de vitória.
*   **Análise das Mecânicas:** Discussão sobre o balanceamento. "O inimigo X se mostrou muito fraco, então ajustamos sua vida de 50 para 70". "A habilidade Y era muito overpowered, então adicionamos um custo de MP maior".
*   **Dificuldades Encontradas e Soluções:** Problemas técnicos são ótimos de se comentar! "Tivemos um bug onde o turno não passava; descobrimos que era um loop infinito e corrigimos implementando...". Isso mostra capacidade de debug.
*   **Limitações do Projeto:** O que não ficou tão bom ou não foi implementado? (ex: "Não foi possível implementar IA para os inimigos, eles apenas usam ataques aleatórios").

**CONCLUSÃO (Capítulo 6)**
*   **Retomada dos Objetivos:** Reafirme rapidamente o que foi proposto.
*   **Síntese dos Resultados:** O que foi efetivamente alcançado.
*   **Trabalhos Futuros:** O que poderia ser feito depois? Adicionar uma história, criar inimigos com IA, transformar em um jogo online, adicionar mais classes, implementar uma interface gráfica (usando PyGame ou Tkinter).

**3. Elementos Pós-Textuais**
*   **Referências:** Liste todos os livros, sites (como Stack Overflow, documentação do Python), vídeos e artigos que você usou.
*   **Anexos:** Local perfeito para colocar **o código-fonte completo** do projeto.
*   **Apêndices (Opcional):** Manual do jogador, transcript de uma sessão de jogo completa.

---

**Dica Final:** Seu diferencial será a **clareza técnica**. Use e abuse de diagramas UML (de classe, de sequência, de atividade) para explicar sua arquitetura. Isso transforma uma simples documentação em um projeto de alto nível.

# Diadema

**Diadema** é um projeto modular focado em automatizar o processo de networking e candidatura a vagas no LinkedIn (e outras plataformas), usando inteligência artificial local, automação de navegação e integração com bots de mensagem.

O objetivo é eliminar a repetição de tarefas manuais, economizar tempo e aumentar as chances de ser notado pelo RH, tudo de maneira automatizada e personalizável.

## Módulos

- **conexao-bot:** Automação para aumentar conexões no LinkedIn, focando em perfis de RH e tech recruiters.
- **aplicacao-bot:** Automação do processo de candidatura em vagas, preenchendo formulários automaticamente.
- **scroll-filter-bot:** Bot para rolar o feed e filtrar vagas postadas, podendo já aplicar ou notificar o usuário.
- **llm-core:** Núcleo de IA local, responsável por interpretar páginas, tomar decisões e gerar respostas.
- **shared:** Código utilitário e componentes comuns (ex: integração com Telegram, banco, configs).

> O projeto é 100% modular. Cada bot pode ser executado de forma independente ou integrada, usando Docker.

## Como começar

1. Instale as dependências em cada módulo (`npm install` ou `pip install`, conforme a stack).
2. Configure as variáveis de ambiente necessárias.
3. Rode cada bot individualmente, ou use o `docker-compose.yml` para rodar tudo junto.
4. Veja os READMEs individuais para instruções de cada parte.

---

## **3. README.md de cada módulo (exemplo para conexao-bot/README.md)**

```markdown
# Conexao-Bot

Módulo responsável por automatizar o aumento de conexões no LinkedIn, focando principalmente em perfis de RH e tech recruiters.

## Funcionalidades

- Adiciona automaticamente até 200 conexões por semana.
- Faz scraping para identificar perfis estratégicos.
- Pode ser configurado para contato inicial via mensagem automatizada.

## Tecnologias sugeridas

- Node.js/Python
- Playwright ou Selenium

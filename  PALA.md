# LinkedinFarm — PALA

## Visão Geral

O LinkedinFarm é uma suíte modular de automações para LinkedIn (e futuramente outros sites de vagas), criada para facilitar o networking, aumentar conexões relevantes e automatizar candidaturas. O objetivo é eliminar tarefas repetitivas, poupar tempo e maximizar a exposição do perfil para recrutadores, usando inteligência artificial local, automação web e integração com Telegram.
- Automação de conexões
- Aplicação automática em vagas
- Filtro/scroll infinito de vagas postadas

Tudo integrado com uma LLM local (rodando na própria máquina), Telegram para notificações e banco de dados para armazenamento de histórico.

## Estrutura Modular

### 1. Conexao-Bot
- Automatiza conexões, priorizando RH e tech recruiters
- Pode enviar mensagem automatizada na conexão

### 2. Aplicacao-Bot
- Preenche formulários de candidatura em vagas automaticamente
- A LLM processa o HTML das páginas, decide os campos e executa as ações
- Em caso de erro após várias tentativas, aciona o usuário pelo Telegram

### 3. Scroll-Filter-Bot
- Com uma rede de contatos suficiente, faz scroll infinito no feed em busca de vagas postadas por RHs
- Filtra oportunidades e pode aplicar automaticamente ou avisar o usuário

### 4. LLM-Core
- Núcleo inteligente para processar HTML, decidir ações e gerar mensagens/respostas personalizadas
- Local, sem depender de APIs pagas (precisa de GPU)

### 5. Shared
- Utilitários comuns: integração Telegram, banco de dados, configs, logging etc.

## Tecnologias Sugeridas

- Node.js/Python (principalmente para automação)
- Playwright/Selenium para automação web
- Telegram API para alertas/notificações
- Banco de dados simples (SQLite ou MongoDB)
- LLM local (ex: GPT4All, LM Studio, Ollama, etc)
- Docker para modularização e deploy

## Fluxo Resumido (inspirado no diagrama SkyDraw)

- **Conexão:** Bot identifica perfis-alvo e adiciona à rede
- **Aplicação:** LLM recebe HTML da vaga, tenta aplicar usando os dados do usuário, avisa no Telegram se der erro
- **Scrolling:** Quando a rede está grande, bot faz scroll no feed, captura vagas, filtra/interage/aplica conforme a IA decidir

## Observações

- Projeto pensado para ser expandido e mantido por vários devs ao mesmo tempo
- Modularidade é prioridade: cada componente pode evoluir isoladamente


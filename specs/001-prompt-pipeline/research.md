# Technical Research: Pull, Otimização e Push de Prompts via LangSmith

Este documento descreve as decisões de arquitetura e pesquisas técnicas realizadas para a feature `001-prompt-pipeline`.

## 1. Integração com LangSmith Hub (Pull e Push)

### Decisão de Integração

Utilizar o módulo `hub` integrado do `langchain` para download e upload de prompts.

### Raciocínio de Integração

A biblioteca `langchain` oferece métodos nativos e performáticos para interagir com o LangSmith Prompt Hub:

- `hub.pull("leonanluppi/bug_to_user_story_v1")` retorna o objeto `ChatPromptTemplate` contendo as mensagens.
- `hub.push("{username}/bug_to_user_story_v2", prompt_template, new_repo_is_public=True)` publica o prompt otimizado e o torna visível publicamente no hub.

### Alternativas Consideradas de Integração

Utilizar chamadas diretas à API REST do LangSmith. Rejeitado devido à complexidade extra de gerenciar payloads HTTP e autenticação manual quando o SDK do LangChain já encapsula isso.

---

## 2. Estrutura do Prompt YAML e Serialização

### Decisão de Formato e Serialização

Salvar e ler os prompts usando formato YAML com chaves planas para system_prompt, user_prompt e metadados, facilitando a manipulação e a execução dos testes unitários estruturais.

### Raciocínio de Formato e Serialização

O formato YAML é legível para humanos e fácil de versionar via Git. A serialização nativa do LangChain (JSON completo do prompt) gera arquivos muito extensos e difíceis de editar manualmente. A abordagem simplificada com `system_prompt` e `user_prompt` atende perfeitamente ao desafio de Prompt Engineering.

---

## 3. Tratamento de Erros e Logs

### Decisão de Robustez e Rastreabilidade

Todas as operações críticas de rede e I/O de arquivo devem ser protegidas por blocos `try-except` específicos capturando `Exception` ou erros de conexão específicos do LangSmith, além de reportar mensagens detalhadas usando o módulo `logging`.

### Raciocínio de Robustez e Rastreabilidade

Previne falhas silenciosas e vazamentos de stack traces confusos para o usuário, ao mesmo tempo que mantém a rastreabilidade em produção em conformidade com as Regras da Constituição.

# Data Model: Pull, Otimização e Push de Prompts via LangSmith

Este documento define as entidades de dados e o formato dos prompts utilizados no pipeline.

## 1. Estrutura do Prompt YAML

Tanto os prompts originais (v1) quanto os otimizados (v2) devem seguir uma estrutura consistente definida no YAML:

```yaml
bug_to_user_story_v2:
  description: "Descrição do propósito do prompt."
  system_prompt: |
    [Instruções do sistema, incluindo persona (Role), regras de comportamento, exemplos Few-Shot e lógica de raciocínio (Chain of Thought)]
  user_prompt: |
    [Template de mensagem do usuário, ex: "{bug_report}"]
  version: "v2"
  created_at: "YYYY-MM-DD"
  tags:
    - "bug-analysis"
    - "user-story"
  techniques_applied:
    - "few-shot"
    - "role-prompting"
    - "chain-of-thought"
```

### Regras de Validação de Dados

- `system_prompt`: Obrigatório, string não vazia. Não deve conter marcadores `TODO`.
- `user_prompt`: Obrigatório, contendo a variável de entrada `{bug_report}`.
- `techniques_applied`: Obrigatório, lista de strings com no mínimo 2 elementos.

---

## 2. Entidade de Dataset de Avaliação

A avaliação consome um arquivo em formato JSON Lines (`.jsonl`) localizado em `datasets/bug_to_user_story.jsonl`. Cada linha representa um exemplo no formato:

```json
{
  "inputs": {
    "bug_report": "Descrição do bug reportado pelo usuário."
  },
  "outputs": {
    "reference": "User Story de referência esperada em formato Markdown."
  }
}
```

# Implementation Plan: Pull, Otimização e Push de Prompts via LangSmith

**Branch**: `001-prompt-pipeline` | **Date**: 2026-06-17 | **Spec**: [spec.md](file:///home/bvresende/src/mba-ia-pull-evaluation-prompt/specs/001-prompt-pipeline/spec.md)

**Input**: Feature specification from `specs/001-prompt-pipeline/spec.md`

## Summary

O projeto consiste na implementação de um pipeline completo para pull, otimização local de prompts usando técnicas de Prompt Engineering, validação com testes estruturais pytest, push de volta para o LangSmith Hub e avaliação automática baseada em 5 métricas de qualidade.

A abordagem técnica seguirá as restrições inegociáveis de preservação de código, tratamento robusto de erros e logs estruturados em Python, garantindo que o prompt otimizado v2 alcance notas >= 0.8 em todas as métricas avaliadas.

## Technical Context

**Language/Version**: Python 3.9+

**Primary Dependencies**: `langchain`, `langsmith`, `pytest`, `python-dotenv`, `pyyaml`

**Storage**: Arquivos locais YAML para os prompts (`prompts/`) e JSONL para o dataset (`datasets/`)

**Testing**: pytest

**Target Platform**: Linux runtime / CLI local

**Project Type**: CLI tool e prompt engineering pipeline

**Performance Goals**: Execução síncrona robusta e pontuação >= 0.8 nas 5 métricas de qualidade do LangSmith

**Constraints**: Preservação estrita dos arquivos `src/evaluate.py`, `src/metrics.py`, `src/utils.py`, `datasets/bug_to_user_story.jsonl`. Sem uso de prints genéricos no código final.

**Scale/Scope**: Otimização do prompt `bug_to_user_story` testado contra 15 cenários de bugs

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Princípios Constitucionais Aplicáveis

- **I. Stack Tecnológica de Produção**: Uso obrigatório de Python 3.9+, LangChain (hub), LangSmith (Client) e Pytest.
- **II. Gerenciamento de Prompts em Formato YAML**: Todos os prompts sob `prompts/` em formato YAML.
- **III. Preservação de Infraestrutura e Datasets**: É proibido alterar os arquivos de infraestrutura.
- **IV. Qualidade de Código e Robustez em Produção**: Logs estruturados via `logging`, tratamento de exceções específico e validação estrita do `.env`.
- **V. Cobertura de Testes Estruturais**: Cobertura obrigatória dos 6 testes exigidos no `tests/test_prompts.py`.

*Status: Aprovado. Nenhuma violação detectada.*

## Project Structure

### Documentation (this feature)

```text
specs/001-prompt-pipeline/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
prompts/
├── bug_to_user_story_v1.yml  # Prompt original (LEITURA)
└── bug_to_user_story_v2.yml  # Prompt otimizado (ESCRITA)

src/
├── pull_prompts.py           # Script de pull
├── push_prompts.py           # Script de push
├── evaluate.py               # Script de avaliação (PRESERVADO)
├── metrics.py                # Métricas de avaliação (PRESERVADO)
└── utils.py                  # Auxiliares (PRESERVADO)

tests/
└── test_prompts.py           # Suíte de testes pytest
```

**Structure Decision**: Seguir o padrão de projeto único (Single Project) pré-estabelecido.

## Complexity Tracking

Nenhuma complexidade adicional introduzida.

---

## Arquitetura Técnica Detalhada

### 1. Importações Obrigatórias (LangChain & LangSmith)

- **Em `src/pull_prompts.py`:**
  - `from langchain import hub`: Usado para realizar o pull do prompt original do LangSmith Hub através do método `hub.pull`.
- **Em `src/push_prompts.py`:**
  - `from langchain import hub`: Usado para fazer o push do prompt otimizado ao LangSmith Hub usando `hub.push`.
  - `from langchain_core.prompts import ChatPromptTemplate`: Usado para instanciar a estrutura do prompt a partir dos dados lidos do YAML antes do push.
  - `from langsmith import Client`: Usado para gerenciar e validar o estado dos artefatos no LangSmith se necessário.

### 2. Instanciação e Configuração do Logger (`logging`)

Ambos os scripts devem configurar e usar o logger padrão do Python da seguinte maneira:

```python
import logging

# Configuração básica de logging no escopo global
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("prompt_pipeline")
```

Todas as saídas de depuração e status de fluxo devem utilizar `logger.info()`, `logger.error()`, ou `logger.warning()`. Chamadas a `print()` são estritamente proibidas para mensagens de log no código de produção.

### 3. Estrutura Passo a Passo dos 6 Testes no pytest (`tests/test_prompts.py`)

A classe `TestPrompts` conterá os seguintes testes implementados com `pytest`:

1. **`test_prompt_has_system_prompt`**:
   - Carrega o YAML `prompts/bug_to_user_story_v2.yml` usando o helper `load_prompts`.
   - Obtém os dados sob a chave `bug_to_user_story_v2`.
   - Valida que a chave `system_prompt` existe e seu conteúdo é uma string não vazia.

2. **`test_prompt_has_role_definition`**:
   - Carrega o prompt v2.
   - Varre o texto do `system_prompt` em busca de padrões que definam o papel/persona do agente (e.g., "Você é", "You are", "Product Manager", "Product Owner", "analista").
   - Valida que pelo menos uma definição de papel/persona está presente.

3. **`test_prompt_mentions_format`**:
   - Carrega o prompt v2.
   - Valida que as instruções do prompt exigem que o LLM responda no formato correto (e.g., "Markdown", "User Story", "Como [um]", "Para [que]", "Quero [alguma]").

4. **`test_prompt_has_few_shot_examples`**:
   - Carrega o prompt v2.
   - Analisa o texto do prompt para garantir a presença de exemplos de entrada/saída (Few-shot learning), buscando termos como "Exemplo", "Example", "Input:", "Output:".

5. **`test_prompt_no_todos`**:
   - Carrega o prompt v2.
   - Verifica recursivamente todo o texto das mensagens do prompt (system e user).
   - Valida que a string `TODO` ou `[TODO]` não está presente em nenhum campo.

6. **`test_minimum_techniques`**:
   - Carrega o prompt v2.
   - Lê a lista de técnicas sob a chave de metadados `techniques_applied`.
   - Garante que a lista possui pelo menos 2 técnicas (e.g., `few-shot`, `role-prompting`, `chain-of-thought`).

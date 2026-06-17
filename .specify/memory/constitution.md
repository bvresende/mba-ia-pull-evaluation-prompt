<!--
Sync Impact Report:
- Version change: [CONSTITUTION_VERSION] -> 1.0.0
- List of modified principles:
  * [PRINCIPLE_1_NAME] -> I. Stack Tecnológica de Produção
  * [PRINCIPLE_2_NAME] -> II. Gerenciamento de Prompts em Formato YAML
  * [PRINCIPLE_3_NAME] -> III. Preservação de Infraestrutura e Datasets
  * [PRINCIPLE_4_NAME] -> IV. Qualidade de Código e Robustez em Produção
  * [PRINCIPLE_5_NAME] -> V. Cobertura de Testes Estruturais de Prompts
- Added sections:
  * Restrições de Qualidade e Desempenho
  * Fluxo de Trabalho de Desenvolvimento
- Removed sections:
  * None
- Templates requiring updates:
  * .specify/templates/plan-template.md (✅ verified alignment)
  * .specify/templates/spec-template.md (✅ verified alignment)
  * .specify/templates/tasks-template.md (✅ verified alignment)
- Follow-up TODOs: None
-->

# MBA-IA Pull, Otimização e Avaliação de Prompts Constitution

## Core Principles

### I. Stack Tecnológica de Produção
The project MUST strictly use Python 3.9+, LangChain (via `hub` for pull/push operations), LangSmith (via `Client` and `evaluate` for tracing and evaluation), and Pytest. No other prompt management or evaluation libraries are allowed.
Rationale: Ensures standard production tools and strict compatibility with current project environments.

### II. Gerenciamento de Prompts em Formato YAML
All prompts (both source `v1` and optimized `v2`) MUST be managed strictly as YAML files located within the `prompts/` directory. Direct embedding of prompt template strings inside python source code files is strictly prohibited.
Rationale: Decouples prompt engineering from application code, allowing dynamic updates and clean configuration management.

### III. Preservação de Infraestrutura e Datasets
It is strictly forbidden to modify the files `src/evaluate.py`, `src/metrics.py`, `src/utils.py`, and the evaluation dataset `datasets/bug_to_user_story.jsonl`. All changes must be external to these files.
Rationale: Guarantees evaluation integrity and standard metric comparison across runs.

### IV. Qualidade de Código e Robustez em Produção
All production code MUST implement robust exception handling with specific try/except blocks around external API calls (e.g. LangSmith or LLM calls). The python `logging` module MUST be used for traceability; generic `print` statements are prohibited in the final code. Mandatory strict validation of `.env` configuration keys must occur at the initialization step of `src/pull_prompts.py` and `src/push_prompts.py`.
Rationale: Ensures software reliability, error reporting, and security compliance in a production environment.

### V. Cobertura de Testes Estruturais de Prompts
A pytest suite MUST be implemented in `tests/test_prompts.py` mapping exactly the 6 required prompt structure tests (verifying system prompt, role definition, format instructions, few-shot examples, no TODOs, and minimum techniques in metadata).
Rationale: Prevents deployment of incomplete or malformed prompts that fail to leverage advanced prompt engineering techniques.

## Restrições de Qualidade e Desempenho
All optimized prompts (v2) must reach a minimum score of 0.8 (80%) on all five evaluation metrics (Helpfulness, Correctness, F1-Score, Clarity, Precision) as assessed by LangSmith. The average of all metrics must also be >= 0.8, and no single metric can drop below this threshold.

## Fluxo de Trabalho de Desenvolvimento
1. Executar pull dos prompts ruins do LangSmith usando `src/pull_prompts.py`.
2. Refatorar e otimizar prompts localmente em `prompts/bug_to_user_story_v2.yml` usando Few-shot e técnicas adicionais.
3. Executar a suite de testes estruturais localmente usando `pytest tests/test_prompts.py`.
4. Fazer push do prompt otimizado usando `src/push_prompts.py`.
5. Executar a avaliação usando `src/evaluate.py` no LangSmith.
6. Analisar o tracing, realizar ajustes necessários no prompt v2, e iterar até aprovação.

## Governance
This constitution is the authority for the repository's governance. All pull requests, code reviews, and implementations must comply with the principles.
Amendments require updating the version according to semantic rules:
- MAJOR: Backwards-incompatible governance or principle changes.
- MINOR: New principles or section additions.
- PATCH: Clarifications, typo fixes, or wording enhancements.
The ratification date is the original adoption date.

**Version**: 1.0.0 | **Ratified**: 2026-06-17 | **Last Amended**: 2026-06-17

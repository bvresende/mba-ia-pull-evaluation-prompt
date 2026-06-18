# Tasks: Pull, Otimização e Push de Prompts via LangSmith

**Input**: Design documents from `specs/001-prompt-pipeline/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Testes estruturais do prompt são obrigatórios e devem ser mapeados em `tests/test_prompts.py`.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and environment configuration

- [x] T001 Configure environment variables in `.env` based on `.env.example`
- [x] T002 Install project dependencies from `requirements.txt`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core logging setup and shared utilities readiness

- [x] T003 Setup and verify base logging configuration in `src/pull_prompts.py` and `src/push_prompts.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Obter prompt inicial do repositório remoto (Priority: P1)

**Goal**: Fazer pull do prompt original do LangSmith Hub e salvar localmente.

**Independent Test**: Executar `python src/pull_prompts.py` e verificar a criação do arquivo `prompts/bug_to_user_story_v1.yml`.

### Implementation for User Story 1

- [x] T004 [US1] Implement environment variables check and logging initialization in `src/pull_prompts.py`
- [x] T005 [US1] Implement pull of prompt v1 using langchain's `hub.pull` and save as YAML in `prompts/bug_to_user_story_v1.yml` using helper `save_yaml`

**Checkpoint**: Prompt v1 está salvo localmente e pronto para análise.

---

## Phase 4: User Story 2 - Otimização avançada de prompt local (Priority: P1)

**Goal**: Criar o prompt otimizado v2 aplicando técnicas avançadas.

**Independent Test**: Arquivo `prompts/bug_to_user_story_v2.yml` existe e possui a estrutura requerida.

### Implementation for User Story 2

- [x] T006 [US2] Create and design the optimized prompt YAML in `prompts/bug_to_user_story_v2.yml` applying Few-Shot, Role Prompting, and CoT

**Checkpoint**: Prompt v2 estruturado pronto para passar nos testes unitários.

---

## Phase 5: User Story 3 - Validação estrutural de prompts (Priority: P2)

**Goal**: Implementar a suíte de 6 testes obrigatórios de estrutura.

**Independent Test**: Executar `pytest tests/test_prompts.py` e obter 100% de sucesso.

### Implementation for User Story 3

- [x] T007 [P] [US3] Implement `test_prompt_has_system_prompt` and `test_prompt_has_role_definition` in `tests/test_prompts.py`
- [x] T008 [P] [US3] Implement `test_prompt_mentions_format` and `test_prompt_has_few_shot_examples` in `tests/test_prompts.py`
- [x] T009 [P] [US3] Implement `test_prompt_no_todos` and `test_minimum_techniques` in `tests/test_prompts.py`

**Checkpoint**: Todos os 6 testes unitários passando em verde.

---

## Phase 6: User Story 4 - Publicar prompt otimizado no LangSmith (Priority: P1)

**Goal**: Publicar o prompt v2 com metadados e torná-lo público no LangSmith Hub.

**Independent Test**: Executar `python src/push_prompts.py` e validar publicação no painel do LangSmith.

### Implementation for User Story 4

- [x] T010 [US4] Implement environment variables check and logging initialization in `src/push_prompts.py`
- [x] T011 [US4] Implement YAML parsing, validation using helper `validate_prompt_structure`, and push logic using `hub.push` in `src/push_prompts.py`

**Checkpoint**: Prompt v2 publicado com sucesso no LangSmith.

---

## Phase 7: User Story 5 - Automatic Quality Evaluation (Priority: P1)

**Goal**: Executar avaliação e atingir pontuação mínima >= 0.8 nas 5 métricas.

**Independent Test**: Executar `python src/evaluate.py` e obter aprovação geral.

### Implementation for User Story 5

- [x] T012 [US5] Execute evaluation with `python src/evaluate.py` to calculate metrics against `datasets/bug_to_user_story.jsonl`
- [x] T013 [US5] Perform iterative adjustments on `prompts/bug_to_user_story_v2.yml` and re-evaluate until all 5 metrics are >= 0.8

**Checkpoint**: Avaliação do prompt aprovada com todas as notas individuais >= 0.8.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Documentação final e refinamento do projeto

- [x] T014 Document the applied techniques, comparative results, and instructions in `README.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion.
- **User Stories (Phase 3+)**: All depend on Foundational phase completion.
  - US1 (Phase 3) -> US2 (Phase 4) -> US3 (Phase 5) -> US4 (Phase 6) -> US5 (Phase 7).
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### Parallel Opportunities

- The three testing tasks under US3 (T007, T008, T009) can be implemented in parallel.

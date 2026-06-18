# Feature Specification: Pull, Otimização e Push de Prompts via LangSmith

**Feature Branch**: `001-prompt-pipeline`

**Created**: 2026-06-17

**Status**: Draft

**Input**: User description: "Implementação do fluxo de Pull, Otimização (Prompt Engineering avançado) e Push de prompts via LangSmith"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Obter prompt inicial do repositório remoto (Priority: P1)

O desenvolvedor deseja baixar o prompt de baixa qualidade inicial (`bug_to_user_story_v1`) diretamente do LangSmith Prompt Hub e salvá-lo localmente no formato YAML estruturado.

**Why this priority**: É a etapa inicial indispensável para estabelecer a baseline e iniciar a otimização dos prompts.

**Independent Test**: Executar o comando de pull localmente e validar se o arquivo `prompts/bug_to_user_story_v1.yml` é criado com o conteúdo correto.

**Acceptance Scenarios**:

1. **Given** credenciais válidas configuradas no arquivo `.env`, **When** o comando de pull for executado, **Then** o prompt `leonanluppi/bug_to_user_story_v1` é obtido com sucesso do LangSmith Prompt Hub.
2. **Given** a execução com sucesso, **When** o arquivo local for verificado, **Then** o prompt deve estar salvo na pasta `prompts/` como `bug_to_user_story_v1.yml`.
3. **Given** credenciais inválidas ou ausentes, **When** o comando for executado, **Then** o sistema lança um erro amigável de inicialização e encerra sem criar arquivos corrompidos.

---

### User Story 2 - Otimização avançada de prompt local (Priority: P1)

O engenheiro de prompts deseja otimizar o prompt em um novo arquivo `prompts/bug_to_user_story_v2.yml` usando técnicas avançadas de Prompt Engineering para melhorar a assertividade das respostas do LLM.

**Why this priority**: Garante que o prompt v2 atinja a qualidade mínima exigida para aprovação nos testes de avaliação de produção.

**Independent Test**: Verificar se o arquivo `prompts/bug_to_user_story_v2.yml` possui todas as diretrizes e técnicas especificadas.

**Acceptance Scenarios**:

1. **Given** a estrutura do prompt v2, **When** for verificado o arquivo local, **Then** o prompt deve incluir obrigatoriamente Few-Shot Learning (exemplos práticos de entrada/saída), Role Prompting e Chain of Thought (CoT).
2. **Given** a validação do formato, **When** o arquivo YAML for lido, **Then** as chaves estruturais (como system prompt, role definition, formato, e metadados) devem estar perfeitamente legíveis.

---

### User Story 3 - Validação estrutural de prompts (Priority: P2)

O desenvolvedor deseja rodar testes automatizados locais para certificar-se de que o prompt otimizado segue todos os padrões de qualidade e de metadados obrigatórios antes de realizar o push.

**Why this priority**: Evita que prompts malformados ou incompletos sejam enviados para o LangSmith Hub ou utilizados em produção.

**Independent Test**: Executar `pytest tests/test_prompts.py` e obter 100% de sucesso nos testes estruturais.

**Acceptance Scenarios**:

1. **Given** o prompt v2 otimizado, **When** a suíte de testes for executada, **Then** o arquivo deve passar nos 6 testes obrigatórios: system prompt existente, definição de persona/papel (role definition), instruções explícitas de formato, presença de few-shot, ausência de TODOs e mínimo de 2 técnicas listadas nos metadados.

---

### User Story 4 - Publicar prompt otimizado no LangSmith (Priority: P1)

O desenvolvedor deseja enviar o prompt v2 local devidamente otimizado e testado de volta ao LangSmith Prompt Hub, vinculando as tags das técnicas de prompt utilizadas.

**Why this priority**: Permite versionar o prompt otimizado em produção e disponibilizá-lo para a etapa de avaliação oficial.

**Independent Test**: Executar o script de push e verificar o painel do LangSmith Prompt Hub.

**Acceptance Scenarios**:

1. **Given** o arquivo `prompts/bug_to_user_story_v2.yml` testado e válido, **When** o comando de push for executado, **Then** o prompt deve ser publicado no LangSmith Prompt Hub sob o namespace correspondente (`{seu_username}/bug_to_user_story_v2`).
2. **Given** a publicação concluída, **When** os metadados do prompt forem verificados no LangSmith, **Then** eles devem exibir as tags das técnicas aplicadas.

---

### User Story 5 - Avaliação automática de qualidade (Priority: P1)

O engenheiro de qualidade deseja executar a suite de avaliação no LangSmith para verificar se o prompt otimizado alcança a nota mínima em todas as métricas estabelecidas.

**Why this priority**: É o critério final para homologar e aprovar o prompt para ambiente produtivo.

**Independent Test**: Rodar o script de avaliação e obter status "APROVADO".

**Acceptance Scenarios**:

1. **Given** a execução da avaliação no dataset de 15 bugs, **When** a execução for finalizada, **Then** as 5 métricas (Helpfulness, Correctness, F1-Score, Clarity e Precision) devem atingir notas individuais maiores ou iguais a 0.8 (80%).
2. **Given** as notas obtidas, **When** qualquer nota for menor que 0.8, **Then** o status de aprovação deve ser reprovado ("REPROVADO") com listagem das métricas violadas.

---

### Edge Cases

- **Ausência ou Expiração de Credenciais**: Tentativa de autenticação na API do LangSmith com chaves inválidas ou expiradas na inicialização.
- **Formato YAML Inválido**: O arquivo `bug_to_user_story_v2.yml` corrompido ou mal indentado que impeça a leitura pelo parser de YAML.
- **Bugs Complexos no Dataset**: Exemplos complexos no dataset de avaliação que façam o prompt otimizado falhar na nota mínima de corretude ou clareza (requer prompts altamente robustos).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O script `src/pull_prompts.py` MUST validar as variáveis de ambiente `.env` na inicialização e, em seguida, fazer o download do prompt `leonanluppi/bug_to_user_story_v1` do LangSmith Prompt Hub.
- **FR-002**: O script `src/pull_prompts.py` MUST salvar o prompt obtido em formato YAML estruturado no caminho local `prompts/bug_to_user_story_v1.yml`.
- **FR-003**: O arquivo `prompts/bug_to_user_story_v2.yml` MUST conter em sua estrutura a persona (Role Prompting), exemplos estruturados de entrada/saída (Few-Shot Learning) e raciocínio lógico estruturado (Chain of Thought).
- **FR-004**: O arquivo `tests/test_prompts.py` MUST conter exatamente os 6 testes obrigatórios de estrutura de prompt definidos:
  - `test_prompt_has_system_prompt`
  - `test_prompt_has_role_definition`
  - `test_prompt_mentions_format`
  - `test_prompt_has_few_shot_examples`
  - `test_prompt_no_todos`
  - `test_minimum_techniques`
- **FR-005**: O script `src/push_prompts.py` MUST validar as chaves do `.env` na inicialização, carregar o arquivo local `prompts/bug_to_user_story_v2.yml` e fazer o push para o LangSmith no formato `{seu_username}/bug_to_user_story_v2`.
- **FR-006**: O script `src/push_prompts.py` MUST anexar tags das técnicas aplicadas nos metadados do prompt enviado.
- **FR-007**: Todo o código implementado MUST tratar chamadas de APIs externas com blocos de tratamento de exceção (`try-except`) robustos e específicos.
- **FR-008**: O código MUST usar exclusivamente o módulo `logging` para rastreamento de fluxo de execução, proibindo o uso de prints genéricos para logs finais de produção.

### Key Entities

- **Prompt**: Estrutura YAML que encapsula as mensagens (System/User), metadados e tags de técnicas de prompt engineering.
- **Dataset**: Arquivo local JSON Lines (`datasets/bug_to_user_story.jsonl`) contendo os 15 casos de bugs para avaliação.
- **Evaluation Run**: Execução de teste do prompt otimizado frente ao dataset, gerando scores para 5 métricas de qualidade.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: O prompt otimizado atinge pontuação >= 0.8 (80%) para as métricas de Helpfulness, Correctness, F1-Score, Clarity e Precision no LangSmith.
- **SC-002**: A execução de `pytest tests/test_prompts.py` passa 100% dos 6 testes locais sem falhas.
- **SC-003**: A inicialização dos scripts interrompe imediatamente a execução em menos de 1 segundo caso as chaves necessárias no `.env` não sejam válidas.
- **SC-004**: O pipeline completo de pull, teste, push e avaliação roda com sucesso sem interrupções manuais ou erros não tratados.

## Assumptions

- Presume-se que o usuário possua uma conta ativa no LangSmith e as chaves de API necessárias (OpenAI/Gemini e LangSmith) para autenticação.
- O dataset `datasets/bug_to_user_story.jsonl` está completo e não sofreu alterações.
- O formato do LangSmith Prompt Hub é compatível com o parser YAML utilizado na leitura do arquivo local.

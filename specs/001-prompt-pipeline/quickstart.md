# Quickstart Guide: Pull, Otimização e Push de Prompts via LangSmith

Este guia descreve as etapas para executar, testar e avaliar a feature de otimização de prompts.

## Pré-requisitos

Certifique-se de configurar as variáveis de ambiente necessárias no arquivo `.env` baseado no `.env.example`:

```bash
LANGSMITH_API_KEY=sua_chave_langsmith
USERNAME_LANGSMITH_HUB=seu_username_langsmith
OPENAI_API_KEY=sua_chave_openai (se usar openai)
GOOGLE_API_KEY=sua_chave_gemini (se usar google)
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Passos para Execução

### 1. Fazer Pull do Prompt Original (v1)

Faça o download do prompt inicial para o ambiente local:

```bash
python src/pull_prompts.py
```

*Resultado esperado*: Criação do arquivo `prompts/bug_to_user_story_v1.yml`.

### 2. Otimizar o Prompt Localmente

Edite o arquivo `prompts/bug_to_user_story_v2.yml` (seja criando a partir do v1 ou do zero) aplicando as técnicas obrigatórias:

- Role Prompting
- Few-Shot Learning (com 2 a 3 exemplos)
- Chain of Thought (CoT)

### 3. Executar os Testes de Estrutura

Verifique localmente a conformidade dos prompts:

```bash
pytest tests/test_prompts.py
```

*Resultado esperado*: Todos os 6 testes devem passar (Green).

### 4. Fazer Push do Prompt Otimizado (v2)

Publique o prompt no LangSmith Prompt Hub:

```bash
python src/push_prompts.py
```

*Resultado esperado*: Prompt publicado no hub em `{seu_username}/bug_to_user_story_v2` e definido como público.

### 5. Executar Avaliação e Obter Métricas

Execute a avaliação automática contra o dataset de teste:

```bash
python src/evaluate.py
```

*Resultado esperado*: Status final `APROVADO` com todas as 5 métricas atingindo nota >= 0.8.

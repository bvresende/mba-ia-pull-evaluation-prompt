"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
import logging
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("push_prompts")

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    logger.info(f"Preparando push para o prompt '{prompt_name}'...")
    try:
        system_prompt = prompt_data.get("system_prompt", "")
        user_prompt = prompt_data.get("user_prompt", "")
        
        # Constrói o ChatPromptTemplate
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])
        
        # Faz o push público ao hub
        logger.info(f"Enviando '{prompt_name}' ao LangSmith Prompt Hub...")
        hub.push(prompt_name, prompt_template, new_repo_is_public=True)
        logger.info(f"Prompt '{prompt_name}' publicado com sucesso no Hub.")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao fazer push do prompt '{prompt_name}' para o LangSmith Hub: {e}", exc_info=True)
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    return validate_prompt_structure(prompt_data)


def main():
    """Função principal"""
    print_section_header("PUSH PROMPTS TO LANGSMITH HUB")
    
    # Validação estrita das credenciais no .env
    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        logger.error("Credenciais obrigatórias ausentes no arquivo .env.")
        return 1
        
    username = os.getenv("USERNAME_LANGSMITH_HUB")
    file_path = "prompts/bug_to_user_story_v2.yml"
    
    logger.info(f"Carregando arquivo de prompts local: {file_path}")
    data = load_yaml(file_path)
    if not data:
        logger.error(f"Não foi possível carregar o arquivo YAML local: {file_path}")
        return 1
        
    prompt_key = "bug_to_user_story_v2"
    if prompt_key not in data:
        logger.error(f"Chave '{prompt_key}' não encontrada no arquivo {file_path}")
        return 1
        
    prompt_data = data[prompt_key]
    
    # Validação estrutural do prompt
    logger.info("Validando a estrutura do prompt v2...")
    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        logger.error("Falha na validação do prompt:")
        for err in errors:
            logger.error(f"  - {err}")
        return 1
    logger.info("Prompt v2 validado com sucesso.")
    
    # Executa o push
    hub_prompt_name = f"{username}/{prompt_key}"
    success = push_prompt_to_langsmith(hub_prompt_name, prompt_data)
    
    if success:
        logger.info("Processo de push concluído com sucesso.")
        return 0
    else:
        logger.error("Processo de push finalizado com erro.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("pull_prompts")

load_dotenv()


def pull_prompts_from_langsmith() -> bool:
    """
    Faz pull do prompt do LangSmith Hub e salva localmente como YAML.
    """
    logger.info("Iniciando pull do prompt 'leonanluppi/bug_to_user_story_v1'...")
    try:
        # Pull do prompt
        prompt = hub.pull("leonanluppi/bug_to_user_story_v1")
        logger.info("Prompt obtido com sucesso do LangSmith Hub.")
        
        system_prompt = ""
        user_prompt = ""
        
        # Extrai o conteúdo do prompt
        if hasattr(prompt, "messages"):
            for msg in prompt.messages:
                role = getattr(msg, "role", None)
                if not role:
                    cls_name = msg.__class__.__name__
                    if "System" in cls_name:
                        role = "system"
                    elif "Human" in cls_name:
                        role = "human"
                
                content = ""
                if hasattr(msg, "prompt") and hasattr(msg.prompt, "template"):
                    content = msg.prompt.template
                elif hasattr(msg, "content"):
                    content = msg.content
                
                if role == "system":
                    system_prompt = content
                elif role in ["human", "user"]:
                    user_prompt = content
        else:
            if hasattr(prompt, "template"):
                system_prompt = prompt.template
            user_prompt = "{bug_report}"
            
        logger.info("Conteúdo do prompt extraído com sucesso.")
        
        # Estrutura final do arquivo YAML
        prompt_data = {
            "bug_to_user_story_v1": {
                "description": "Prompt para converter relatos de bugs em User Stories",
                "system_prompt": system_prompt,
                "user_prompt": user_prompt,
                "version": "v1",
                "created_at": "2025-01-15",
                "tags": ["bug-analysis", "user-story", "product-management"]
            }
        }
        
        file_path = "prompts/bug_to_user_story_v1.yml"
        if save_yaml(prompt_data, file_path):
            logger.info(f"Prompt salvo com sucesso em {file_path}")
            return True
        else:
            logger.error(f"Falha ao salvar o prompt em {file_path}")
            return False
            
    except Exception as e:
        logger.error(f"Erro ao obter prompt do LangSmith Hub: {e}", exc_info=True)
        return False


def main():
    """Função principal"""
    print_section_header("PULL PROMPTS FROM LANGSMITH HUB")
    
    # Validação estrita das credenciais no .env
    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        logger.error("Credenciais obrigatórias ausentes no arquivo .env.")
        return 1
        
    success = pull_prompts_from_langsmith()
    if success:
        logger.info("Processo de pull concluído com sucesso.")
        return 0
    else:
        logger.error("Processo de pull finalizado com erro.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

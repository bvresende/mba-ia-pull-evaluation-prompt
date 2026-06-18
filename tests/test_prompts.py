"""
Testes automatizados para validação de prompts.
"""
# pyrefly: ignore [missing-import]
import pytest
import yaml
import sys
import os
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# pyrefly: ignore [missing-import]
from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    @property
    def prompt_v2(self):
        """Retorna o prompt v2 carregado."""
        file_path = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
        data = load_prompts(str(file_path))
        return data["bug_to_user_story_v2"]

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompt = self.prompt_v2
        assert "system_prompt" in prompt, "O campo 'system_prompt' deve existir no YAML do prompt v2."
        assert isinstance(prompt["system_prompt"], str), "O 'system_prompt' deve ser uma string."
        assert len(prompt["system_prompt"].strip()) > 0, "O 'system_prompt' não deve estar vazio."

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = self.prompt_v2.get("system_prompt", "")
        keywords = ["Product Manager", "Analista de Negócios", "Product Owner", "Você é", "Persona"]
        found = any(keyword.lower() in system_prompt.lower() for keyword in keywords)
        assert found, "O system_prompt deve definir uma persona/role clara para o agente de IA."

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = self.prompt_v2.get("system_prompt", "")
        keywords = ["Como um", "Eu quero", "Para que", "Given-When-Then", "Dado-Quando-Então", "Critérios de Aceitação"]
        found = any(keyword.lower() in system_prompt.lower() for keyword in keywords)
        assert found, "O prompt deve mencionar as regras de formatação (User Story / Critérios de Aceitação / Given-When-Then)."

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = self.prompt_v2.get("system_prompt", "")
        keywords = ["exemplo", "example", "few-shot", "input", "output", "entrada", "saída"]
        found = any(keyword.lower() in system_prompt.lower() for keyword in keywords)
        assert found, "O prompt deve incluir exemplos práticos de Few-shot learning para guiar a geração."

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompt = self.prompt_v2
        system_prompt = prompt.get("system_prompt", "")
        user_prompt = prompt.get("user_prompt", "")
        
        # Evita falso positivo com "metodologia" e "método"
        system_prompt_clean = system_prompt.lower().replace("metodologia", "").replace("metodo", "").replace("método", "")
        user_prompt_clean = user_prompt.lower().replace("metodologia", "").replace("metodo", "").replace("método", "")
        
        assert "todo" not in system_prompt_clean, "O system_prompt não deve conter marcadores TODO."
        assert "todo" not in user_prompt_clean, "O user_prompt não deve conter marcadores TODO."

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = self.prompt_v2.get("techniques_applied", [])
        assert isinstance(techniques, list), "O campo 'techniques_applied' deve ser uma lista de strings."
        assert len(techniques) >= 2, f"Devem ser aplicadas pelo menos 2 técnicas avançadas. Encontradas: {len(techniques)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
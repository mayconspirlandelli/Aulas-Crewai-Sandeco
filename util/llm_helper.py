# llm_helper.py

import os
from dotenv import load_dotenv
from crewai import LLM

class LLMHelper:
    @staticmethod
    def get_llm(
        model_name="gemini/gemini-2.0-flash",
        temperature=0.0,
        env_var_key="GOOGLE_API_KEY"
    ):
        """Retorna uma instância configurada do LLM."""
        load_dotenv()

        api_key = os.getenv(env_var_key)
        if not api_key:
            raise ValueError(f"Chave '{env_var_key}' não encontrada no .env")

        return LLM(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )

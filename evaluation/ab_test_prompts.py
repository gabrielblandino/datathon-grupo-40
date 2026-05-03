"""
Script para A/B testing de Prompts do Sistema (Champion/Challenger).
"""
import logging
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

PROMPT_A = "Você é um atendente bancário. Responda à pergunta: {query}"
PROMPT_B = "Você é um analista de crédito sênior. Responda à pergunta detalhadamente: {query}"

def compare_prompts(query: str):
    """Compara as respostas de duas versões de prompt diferentes."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    
    logger.info("Testando Prompt A (Champion)...")
    res_a = llm.invoke(PROMPT_A.format(query=query)).content
    
    logger.info("Testando Prompt B (Challenger)...")
    res_b = llm.invoke(PROMPT_B.format(query=query)).content
    
    print("\n--- RESULTADO PROMPT A ---")
    print(res_a)
    print("\n--- RESULTADO PROMPT B ---")
    print(res_b)

if __name__ == "__main__":
    compare_prompts("Qual a taxa média de juros para um empréstimo grau B?")
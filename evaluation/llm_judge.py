"""
Avaliação LLM-as-a-judge usando 3 critérios (Relevância, Clareza, Regras de Negócio).
Corrigido para limpeza de JSON e caminhos da pasta BUILD.
"""
import os
import logging
import json
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Carrega a OPENAI_API_KEY do arquivo .env
load_dotenv()

logger = logging.getLogger(__name__)

JUDGE_PROMPT = PromptTemplate.from_template("""
Você é um auditor financeiro sênior avaliando respostas geradas por um assistente de IA.
Avalie a seguinte interação com base em 3 critérios, dando uma nota de 1 a 5 para cada:

1. Clareza: A resposta é fácil de entender para o cliente final?
2. Aderência ao Negócio: A resposta respeita diretrizes de crédito (DTI, Renda Mínima, Histórico)?
3. Relevância: A resposta responde diretamente ao que foi perguntado?

Pergunta do usuário: {query}
Resposta do Assistente: {response}

Retorne APENAS um formato JSON válido com as chaves: "clareza", "aderencia", "relevancia".
""")

def clean_json_response(raw_content: str) -> str:
    """Remove blocos de código markdown (```json) se existirem."""
    return re.sub(r'```json|```', '', raw_content).strip()

def evaluate_with_judge(query: str, response: str) -> dict:
    """Usa o GPT-4o-mini como juiz da qualidade das respostas."""
    try:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
        chain = JUDGE_PROMPT | llm
        
        resultado = chain.invoke({"query": query, "response": response})
        
        # Limpa e carrega o JSON com segurança
        clean_content = clean_json_response(resultado.content)
        notas = json.loads(clean_content)
        
        print("\n--- AVALIAÇÃO DO JUIZ (IA) ---")
        print(json.dumps(notas, indent=4, ensure_ascii=False))
        
        # Salva o log na pasta build/results conforme a arquitetura
        log_dir = os.path.join("build", "results")
        os.makedirs(log_dir, exist_ok=True)
        with open(os.path.join(log_dir, "judge_logs.json"), "a", encoding="utf-8") as f:
            log_entry = {"query": query, "response": response, "scores": notas}
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
            
        return notas
    except Exception as e:
        logger.error(f"Erro na avaliação do juiz: {e}")
        return {}

if __name__ == "__main__":
    pergunta = "Por que meu empréstimo foi negado?"
    resposta_ia = "Seu empréstimo foi negado pois o DTI está em 45%, o que viola a política da classe C (máximo 40%)."
    evaluate_with_judge(pergunta, resposta_ia)
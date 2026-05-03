import os
import json
from dotenv import load_dotenv
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    context_precision,
    context_recall,
    faithfulness,
)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Carrega chaves
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def mock_rag_pipeline(query: str):
    """Simula o retorno do sistema RAG real."""
    return "A política de crédito aceita DTI até 40%.", ["Manual de Crédito Versão 1.0: DTI máximo de 40%."]

def evaluate_rag_pipeline(golden_set_path: str):
    # Garante que o script leia do diretório build correto
    if not os.path.exists(golden_set_path):
        print(f"ERRO: Golden Set não encontrado em {golden_set_path}.")
        return

    with open(golden_set_path, "r", encoding="utf-8") as f:
        golden_set = json.load(f)

    data = {"question": [], "answer": [], "contexts": [], "ground_truth": []}

    for item in golden_set:
        ans, ctx = mock_rag_pipeline(item["query"])
        data["question"].append(item["query"])
        data["answer"].append(ans)
        data["contexts"].append(ctx)
        data["ground_truth"].append(item["expected_answer"])

    dataset = Dataset.from_dict(data)

    result = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        llm=llm,
        embeddings=embeddings
    )

    result_dict = {
        "faithfulness": result["faithfulness"],
        "answer_relevancy": result["answer_relevancy"],
        "context_precision": result["context_precision"],
        "context_recall": result["context_recall"]
    }

    print("\n--- RESULTADOS RAGAS (Custo Mínimo) ---")
    print(json.dumps(result_dict, indent=4))
    
    os.makedirs("evaluation/results", exist_ok=True)
    with open("evaluation/results/ragas_metrics.json", "w") as f:
        json.dump(result_dict, f, indent=4)

if __name__ == "__main__":
    # Caminho ajustado para a pasta BUILD conforme sua estrutura
    path = os.path.join("build", "data", "golden_set", "credit_qa.json")
    evaluate_rag_pipeline(path)
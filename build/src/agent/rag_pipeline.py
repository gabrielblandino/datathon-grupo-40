"""Pipeline RAG: Embedding + Retriever + Generator."""
import logging
from typing import Tuple, List
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

logger = logging.getLogger(__name__)

def build_retriever(data_path: str):
    """
    Constrói a base vetorial a partir dos documentos de contexto.
    Args:
        data_path: Caminho para os arquivos de política ou base de dados.
    """
    try:
        logger.info(f"Carregando documentos de {data_path} para o VectorStore...")
        # Nota: Em produção, substituir por um carregamento fatiado (RecursiveCharacterTextSplitter)
        loader = TextLoader(data_path, encoding='utf-8')
        docs = loader.load()
        
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(docs, embeddings)
        logger.info("VectorStore inicializado com sucesso.")
        
        return vectorstore.as_retriever(search_kwargs={"k": 3})
    except Exception as e:
        logger.error(f"Erro na construção do retriever RAG: {e}")
        raise

def mock_rag_fn(query: str) -> Tuple[str, List[str]]:
    """
    Função wrapper para injeção na avaliação RAGAS (Etapa 3).
    Args:
        query: Pergunta do usuário.
    Returns:
        Tupla contendo a (resposta, contextos_recuperados).
    """
    # Implementação padrão simulada para integração imediata
    return ("Resposta gerada pelo RAG", ["Contexto 1 do banco", "Contexto 2 do documento"])
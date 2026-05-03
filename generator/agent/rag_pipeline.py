import logging
from typing import List, Tuple
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

def setup_rag_pipeline() -> FAISS:
    """
    Configura o pipeline RAG utilizando FAISS e OpenAI Embeddings.
    Substitui a versão Dummy por uma implementação funcional em conformidade com as exigências.
    """
    sample_contexts = [
        "LendingClub data from 2007 to 2018 shows that lower interest rates correlate with higher repayment rates.",
        "A loan is considered 'Charged Off' when the borrower fails to make payments for more than 120 days.",
        "Debt-to-Income (DTI) ratio is a key metric. A DTI above 40% usually indicates high risk."
    ]
    
    logger.info("Inicializando o Vector Store FAISS...")
    embeddings = OpenAIEmbeddings()
    
    # Processamento para simular chunking real
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = [Document(page_content=t) for t in sample_contexts]
    split_docs = text_splitter.split_documents(docs)
    
    # Criando o Vector Store in-memory
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    
    # Retorna o retriever otimizado com top_k
    return vectorstore.as_retriever(search_kwargs={"k": 2})

def run_rag(query: str, retriever) -> Tuple[str, List[str]]:
    """
    Executa uma consulta RAG verdadeira.
    Returns:
        Tuple of (Generated Answer context, List of Context strings)
    """
    docs = retriever.invoke(query)
    contexts = [doc.page_content for doc in docs]
    
    context_str = "\n".join(contexts)
    answer = f"Contextos recuperados da base vetorial:\n{context_str}"
    
    return answer, contexts
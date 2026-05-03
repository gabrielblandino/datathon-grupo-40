"""Agente ReAct com tools customizadas para o domínio do Datathon[cite: 1].
Referência: Yao et al. (2023) — ReAct: Synergizing Reasoning and Acting
in Language Models. https://arxiv.org/abs/2210.03629
"""
import logging
from typing import List
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import Tool

logger = logging.getLogger(__name__)

# Template do Prompt devidamente formatado para parsing ReAct seguro
REACT_PROMPT = PromptTemplate.from_template("""Você é um assistente especializado em análise de crédito corporativo.
Use as ferramentas disponíveis para responder as perguntas de negócio e extrair dados da base de dados.

Ferramentas disponíveis:
{tools}

Use extritamente o seguinte formato de raciocínio passo a passo:

Thought: pensar sobre o que fazer
Action: nome_da_ferramenta
Action Input: input para a ferramenta
Observation: resultado da ferramenta
Thought: Avaliarei se a observação responde a pergunta. (repita Thought/Action/Observation quantas vezes necessário)
Thought: Agora sei a resposta final
Final Answer: a resposta detalhada e justificada para o usuário

Pergunta: {input}
{agent_scratchpad}""")

def create_datathon_agent(
    tools: List[Tool],
    model_name: str = "gpt-4o-mini",
    temperature: float = 0.0,
) -> AgentExecutor:
    """Cria agente ReAct para o Datathon assegurando uso de múltiplas tools.
    
    Args:
        tools: Lista de ferramentas customizadas (mínimo de 3 exigido pela banca).
        model_name: Identificador do modelo LLM a utilizar.
        temperature: Temperatura de geração (0.0 para determinismo analítico).
        
    Returns:
        AgentExecutor configurado e acoplado ao LLM.
    """
    if len(tools) < 3:
        logger.warning("Datathon exige ≥ 3 tools. Fornecidas: %d. A pontuação pode ser penalizada.", len(tools))
        
    llm = ChatOpenAI(model=model_name, temperature=temperature)
    agent = create_react_agent(llm=llm, tools=tools, prompt=REACT_PROMPT)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True,
    )
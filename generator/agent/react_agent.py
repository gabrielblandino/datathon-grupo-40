import logging

# Importação corrigida para versões modernas do LangChain:
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from generator.agent.tools import get_all_tools

logger = logging.getLogger(__name__)

REACT_PROMPT = PromptTemplate.from_template("""Você é um assistente especializado do Datathon - Fase 05.
Use as ferramentas disponíveis para responder perguntas e calcular métricas financeiras.

Ferramentas disponíveis:
{tools}

Use o formato obrigatório abaixo:
Thought: pensar sobre o que fazer e se preciso de uma ferramenta.
Action: nome_da_ferramenta_escolhida (deve ser estritamente uma destas: {tool_names})
Action Input: input para a ferramenta
Observation: o resultado retornado pela ferramenta
... (repita Thought/Action/Observation quantas vezes necessário)
Thought: Agora sei a resposta final
Final Answer: a resposta detalhada para o usuário

Pergunta: {input}
{agent_scratchpad}""")

def create_datathon_agent(model_name: str = "gpt-4o-mini", temperature: float = 0.0) -> AgentExecutor:
    """Cria e configura o agente ReAct integrado com as ferramentas de domínio."""
    tools = get_all_tools()
    
    if len(tools) < 3:
        logger.warning(f"O Datathon exige >= 3 tools. Você forneceu: {len(tools)}.")
        
    llm = ChatOpenAI(model=model_name, temperature=temperature)
    agent = create_react_agent(llm=llm, tools=tools, prompt=REACT_PROMPT)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True,
    )
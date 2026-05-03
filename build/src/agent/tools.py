"""Ferramentas customizadas para o Agente ReAct (Etapa 2)."""
import logging
from typing import Dict, Any
from langchain.tools import tool

logger = logging.getLogger(__name__)

@tool
def calcular_dti(renda_anual: float, divida_total: float) -> float:
    """
    Calcula o Debt-to-Income (DTI) ratio do cliente.
    Útil quando é necessário saber o comprometimento da renda do usuário.
    Args:
        renda_anual: Renda anual bruta do cliente.
        divida_total: Total de dívidas anuais ativas.
    Returns:
        O valor percentual do DTI.
    """
    try:
        if renda_anual <= 0:
            return 0.0
        dti = (divida_total / renda_anual) * 100
        logger.info(f"DTI calculado: {dti:.2f}%")
        return round(dti, 2)
    except Exception as e:
        logger.error(f"Erro ao calcular DTI: {e}")
        return 0.0

@tool
def consultar_politica_credito(zip_code: str) -> str:
    """
    Consulta regras específicas de concessão de crédito por região (Zip Code).
    Args:
        zip_code: O código postal da região (ex: '190xx').
    Returns:
        Regra de negócio aplicada à região.
    """
    # Mock de banco de dados regional
    regras = {
        "190xx": "Região PA: Limite máximo aprovado de $35,000. Risco moderado.",
        "481xx": "Região NM: Exigência de DTI menor que 15%. Risco elevado."
    }
    regra = regras.get(zip_code, "Região Padrão: Aplicar política de crédito geral.")
    logger.info(f"Política consultada para o Zip: {zip_code}")
    return regra

@tool
def buscar_dados_cliente(member_id: str) -> Dict[str, Any]:
    """
    Busca o histórico de dados do cliente na base relacional.
    Args:
        member_id: ID único do membro/cliente.
    Returns:
        Dicionário com o score de risco e status de verificação.
    """
    # Mock simulando extração de dados
    logger.info(f"Buscando dados do cliente {member_id}")
    return {
        "member_id": member_id,
        "verification_status": "Verified",
        "delinq_2yrs": 0,
        "fico_range_low": 675.0,
        "fico_range_high": 679.0
    }
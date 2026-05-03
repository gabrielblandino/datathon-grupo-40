"""Testes do agente ReAct e Tools."""
from generator.agent.tools import calculate_dti, search_loan_policy, get_average_interest_rate

def test_calculate_dti_valid():
    """Testa o cálculo do DTI com valores válidos."""
    # 25000 de dívida para 100000 de renda = 25%
    resultado = calculate_dti.invoke({"monthly_debt": 25000.0, "monthly_income": 100000.0})
    assert resultado == "The calculated DTI is 25.00%."

def test_calculate_dti_zero_income():
    """Testa a robustez da tool contra divisão por zero ou valores negativos."""
    resultado = calculate_dti.invoke({"monthly_debt": 10000.0, "monthly_income": 0.0})
    assert "Error: Monthly income must be greater than zero" in resultado

def test_search_loan_policy():
    """Testa a ferramenta de busca de política de crédito do Agente."""
    # Testa uma política existente
    resultado_dti = search_loan_policy.invoke({"query": "dti"})
    assert "Maximum allowed DTI" in resultado_dti
    
    # Testa uma política inexistente (fallback)
    resultado_vazio = search_loan_policy.invoke({"query": "palavra_aleatoria_inexistente"})
    assert "No specific policy found" in resultado_vazio

def test_get_average_interest_rate():
    """Testa a ferramenta de consulta de taxa de juros do Agente."""
    # Testa um grau válido (A)
    resultado_a = get_average_interest_rate.invoke({"grade": "A"})
    assert "7.5%" in resultado_a
    
    # Testa sensibilidade a letras minúsculas (b -> B)
    resultado_b = get_average_interest_rate.invoke({"grade": "b"})
    assert "11.2%" in resultado_b
    
    # Testa grau inválido
    resultado_invalido = get_average_interest_rate.invoke({"grade": "Z"})
    assert "Unknown grade" in resultado_invalido
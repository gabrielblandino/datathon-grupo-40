from langchain.tools import tool
import pandas as pd
import logging

logger = logging.getLogger(__name__)

@tool
def calculate_dti(monthly_debt: float, monthly_income: float) -> str:
    """
    Calculates the Debt-to-Income (DTI) ratio.
    Args:
        monthly_debt: Total monthly debt payments.
        monthly_income: Gross monthly income.
    Returns:
        String with the DTI percentage or an error message.
    """
    try:
        if monthly_income <= 0:
            return "Error: Monthly income must be greater than zero."
        dti = (monthly_debt / monthly_income) * 100
        return f"The calculated DTI is {dti:.2f}%."
    except Exception as e:
        logger.error(f"Error calculating DTI: {e}")
        return f"Error calculating DTI: {e}"

@tool
def search_loan_policy(query: str) -> str:
    """
    Searches the internal loan policy document for guidelines.
    Args:
        query: Keyword or question about loan policies.
    Returns:
        Relevant policy excerpt.
    """
    policies = {
        "dti": "Maximum allowed DTI for grade A is 35%. For grade B and C, it is 40%.",
        "income": "Minimum annual income required is $30,000.",
        "default": "Applicants with a history of default within the last 2 years are automatically rejected."
    }
    query_lower = query.lower()
    for key, policy in policies.items():
        if key in query_lower:
            return policy
    return "No specific policy found for the given query. Please consult the underwriter manual."

@tool
def get_average_interest_rate(grade: str) -> str:
    """
    Gets the historical average interest rate for a given loan grade (A-G).
    Args:
        grade: Loan grade letter (e.g., A, B, C).
    Returns:
        Average interest rate percentage.
    """
    grade = grade.upper().strip()
    avg_rates = {
        "A": "7.5%", "B": "11.2%", "C": "14.5%", 
        "D": "18.0%", "E": "21.5%", "F": "25.0%", "G": "28.0%"
    }
    return avg_rates.get(grade, "Unknown grade. Valid grades are A, B, C, D, E, F, G.")

def get_all_tools():
    return [calculate_dti, search_loan_policy, get_average_interest_rate]
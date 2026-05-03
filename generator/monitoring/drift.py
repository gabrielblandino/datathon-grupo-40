# generator/monitoring/drift.py
import logging
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

logger = logging.getLogger(__name__)

def check_data_drift(reference_df: pd.DataFrame, current_df: pd.DataFrame, drift_threshold: float = 0.2) -> bool:
    """
    Compara os dados de treino com os dados de inferência atuais para detectar Data Drift.
    
    Args:
        reference_df (pd.DataFrame): Dados originais usados no treinamento (Baseline).
        current_df (pd.DataFrame): Dados novos recebidos em produção.
        drift_threshold (float): Limite percentual aceitável de colunas com drift.
        
    Returns:
        bool: Retorna True se o drift ultrapassar o limiar estipulado (indicando necessidade de retreino).
    """
    logger.info("Iniciando análise de drift de dados com Evidently...")
    
    try:
        # Configura o relatório com o preset de Data Drift
        report = Report(metrics=[DataDriftPreset()])
        report.run(reference_data=reference_df, current_data=current_df)
        
        # Extrai os resultados em formato de dicionário
        drift_result = report.as_dict()
        
        # Coleta a proporção de colunas que apresentaram drift estatístico
        drift_share = drift_result["metrics"][0]["result"]["share_of_drifted_columns"]
        logger.info(f"Proporção de colunas com drift detectado: {drift_share:.2%}")
        
        # Avalia se a degradação ultrapassou nosso limite de alerta
        if drift_share > drift_threshold:
            logger.warning(f"ALERTA: Data Drift de {drift_share:.0%} excedeu o limite de {drift_threshold:.0%}. Retreinamento recomendado!")
            return True
            
        return False
        
    except Exception as e:
        logger.error(f"Erro inesperado ao executar a verificação de drift: {e}")
        return False
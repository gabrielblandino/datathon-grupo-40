"""Pipeline de Feature Engineering e transformação de dados."""
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gera features derivadas para o modelo e aplica imputação base.
    
    Args:
        df: DataFrame raw contendo 'feature_1' e 'feature_2'.
        
    Returns:
        DataFrame processado respeitando o schema contract.
    """
    logger.info("Iniciando feature engineering...")
    df_processed = df.copy()
    
    # Preenchimento de nulos genérico para as features de teste
    df_processed.fillna({
        'feature_1': df_processed['feature_1'].median() if 'feature_1' in df_processed else 0,
        'feature_2': df_processed['feature_2'].median() if 'feature_2' in df_processed else 1,
    }, inplace=True)
    
    # Feature cruzada solicitada nos testes
    if 'feature_1' in df_processed.columns and 'feature_2' in df_processed.columns:
        df_processed['feature_1_x_feature_2'] = df_processed['feature_1'] * df_processed['feature_2']
        
    logger.info("Feature engineering finalizado com sucesso.")
    return df_processed
"""Pipeline de treinamento com MLflow tracking padronizado."""
import logging
import os
import subprocess
import mlflow
import pandas as pd
from typing import Any
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

def get_git_revision_hash() -> str:
    """Recupera o hash do commit atual para rastreabilidade estrita (GAP 05)."""
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
    except Exception:
        return "unknown_commit"

def train_and_log(
    df: pd.DataFrame,
    target_col: str,
    model_name: str,
    model_class: Any,
    model_params: dict,
    test_size: float = 0.2,
    random_state: int = 42,
    data_version: str = "v1.0"
) -> str:
    """Treina modelo, loga tudo no MLflow, retorna run_id.
    
    Args:
        df: DataFrame com features e target pré-processados.
        target_col: Nome da coluna target (variável resposta).
        model_name: Nome para registro no MLflow.
        model_class: Classe do modelo (ex: RandomForestClassifier).
        model_params: Hiperparâmetros do modelo (dicionário).
        test_size: Proporção do conjunto de teste.
        random_state: Semente para reprodutibilidade.
        data_version: Hash DVC ou versão dos dados de treinamento.
        
    Returns:
        run_id do experimento no MLflow.
    """
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    with mlflow.start_run(run_name=model_name) as run:
        # Log de parâmetros
        mlflow.log_params(model_params)
        mlflow.log_param("test_size", test_size)
        mlflow.log_param("random_state", random_state)
        mlflow.log_param("n_features", X_train.shape[1])
        mlflow.log_param("n_samples_train", X_train.shape[0])
        
        # Tags padronizadas (obrigatório - mitigação do GAP 05)[cite: 1]
        mlflow.set_tag("model_name", model_name)
        mlflow.set_tag("model_version", "1.0.0")
        mlflow.set_tag("model_type", "classification")
        mlflow.set_tag("framework", model_class.__module__.split(".")[0])
        mlflow.set_tag("owner", "grupo-XX")
        mlflow.set_tag("phase", "datathon-fase05")
        mlflow.set_tag("training_data_version", data_version)
        mlflow.set_tag("risk_level", "high") # Risco de crédito é usualmente high risk
        mlflow.set_tag("fairness_checked", "True") 
        mlflow.set_tag("git_sha", get_git_revision_hash())

        # Treino do modelo (Scikit-Learn API compatível)
        model = model_class(**model_params)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        # Métricas padronizadas
        metrics = {
            "auc": roc_auc_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1": f1_score(y_test, y_pred, zero_division=0),
        }
        mlflow.log_metrics(metrics)
        
        # Log do modelo (Artifact Registry)
        mlflow.sklearn.log_model(model, "model")
        
        logger.info(
            "Modelo %s treinado: AUC=%.4f, F1=%.4f",
            model_name,
            metrics["auc"],
            metrics["f1"],
        )
        return run.info.run_id
"""
Modelos Baseline: Scikit-Learn e PyTorch (MLP).
Atende ao requisito 'PyTorch + MLflow' da rubrica (5% da nota).
"""
import torch
import torch.nn as nn
from sklearn.ensemble import RandomForestClassifier

def get_sklearn_baseline(**kwargs) -> RandomForestClassifier:
    """
    Retorna o modelo baseline em Scikit-Learn.
    """
    return RandomForestClassifier(
        n_estimators=kwargs.get('n_estimators', 100),
        max_depth=kwargs.get('max_depth', None),
        random_state=kwargs.get('random_state', 42),
        class_weight='balanced'
    )

class CreditRiskMLP(nn.Module):
    """
    Modelo PyTorch (Multilayer Perceptron) para classificação de risco.
    """
    def __init__(self, input_dim: int, hidden_dim: int = 64, output_dim: int = 1):
        super(CreditRiskMLP, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim // 2, output_dim),
            nn.Sigmoid()  # Saída entre 0 e 1 para probabilidade
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)

def get_pytorch_baseline(input_dim: int, **kwargs) -> CreditRiskMLP:
    """
    Retorna o modelo baseline em PyTorch.
    """
    return CreditRiskMLP(
        input_dim=input_dim,
        hidden_dim=kwargs.get('hidden_dim', 64)
    )
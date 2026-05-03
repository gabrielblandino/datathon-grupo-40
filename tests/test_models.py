import torch
from generator.models.baseline import get_sklearn_baseline, get_pytorch_baseline

def test_model_baselines_coverage():
    # Testa a criação do modelo Scikit-Learn
    model_sk = get_sklearn_baseline(n_estimators=10)
    assert model_sk.n_estimators == 10
    
    # Testa a criação do modelo PyTorch (MLP) exigido na Etapa 1
    model_pt = get_pytorch_baseline(input_dim=10, hidden_dim=20)
    assert isinstance(model_pt, torch.nn.Module)
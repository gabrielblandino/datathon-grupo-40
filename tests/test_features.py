"""Testes de feature engineering e schema contracts."""
import pytest
import pandera.pandas as pa
from generator.features.feature_engineering import compute_features

# Contrato estrito de saída das features (Evita erros em produção)
FEATURE_SCHEMA = pa.DataFrameSchema({
    "feature_1": pa.Column(float, pa.Check.between(0, 1)),
    "feature_2": pa.Column(float, pa.Check.gt(0)),
    "feature_1_x_feature_2": pa.Column(float),
})

def test_schema_contract(sample_data):
    """Features de saída devem respeitar o contrato de schema."""
    result = compute_features(sample_data)
    FEATURE_SCHEMA.validate(result)

def test_no_nulls(sample_data):
    """Nenhuma feature pode ter null após transformação."""
    result = compute_features(sample_data)
    assert result.isnull().sum().sum() == 0

def test_row_count_preserved(sample_data):
    """Número de registros deve ser preservado garantindo integridade das observações."""
    result = compute_features(sample_data)
    assert len(result) == len(sample_data)

def test_compute_features_full_logic(sample_data):
    # Adicionando teste para a lógica de multiplicação de features
    from generator.features.feature_engineering import compute_features
    result = compute_features(sample_data)
    assert "feature_1_x_feature_2" in result.columns
    assert result["feature_1_x_feature_2"].iloc[0] == pytest.approx(0.1 * 1.0)

def test_compute_features_logic():
    from generator.features.feature_engineering import compute_features
    import pandas as pd
    df = pd.DataFrame({"feature_1": [2.0], "feature_2": [5.0]})
    result = compute_features(df)
    # Garante que a lógica de multiplicação está coberta[cite: 1, 2]
    assert "feature_1_x_feature_2" in result.columns
    assert result["feature_1_x_feature_2"].iloc[0] == 10.0
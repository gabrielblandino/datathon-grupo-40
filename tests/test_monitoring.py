# tests/test_monitoring.py
import pandas as pd
from fastapi.testclient import TestClient
from generator.serving.app import app, REQUEST_COUNT
from generator.monitoring.drift import check_data_drift

client = TestClient(app)

def test_check_data_drift_no_drift():
    """Testa a função de drift com dados idênticos (não deve haver drift)."""
    df_reference = pd.DataFrame({'feature_1': [1, 2, 3], 'feature_2': [10, 20, 30]})
    df_current = pd.DataFrame({'feature_1': [1, 2, 3], 'feature_2': [10, 20, 30]})
    
    has_drift = check_data_drift(df_reference, df_current, drift_threshold=0.2)
    assert has_drift is False

def test_prometheus_metrics_middleware():
    """Garante que o middleware do Prometheus no app.py conta requisições corretamente."""
    # Captura a métrica exata definida no app.py (labels: method, endpoint)
    metric_value_before = REQUEST_COUNT.labels(method='GET', endpoint='/health')._value.get()
    
    response = client.get("/health")
    assert response.status_code == 200
    
    metric_value_after = REQUEST_COUNT.labels(method='GET', endpoint='/health')._value.get()
    assert metric_value_after > metric_value_before

def test_prometheus_metrics_endpoint_exists():
    """Garante que o endpoint /metrics está expondo os dados para o Grafana."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "app_requests_total" in response.text
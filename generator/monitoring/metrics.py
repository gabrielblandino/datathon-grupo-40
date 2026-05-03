"""
Métricas customizadas do Prometheus para Observabilidade Operacional (Etapa 3).
"""
import time
from typing import Callable
from fastapi import Request
from prometheus_client import Counter, Histogram

# Contadores e Histogramas para o painel do Grafana
REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total de requisições recebidas pela API",
    ["method", "endpoint", "http_status"]
)

REQUEST_LATENCY = Histogram(
    "api_request_latency_seconds",
    "Latência das requisições em segundos",
    ["method", "endpoint"]
)

LLM_PREDICTION_COUNT = Counter(
    "llm_predictions_total",
    "Total de predições/respostas geradas pelo Agente LLM",
    ["status"]
)

async def prometheus_metrics_middleware(request: Request, call_next: Callable):
    """
    Middleware do FastAPI para interceptar requisições e registrar métricas no Prometheus.
    Para usar no app.py, adicione: app.middleware("http")(prometheus_metrics_middleware)
    """
    method = request.method
    endpoint = request.url.path
    
    start_time = time.time()
    
    try:
        response = await call_next(request)
        status_code = response.status_code
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()
    except Exception as e:
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=500).inc()
        raise e
    finally:
        latency = time.time() - start_time
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(latency)
        
    return response
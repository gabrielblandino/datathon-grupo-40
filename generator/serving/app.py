from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, make_asgi_app
import time
import os
import logging
import mlflow
from dotenv import load_dotenv

from generator.agent.react_agent import create_datathon_agent
from generator.security.guardrails import InputGuardrail, OutputGuardrail

load_dotenv()


logger = logging.getLogger(__name__)

app = FastAPI(title="Datathon API - Grupo 40", version="0.1.0")

# --- MONITORAMENTO (Prometheus) ---
REQUEST_COUNT = Counter("app_requests_total", "Total de requisições", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("app_request_latency_seconds", "Latência das requisições")

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# --- CONFIGURAÇÃO MLFLOW ---
base_dir = os.getcwd()
db_path = os.path.join(base_dir, "mlflow.db")
mlflow.set_tracking_uri(f"sqlite:///{db_path}")

# --- INICIALIZAÇÃO DE COMPONENTES ---
# Inicializa o agente e as proteções em memória quando a API sobe
input_guardrail = InputGuardrail()
output_guardrail = OutputGuardrail(language="pt")
agent_executor = create_datathon_agent()

class PredictRequest(BaseModel):
    # Ajuste para Pydantic V2 (remove o warning de 'example')
    texto: str = Field(..., json_schema_extra={"example": "Qual o DTI máximo para Grau A?"})

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_LATENCY.observe(latency)
    return response

@app.get("/")
def read_root():
    return {
        "projeto": "Datathon Fase 5 - Grupo 40",
        "status": "Online",
        "documentacao": "/docs",
        "metricas": "/metrics"
    }

@app.get("/health")
def healthcheck():
    # Ajustado para bater com a expectativa do teste tests/test_api.py
    return {"status": "ok", "service": "LLM Agent"}

@app.post("/api/v1/predict")
def predict(request: PredictRequest):
    query = request.texto
    
    # 1. Validação de Input (Prevenção de Prompt Injection)
    is_valid, reason = input_guardrail.validate(query)
    if not is_valid:
        raise HTTPException(status_code=400, detail=reason)
    
    # 2. Execução do Agente ReAct (com uso real das Tools)
    try:
        agent_response = agent_executor.invoke({"input": query})
        raw_answer = agent_response.get("output", "Desculpe, não consegui processar a resposta.")
    except Exception as e:
        logger.error(f"Erro na execução do agente: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no processamento do agente.")

    # 3. Sanitização de Output (Anonimização de PII via Presidio)
    safe_answer = output_guardrail.sanitize(raw_answer)

    return {
        "resultado": safe_answer,
        "modelo_versao": "ReAct_Agent_v1",
        "data_processamento": time.strftime("%Y-%m-%d %H:%M:%S")
    }
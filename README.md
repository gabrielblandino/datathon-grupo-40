# 🚀 Classificador de Risco de Crédito & LLM Agent - Datathon Fase 05

Este projeto compõe a entrega final do **Datathon Fase 05 (Grupo 40)**, consistindo em uma plataforma ponta a ponta de Machine Learning (MLOps) e LLMs operacionais. O sistema atua na avaliação de risco de crédito, orquestrando desde a engenharia de features até a exposição de um Agente RAG (ReAct) protegido por Guardrails e monitorado continuamente.

## 🎯 Maturidade MLOps (Nível 2)
Arquitetura projetada para atender ao **Nível 2 do Microsoft MLOps Maturity Model**, com foco em:
* **Pipelines Reprodutíveis:** Uso de DVC para tracking de dados e Docker para isolamento.
* **Tracking e Governança:** MLflow registrando métricas (AUC, F1), hiperparâmetros, artefatos e *tags* de negócio e conformidade LGPD.
* **Observabilidade:** Monitoramento ativo via Prometheus/Grafana (latência, requests) e detecção de degradação preditiva (Data Drift) com Evidently.
* **Segurança GenAI:** Agente RAG isolado, testes adversariais (Red Team) e Presidio Analyzer para sanitização de PII em tempo real.

## 📁 Estrutura de Diretórios
```text
datathon-grupo-40/
├── configs/               # Configurações de hiperparâmetros e monitoramento
├── docs/                  # System Card, Model Card, Threat Modeling (OWASP) e Report Red Team
├── evaluation/            # Scripts de avaliação LLM-as-a-Judge e métricas RAGAS
├── generator/             # Código-fonte principal da aplicação
│   ├── agent/             # Lógica do Agente ReAct, RAG Pipeline e Ferramentas (Tools)
│   ├── features/          # Engenharia de Features e processamento
│   ├── models/            # Modelos Baseline (Scikit-Learn e MLP PyTorch)
│   ├── monitoring/        # Scripts de Data Drift (Evidently) e Métricas (Prometheus)
│   ├── security/          # Guardrails de Input (Injection) e Output (PII Masking)
│   └── serving/           # Endpoints FastAPI
├── tests/                 # Testes unitários (Pytest) com cobertura superior a 60%
├── notebooks/             # Análise Exploratória de Dados (EDA)
├── pyproject.toml         # Gestão de dependências padronizada
├── dvc.yaml               # Grafo do pipeline de dados (DAG)
├── docker-compose.yml     # Orquestração de serviços (API, MLflow, Prometheus, Grafana)
└── Makefile               # Automação de comandos

🛠️ Como Executar Localmente
1. Pré-requisitos
Python 3.11+

Docker e Docker Compose

Git e DVC instalados

Chave da OpenAI (OPENAI_API_KEY)

2. Configuração do Ambiente (Setup)
Clone o repositório e configure as variáveis de ambiente utilizando o arquivo de exemplo:

Bash
cp .env.example .env
# Edite o arquivo .env e insira sua OPENAI_API_KEY
Instale as dependências e baixe os dados processados via DVC:

Bash
make setup
3. Qualidade de Código e Testes
Garanta que a aplicação atende aos critérios de qualidade (Pytest, Linting e Security Scan):

Bash
make test
(O pipeline falhará caso a cobertura de testes seja inferior a 60%)

4. Treinamento do Modelo (MLflow)
Execute o pipeline completo (Feature Engineering e Treinamento) de forma reprodutível via DVC:

Bash
make train
Acesse a interface do MLflow para visualizar os experimentos: http://localhost:5000

5. Execução dos Serviços (API, Prometheus, Grafana)
Para levantar a arquitetura completa em containers:

Bash
make docker-build
make docker-run
API FastAPI (Agente): http://localhost:8000/docs

Métricas Prometheus: http://localhost:9090

Dashboard Grafana: http://localhost:3001 (Credenciais: admin / admin)

🛡️ Segurança e Governança
Todas as interações com o LLM são interceptadas por nossos Guardrails:

Input: Bloqueio ativo de tentativas de Prompt Injection e Context Stuffing.

Output: Detecção e supressão de informações sensíveis (PII) utilizando o framework Microsoft Presidio em conformidade com a LGPD.

Consulte a pasta docs/ para o plano LGPD completo e os resultados dos ataques simulados (Red Team).
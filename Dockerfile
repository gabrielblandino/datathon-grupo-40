# Container de serving
FROM python:3.11-slim

# Evita a gravação de arquivos .pyc e obriga o stdout a não usar buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
COPY pyproject.toml .
RUN pip install --upgrade pip && pip install -e .

# Copiar código fonte
COPY generator/ /app/generator/
COPY configs/ /app/configs/

# Expor porta FastAPI
EXPOSE 8000

# Executar a aplicação via Uvicorn
CMD ["uvicorn", "generator.serving.app:app", "--host", "0.0.0.0", "--port", "8000"]
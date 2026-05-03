.PHONY: setup test train serve docker-build docker-run

setup:
	pip install -e ".[dev]"
	dvc pull

test:
	pytest tests/ -v --cov=generator --cov-fail-under=60

train:
	dvc repro train

serve:
	uvicorn generator.serving.app:app --reload

docker-build:
	docker-compose build

docker-run:
	docker-compose up -d
.PHONY: help install train test run docker-build docker-up clean

help:
	@echo "Available commands:"
	@echo "  make install     - Install dependencies (conda)"
	@echo "  make train       - Train all models"
	@echo "  make test        - Run tests"
	@echo "  make run-api     - Run FastAPI server"
	@echo "  make run-dash    - Run Streamlit dashboard"
	@echo "  make docker-build - Build Docker images"
	@echo "  make docker-up   - Start all containers"
	@echo "  make clean       - Clean cache files"

install:
	conda env create -f environment.yml
	@echo "✅ Environment created. Run 'conda activate renai'"

train:
	conda run -n renai python ml_pipeline/src/train_pipeline.py

test:
	conda run -n renai pytest tests/ -v

run-api:
	conda run -n renai uvicorn backend.app.main:app --reload --port 8000

run-dash:
	conda run -n renai streamlit run dashboard/app.py

docker-build:
	docker-compose -f docker/docker-compose.yml build

docker-up:
	docker-compose -f docker/docker-compose.yml up -d

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".DS_Store" -delete
	@echo "✅ Cleaned cache files"
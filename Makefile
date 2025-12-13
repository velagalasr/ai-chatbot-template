.PHONY: help install setup run test clean docker docker-up docker-down deploy-aws deploy-azure deploy-hf eval verify

# Default target
help:
	@echo "AI Chatbot Template - Available Commands"
	@echo "========================================"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install      - Install all dependencies"
	@echo "  make setup        - Complete first-time setup"
	@echo ""
	@echo "Development:"
	@echo "  make run          - Run the chatbot locally"
	@echo "  make test         - Run all tests"
	@echo "  make eval         - Run evaluation suite"
	@echo "  make verify       - Verify environment setup"
	@echo ""
	@echo "Docker:"
	@echo "  make docker       - Build Docker image"
	@echo "  make docker-up    - Start with docker-compose"
	@echo "  make docker-down  - Stop docker-compose"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy-aws   - Deploy to AWS (requires AWS CLI)"
	@echo "  make deploy-azure - Deploy to Azure (requires Azure CLI)"
	@echo "  make deploy-hf    - Deploy to HuggingFace Spaces"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean        - Clean cache and temp files"
	@echo "  make init-db      - Initialize vector database"
	@echo ""

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

# First-time setup
setup:
	@echo "Running first-time setup..."
	@if not exist .env copy .env.example .env
	@echo "✅ .env file created (please add your API keys)"
	@if not exist logs mkdir logs
	@if not exist data\evaluation\results mkdir data\evaluation\results
	@echo "✅ Directories created"
	$(MAKE) install
	@echo ""
	@echo "🎉 Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Edit .env and add your API keys"
	@echo "2. Run 'make init-db' to initialize vector database"
	@echo "3. Run 'make run' to start the chatbot"

# Run the application
run:
	@echo "Starting chatbot..."
	streamlit run app.py

# Run tests
test:
	@echo "Running tests..."
	pytest tests/ -v

# Run evaluation
eval:
	@echo "Running evaluation..."
	python scripts/evaluate.py

# Verify setup
verify:
	@echo "Verifying setup..."
	python scripts/verify_setup.py

# Initialize vector database
init-db:
	@echo "Initializing vector database..."
	python scripts/init_vectordb.py

# Build Docker image
docker:
	@echo "Building Docker image..."
	docker build -t ai-chatbot:latest .
	@echo "✅ Docker image built: ai-chatbot:latest"

# Start with docker-compose
docker-up:
	@echo "Starting services with docker-compose..."
	docker-compose up -d
	@echo "✅ Services started"
	@echo "Access at: http://localhost:8501"

# Stop docker-compose
docker-down:
	@echo "Stopping services..."
	docker-compose down
	@echo "✅ Services stopped"

# Deploy to AWS
deploy-aws:
	@echo "Deploying to AWS ECS..."
	@cd deployment/aws && docker build -t ai-chatbot-aws .
	@echo "Please configure AWS CLI and update task-definition.json"
	@echo "See deployment/aws/README.md for detailed instructions"

# Deploy to Azure
deploy-azure:
	@echo "Deploying to Azure Container Instances..."
	@cd deployment/azure && docker build -t ai-chatbot-azure .
	@echo "Please configure Azure CLI"
	@echo "See deployment/azure/README.md for detailed instructions"

# Deploy to HuggingFace Spaces
deploy-hf:
	@echo "Deploying to HuggingFace Spaces..."
	@cd deployment/huggingface && docker build -t ai-chatbot-hf .
	@echo "See deployment/huggingface/README.md for instructions"

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	@if exist __pycache__ rmdir /s /q __pycache__
	@for /d /r %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
	@if exist .pytest_cache rmdir /s /q .pytest_cache
	@if exist .coverage del .coverage
	@if exist htmlcov rmdir /s /q htmlcov
	@for /r %%f in (*.pyc) do @if exist "%%f" del "%%f"
	@for /r %%f in (*.pyo) do @if exist "%%f" del "%%f"
	@echo "✅ Cleanup complete"

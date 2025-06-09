.PHONY: env install

dotenv:
	@echo "Setting up environment variables..."
	@if [ ! -f .env ]; then cp .env.example .env ; fi
	cp .env.example .env

venv:
	@echo "Setting up virtual environment..."
	@if [ ! -d venv ]; then python -m venv venv ; fi

install:
	@echo "Installing dependencies..."
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt
	venv/bin/pip install -e opensky-api/python

download:
	@echo "Downloading data..."
	@if [ ! -d data ]; then mkdir data ; fi
	venv/bin/python get_data.py
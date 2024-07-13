venv:
	python3 -m venv env

install:
	pip install -r requirements.txt

dev:
	pip install -e .

test:
	pytest tests

run:
	python3 package_name  # Run script located at src/package_name/__main__.py

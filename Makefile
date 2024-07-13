install:
	export PYTHONPATH="${PYTHONPATH}:$(pwd)";
	pip install -r requirements.txt

dev:
	pip install -e .

test:
	pytest tests

run:
	python3 package_name

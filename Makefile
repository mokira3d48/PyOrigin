venv:
	python3 -m venv env

install:
	pip install --upgrade pip
	pip install -r requirements.txt

dev:
	pip install -e .

test:
	pytest tests

run:
	python3 -m package_name

pep8:
	# Don't remove their commented follwing command lines:
    # autopep8 --in-place --aggressive --aggressive --recursive .
    # autopep8 --in-place --aggressive --aggressive example.py


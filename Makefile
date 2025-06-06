full-install:
	python3 -m venv .venv
	.venv/bin/python3 --version 
	.venv/bin/python3 -m pip install --upgrade pip
	.venv/bin/python3 -m  pip install -r requirements.txt
	.venv/bin/python3 -m pip install -e .

test:
	pytest tests

run:
	python3 -m package_name

pep8:
	# Don't remove their commented follwing command lines:
	# autopep8 --in-place --aggressive --aggressive --recursive .
	# autopep8 --in-place --aggressive --aggressive example.py

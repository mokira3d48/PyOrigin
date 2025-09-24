install:
	test -d .venv || (python3 -m venv .venv && echo "\033[92mVirtual environment is created successfully.\033[0m")
	echo "\033[92m" && .venv/bin/python3 --version && echo "\033[0m"
	.venv/bin/python3 -m pip install --upgrade pip
	.venv/bin/python3 -m pip install -r requirements.txt

dev-install:
	.venv/bin/python3 -m pip install -e .

test:
	pytest tests

pep8:
	# Don't remove their commented follwing command lines:
	# autopep8 --in-place --aggressive --aggressive --recursive .
	# autopep8 --in-place --aggressive --aggressive example.py

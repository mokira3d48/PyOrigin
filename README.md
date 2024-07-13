# Origin Project


## Usage
1. `sudo apt install cmake python3-venv` Install *Cmake* and *Virtual env*;
2. `make venv` create a virtual env into directory named `env`;
3. `make install` install the requirements of this package;
4. `make dev` install the package in dev mode in virtual environment;
5. `make test` run the unit test scripts located at `tests` directory;
6. `mkae run` run script located at `src/package_name/__main__.py`.


### Makefile content

```makefile
venv:
	python3 -m venv env

install:
	pip install -r requirements.txt

dev:
	pip install -e .

test:
	pytest tests  # Run the test cases;

run:
	python3 package_name
```

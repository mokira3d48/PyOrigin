# Origin Project
![](https://img.shields.io/badge/Python-3.10.12-blue)
<!-- ![](https://img.shields.io/badge/Django-5.0-%2344B78B) -->
<!-- ![](https://img.shields.io/badge/REST%20Framework-3.14.0-%23A30000) -->
<!-- ![](https://img.shields.io/badge/Swagger-OpenAPI%202.0-%23aaaa00) -->
![](https://img.shields.io/badge/LICENSE-MIT-%2300557f)
![](https://img.shields.io/badge/lastest-2024--07--13-success)
![](https://img.shields.io/badge/contact-dr.mokira%40gmail.com-blueviolet)

## Usage
1. `sudo apt install cmake python3-venv` Install *Cmake* and *Virtual env*;
2. `make venv` create a virtual env into directory named `env`;
3. `ssource env/bin/activate` activate the virtual environment named `env`;
4. `make install` install the requirements of this package;
5. `make dev` install the package in dev mode in virtual environment;
6. `make test` run the unit test scripts located at `tests` directory;
7. `mkae run` run script located at `src/package_name/__main__.py`.


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

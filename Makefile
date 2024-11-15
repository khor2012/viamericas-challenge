install:
	pip install -r requirements/pip-tools.txt
	uv pip install -r requirements/base.txt

compile:
	uv pip compile requirements/pip-tools.in -o requirements/pip-tools.txt
	uv pip compile requirements/base.in -o requirements/base.txt
	uv pip compile requirements/test.in -o requirements/test.txt

upgrade:
	uv pip compile requirements/pip-tools.in -o requirements/pip-tools.txt --upgrade
	uv pip compile requirements/test.in -o requirements/test.txt --upgrade
	uv pip compile requirements/base.in -o requirements/base.txt --upgrade

sync:
	uv pip sync requirements/base.txt requirements/pip-tools.txt requirements/test.txt

format:
	ruff format
	ruff check --fix

tests:
	coverage run manage.py test
	coverage report -m

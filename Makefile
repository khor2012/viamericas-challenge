install:
	pip install -r requirements/pip-tools.txt
	uv pip install -r requirements/base.txt

compile:
	uv pip compile requirements/pip-tools.in -o requirements/pip-tools.txt
	uv pip compile requirements/base.in -o requirements/base.txt

upgrade:
	uv pip compile requirements/pip-tools.in -o requirements/pip-tools.txt --upgrade
	uv pip compile requirements/base.in -o requirements/base.txt --upgrade

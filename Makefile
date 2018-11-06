DEPS:=requirements.txt
VIRTUALENV=$(shell which virtualenv)
PIP:="venv/bin/pip"
CMD_FROM_VENV:=". venv/bin/activate; which"
PYTHON=$(shell "$(CMD_FROM_VENV)" "python")

.PHONY: requirements killmanage serve shell pyclean clean cleanpipcache tests

## TODO add tox, test, venv, lint, isort, ...


## Utilities for the venv currently active.

requirements:
	pip install -U -r $(DEPS)

killmanage:
	pkill -f manage.py

serve:
	python ./manage.py runserver

shell:
	python ./manage.py shell

tests:
	python ./manage.py test


## Generic utilities.

pyclean:
	find . -name *.pyc -delete
	rm -rf *.egg-info build
	rm -rf coverage.xml .coverage
	rm -rf .pytest_cache

clean: pyclean
	rm -rf venv
	rm -rf .tox
	rm -rf dist

cleanpipcache:
	rm -rf ~/Library/Caches/pip

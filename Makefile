# This Makefile requires the following commands to be available:
# * virtualenv
# * python2

DEPS:=requirements.txt
VIRTUALENV=$(shell which virtualenv)
PIP:="venv/bin/pip"
CMD_FROM_VENV:=". venv/bin/activate; which"
PYTHON=$(shell "$(CMD_FROM_VENV)" "python")

.PHONY: requirements killmanage serve shell pyclean clean cleanpipcache tests

## TODO add tox, test, venv, lint, isort, ...


## Django local dev in the venv currently active.

killmanage: _ensure_active_env
	pkill -f manage.py

serve: _ensure_active_env
	python ./manage.py runserver

shell: _ensure_active_env
	python ./manage.py shell

tests: _ensure_active_env
	python ./manage.py test


## Utilities for the venv currently active.

_ensure_active_env:
ifndef VIRTUAL_ENV
	@echo 'Error: no virtual environment active'
	@exit 1
endif

requirements: _ensure_active_env
	pip install -U -r $(DEPS)


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

pipclean:
	rm -rf ~/Library/Caches/pip
	rm -rf ~/.cache/pip
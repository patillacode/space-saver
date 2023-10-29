# Makefile for space_saver.py

# Variables
VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python3

# Targets

.PHONY: help setup run clean install test lint format docs

help:
	@echo "make clean"
	@echo "       remove python artifacts and virtualenv"
	@echo "make install"
	@echo "       install the project dependencies"

clean:
	rm -rf $(VENV_NAME)
	find -iname "*.pyc" -delete

install:
	python3 -m venv $(VENV_NAME)
	${PYTHON} -m pip install -r requirements.txt


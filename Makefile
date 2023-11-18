# Makefile for space_saver.py

VENV_NAME?=venv
PYTHON=${VENV_NAME}/bin/python3


help:
	@echo "make clean"
	@echo "       remove python artifacts and virtualenv"
	@echo "make install"
	@echo "       install the project dependencies"

clean:
	rm -rf $(VENV_NAME)
	find . -name "*.pyc" -delete

install:
	python3 -m venv $(VENV_NAME)
	${PYTHON} -m pip install -r requirements.txt


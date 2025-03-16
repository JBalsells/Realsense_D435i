VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

REQ := requirements.txt

# Crear entorno virtual
venv:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

# Instalar dependencias
install: venv
	$(PIP) install -r $(REQ)

# Ejecutar el código principal (modifica main.py según tu proyecto)
run: venv
	$(PYTHON) main.py

# Formatear código con black
format: venv
	$(PYTHON) -m black .

# Revisar estilo con flake8
lint: venv
	$(PYTHON) -m flake8 .

# Ejecutar pruebas con pytest
test: venv
	$(PYTHON) -m pytest tests/

# Limpiar archivos innecesarios
clean:
	rm -rf __pycache__ $(VENV) *.pyc *.pyo .pytest_cache .mypy_cache .ruff_cache

# Actualizar dependencias en requirements.txt
freeze: venv
	$(PIP) freeze > $(REQ)

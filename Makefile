PYTHON = C:/WWW/IFTS/backend/api/.venv/Scripts/python.exe
MANAGE = $(PYTHON) manage.py

.PHONY: help runserver migrate makemigrations createsuperuser shell install test clean

help:
	@echo "Comandos disponibles:"
	@echo "  runserver       - Ejecutar el servidor de desarrollo"
	@echo "  migrate         - Aplicar migraciones a la base de datos"
	@echo "  makemigrations  - Crear nuevas migraciones"
	@echo "  createsuperuser - Crear un superusuario"
	@echo "  shell           - Abrir shell de Django"
	@echo "  install         - Instalar dependencias"
	@echo "  test            - Ejecutar tests"
	@echo "  clean           - Limpiar archivos temporales"
	@echo "  setup           - Configuracion inicial completa"
	@echo "  resetdb         - Resetear base de datos (CUIDADO!)"

runserver:
	@echo "Iniciando servidor de desarrollo..."
	$(MANAGE) runserver

migrate:
	@echo "Aplicando migraciones..."
	$(MANAGE) migrate

makemigrations:
	@echo "Creando migraciones..."
	$(MANAGE) makemigrations

createsuperuser:
	@echo "Creando superusuario..."
	$(MANAGE) createsuperuser

shell:
	@echo "Abriendo shell de Django..."
	$(MANAGE) shell

install:
	@echo "Instalando dependencias..."
	$(PYTHON) -m pip install --upgrade pip
	@if exist requirements.txt $(PYTHON) -m pip install -r requirements.txt

test:
	@echo "Ejecutando tests..."
	$(MANAGE) test

clean:
	@echo "Limpiando archivos temporales..."
	@if exist db.sqlite3 del /Q db.sqlite3
	@for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
	@for /d /r . %%d in (*.egg-info) do @if exist "%%d" rd /s /q "%%d"

setup: makemigrations migrate createsuperuser
	@echo "Configuracion inicial completada!"
	@echo "Ahora puedes ejecutar: make runserver"

resetdb:
	@echo "ADVERTENCIA: Esto eliminara toda la base de datos!"
	@echo "Estas seguro? Presiona Ctrl+C para cancelar o Enter para continuar..."
	@pause
	@if exist db.sqlite3 del /Q db.sqlite3
	@for /d /r . %%d in (migrations) do @if exist "%%d" for %%f in ("%%d\*.py") do @if not "%%~nf"=="__init__" del /Q "%%f"
	$(MAKE) makemigrations
	$(MAKE) migrate
	@echo "Base de datos reseteada!"

dev-setup: install makemigrations migrate
	@echo "Configuracion de desarrollo completada!"

freeze:
	@echo "Generando requirements.txt..."
	$(PYTHON) -m pip freeze > requirements.txt
	@echo "requirements.txt generado!"

status:
	@echo "Estado del proyecto:"
	@echo "Python: $(PYTHON)"
	@echo "Django version:"
	@$(MANAGE) --version
	@echo "Migraciones pendientes:"
	@$(MANAGE) showmigrations --plan

collectstatic:
	@echo "Recolectando archivos estaticos..."
	$(MANAGE) collectstatic --noinput

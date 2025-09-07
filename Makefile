# Makefile para el proyecto Django
# Ejecutar con: make <comando>

# Variables
PYTHON = C:/WWW/IFTS/backend/api/.venv/Scripts/python.exe
MANAGE = $(PYTHON) manage.py

# Comandos disponibles
.PHONY: help runserver migrate makemigrations createsuperuser shell install test clean

# Mostrar ayuda
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
	@echo "  setup           - Configuración inicial completa"
	@echo "  resetdb         - Resetear base de datos (¡CUIDADO!)"

# Ejecutar servidor de desarrollo
runserver:
	@echo "🚀 Iniciando servidor de desarrollo..."
	$(MANAGE) runserver

# Aplicar migraciones
migrate:
	@echo "📊 Aplicando migraciones..."
	$(MANAGE) migrate

# Crear migraciones
makemigrations:
	@echo "📝 Creando migraciones..."
	$(MANAGE) makemigrations

# Crear superusuario
createsuperuser:
	@echo "👤 Creando superusuario..."
	$(MANAGE) createsuperuser

# Abrir shell de Django
shell:
	@echo "🐍 Abriendo shell de Django..."
	$(MANAGE) shell

# Instalar dependencias (si tienes requirements.txt)
install:
	@echo "📦 Instalando dependencias..."
	$(PYTHON) -m pip install --upgrade pip
	@if exist requirements.txt $(PYTHON) -m pip install -r requirements.txt

# Ejecutar tests
test:
	@echo "🧪 Ejecutando tests..."
	$(MANAGE) test

# Limpiar archivos temporales
clean:
	@echo "🧹 Limpiando archivos temporales..."
	@if exist db.sqlite3 del /Q db.sqlite3
	@for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
	@for /d /r . %%d in (*.egg-info) do @if exist "%%d" rd /s /q "%%d"

# Configuración inicial completa
setup: makemigrations migrate createsuperuser
	@echo "✅ Configuración inicial completada!"
	@echo "Ahora puedes ejecutar: make runserver"

# Resetear base de datos (¡USAR CON CUIDADO!)
resetdb:
	@echo "⚠️  ADVERTENCIA: Esto eliminará toda la base de datos!"
	@echo "¿Estás seguro? Presiona Ctrl+C para cancelar o Enter para continuar..."
	@pause
	@if exist db.sqlite3 del /Q db.sqlite3
	@for /d /r . %%d in (migrations) do @if exist "%%d" for %%f in ("%%d\*.py") do @if not "%%~nf"=="__init__" del /Q "%%f"
	$(MAKE) makemigrations
	$(MAKE) migrate
	@echo "🔄 Base de datos reseteada!"

# Comandos específicos para desarrollo
dev-setup: install makemigrations migrate
	@echo "🛠️  Configuración de desarrollo completada!"

# Generar requirements.txt
freeze:
	@echo "📋 Generando requirements.txt..."
	$(PYTHON) -m pip freeze > requirements.txt
	@echo "✅ requirements.txt generado!"

# Verificar estado del proyecto
status:
	@echo "📊 Estado del proyecto:"
	@echo "Python: $(PYTHON)"
	@echo "Django version:"
	@$(MANAGE) --version
	@echo "Migraciones pendientes:"
	@$(MANAGE) showmigrations --plan

# Ejecutar collectstatic (para producción)
collectstatic:
	@echo "🎨 Recolectando archivos estáticos..."
	$(MANAGE) collectstatic --noinput

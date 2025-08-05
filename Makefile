# Makefile para MQTT to PostgreSQL Writer

.PHONY: help build up down logs clean test setup sample-data simulate

# Variables
COMPOSE_FILE = docker-compose.yml
SERVICE_NAME = mqtt-writer

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Construir las imágenes Docker
	docker-compose build

up: ## Levantar todos los servicios
	docker-compose up -d

up-with-admin: ## Levantar servicios incluyendo pgAdmin
	docker-compose --profile admin up -d

down: ## Detener todos los servicios
	docker-compose down

logs: ## Ver logs del servicio principal
	docker-compose logs -f $(SERVICE_NAME)

logs-all: ## Ver logs de todos los servicios
	docker-compose logs -f

clean: ## Limpiar containers, volúmenes e imágenes
	docker-compose down -v --rmi all --remove-orphans

clean-orphans: ## Limpiar contenedores huérfanos
	docker-compose down --remove-orphans
	@echo "Contenedores huérfanos eliminados ✅"

setup: build up ## Configuración completa inicial
	@echo "Esperando que los servicios estén listos..."
	@sleep 10
	@make sample-data
	@echo "¡Sistema listo! 🎉"
	@echo "pgAdmin: http://localhost:8080 (admin@geotel.com / admin123)"

sample-data: ## Crear datos de ejemplo en la base de datos
	docker-compose exec $(SERVICE_NAME) python create_sample_data.py

simulate: ## Ejecutar simulador MQTT para todas las unidades
	docker-compose --profile testing up mqtt-simulator

simulate-unit: ## Simular una unidad específica (usar UNIT=número)
	docker-compose exec $(SERVICE_NAME) python simulate_mqtt.py --unit $(or $(UNIT),1) --delay 3

test-mqtt: ## Enviar mensajes MQTT de prueba
	@echo "Enviando mensajes de prueba..."
	mosquitto_pub -h localhost -t "U1_Combustible" -m "75.5"
	mosquitto_pub -h localhost -t "U1_Velocidad" -m "85.2"
	mosquitto_pub -h localhost -t "U1_RPM" -m "2200"
	mosquitto_pub -h localhost -t "U1_Temperatura" -m "89"
	mosquitto_pub -h localhost -t "U1_Panic" -m "1"
	@echo "Mensajes enviados ✅"

db-shell: ## Acceder a la shell de PostgreSQL
	docker-compose exec postgres psql -U geotel_user -d geotel_db

db-query: ## Ejecutar consulta rápida a la BD (usar QUERY="SELECT...")
	docker-compose exec postgres psql -U geotel_user -d geotel_db -c '$(or $(QUERY),SELECT COUNT(*) FROM "Units";)'

status: ## Ver estado de los servicios
	docker-compose ps

restart: ## Reiniciar el servicio principal
	docker-compose restart $(SERVICE_NAME)

dev-install: ## Instalar dependencias para desarrollo local
	pip install -r requirements.txt

dev-run: ## Ejecutar en modo desarrollo local
	cd src && python main.py

check-health: ## Verificar salud de los servicios
	@echo "Verificando servicios..."
	@docker-compose exec postgres pg_isready -U geotel_user -d geotel_db && echo "PostgreSQL: ✅" || echo "PostgreSQL: ❌"
	@docker-compose exec mosquitto mosquitto_pub -h localhost -t test -m "health" && echo "MQTT: ✅" || echo "MQTT: ❌"

# Comandos útiles de desarrollo
lint: ## Ejecutar linting en el código Python
	@if command -v flake8 > /dev/null; then \
		flake8 src/ --max-line-length=120; \
	else \
		echo "flake8 no instalado. Instalar con: pip install flake8"; \
	fi

format: ## Formatear código Python
	@if command -v black > /dev/null; then \
		black src/; \
	else \
		echo "black no instalado. Instalar con: pip install black"; \
	fi

# Comandos de diagnóstico
debug: ## Mostrar logs y estado para diagnosticar problemas
	@echo "=== Estado de contenedores ==="
	docker-compose ps
	@echo "\n=== Logs recientes del mqtt-writer ==="
	docker-compose logs --tail=20 $(SERVICE_NAME)
	@echo "\n=== Estado de PostgreSQL ==="
	docker-compose exec postgres pg_isready -U geotel_user -d geotel_db || echo "PostgreSQL no está listo"

rebuild: down build up ## Reconstruir todo desde cero
	@echo "Sistema reconstruido ✅"

fix-restart: ## Solucionar problemas de reinicio del contenedor
	@echo "Deteniendo contenedores..."
	docker-compose down
	@echo "Reconstruyendo imagen..."
	docker-compose build --no-cache
	@echo "Iniciando servicios..."
	docker-compose up -d
	@echo "Esperando que los servicios estén listos..."
	@sleep 15
	@make logs

create-tables: ## Crear tablas en la base de datos
	@echo "Creando tablas de la base de datos..."
	docker-compose exec postgres psql -U geotel_user -d geotel_db -f /docker-entrypoint-initdb.d/01-schema.sql
	@echo "Tablas creadas ✅"

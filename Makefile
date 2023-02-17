# Convenient shortcuts for local development

build:
	docker build --tag sytizen-server .

# Default port 5000 is in use on Ventura Macs
# 7355 chosen for TESS
run:
	docker compose up --build --detach

logs:
	docker compose logs --follow

stop:
	docker compose down
migrate:
	python backend/manage.py makemigrations
	python backend/manage.py migrate

start: 
	uvicorn core.asgi:application --host 0.0.0.0 --port 8080 --proxy-headers
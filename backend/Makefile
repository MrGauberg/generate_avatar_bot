migrate:
	python manage.py makemigrations
	python manage.py migrate

start: 
	uvicorn core.asgi:application --host 0.0.0.0 --port 8080 --proxy-headers
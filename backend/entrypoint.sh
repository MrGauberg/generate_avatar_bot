set -e  # Прерывать выполнение при ошибке

echo "Checking for model changes..."
python3 manage.py makemigrations --noinput

echo "Applying migrations..."
python3 manage.py migrate

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Creating superuser..."
if [ -f "/app/core/create_superuser.py" ]; then
    python3  /app/core/create_superuser.py
else
    echo "Superuser creation script not found: /app/core/create_superuser.py"
fi

exec "$@"

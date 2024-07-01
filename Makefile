# Run Django development server
runserver:
    python manage.py runserver

# Make migrations and apply them
migrate:
    python manage.py makemigrations
    python manage.py migrate
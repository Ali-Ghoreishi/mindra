# Mindra - Useful Commands

## 1. Ruff (Code Formatting & Linting)

Format all Python files:

```bash
python -m ruff format .
```

Check and fix linting issues:

```bash
python -m ruff check . --fix
```

Organize imports:

```bash
python -m ruff check . --select I --fix
```

## 2. Django

venv

```bash
.\.venv\Scripts\Activate.ps1
```

Run development server:

```bash
python manage.py runserver
```

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Create superuser:

```bash
python manage.py createsuperuser
```

## 3. Testing

Run all tests:

```bash
python manage.py test
```

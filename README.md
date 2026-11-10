# Mindra

**Mindra** is an AI-powered personal assistant designed to help users manage their daily tasks, reminders, and productivity.

## Features

- User registration and authentication using JWT
- User profile management
- Password change and logout
- Task creation, retrieval, updating, and deletion
- Task filtering and ordering
- Task pagination
- PostgreSQL database integration

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Simple JWT

## Project Structure

```text
Mindra/
├── apps/
│   ├── users/
│   ├── tasks/
│   ├── reminders/
│   ├── assistant/
│   └── reports/
├── config/
├── .env.example
├── .gitignore
├── manage.py
└── requirements.txt
```

## Installation

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd ai-personal-assistant
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and configure your environment variables.

### 5. Configure PostgreSQL

Create a PostgreSQL database named:

```text
mindra_db
```

Update the database credentials in `.env`.

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create superuser

```bash
python manage.py createsuperuser
```

### 8. Run development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://localhost:8000/
```

## Environment Variables

See `.env.example` for the required environment variables.

## License

To be determined.
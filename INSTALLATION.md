# Installation Guide

This guide walks you through setting up the GCC website project locally.

## Prerequisites

- Python 3.10+ installed
- pip (usually included with Python)
- Git

Optional:

- MySQL (only if you plan to switch from SQLite)

## 1. Clone the Repository

```bash
git clone https://github.com/Yosores04/GCC-Web.git
cd GCC-Web
```

## 2. Create and Activate a Virtual Environment

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Copy the example environment file and edit values as needed.

### Windows (PowerShell)

```powershell
Copy-Item .env.example .env
```

### macOS/Linux

```bash
cp .env.example .env
```

At minimum, ensure the dashboard path and secret key settings are valid for your environment.

## 5. Run Database Migrations

```bash
python manage.py migrate
```

## 6. Create an Admin Account

```bash
python manage.py createsuperuser
```

## 7. Seed Initial Content

```bash
python manage.py seed_initial_content
```

## 8. Start the Development Server

```bash
python manage.py runserver
```

Open your browser at:

- Public site: http://127.0.0.1:8000/
- Django admin: http://127.0.0.1:8000/admin/
- Dashboard: http://127.0.0.1:8000/<your-secret-dashboard-path>/

## 9. Run Tests

```bash
python manage.py test tests -v 2
```

## Optional: Use MySQL Instead of SQLite

1. Update `.env` with MySQL settings.
2. Ensure your MySQL server is running and the database exists.
3. Run:

```bash
python manage.py migrate
```

If you are migrating existing SQLite data, export/import data as needed using Django management commands documented in the README.

## Troubleshooting

- If activation scripts are blocked on Windows, run PowerShell as admin once and set:

```powershell
Set-ExecutionPolicy RemoteSigned
```

- If `python` is not recognized, reinstall Python and check "Add Python to PATH" during installation.
- If static or media files are missing, verify your local folders and settings in `.env` and `config/settings.py`.

# BDMng - Blood Bank Management System

A full-featured Django web application for managing blood bank operations including donor registration, blood inventory tracking, donation recording, blood request & allocation workflows, reporting, and user management.

---

## Tech Stack

| Layer         | Technology                                  |
|---------------|---------------------------------------------|
| Language      | Python 3.12+                                |
| Framework     | Django 6.x                                  |
| Database      | SQLite (dev) / PostgreSQL (production)       |
| Frontend      | Django Templates + Tailwind CSS (CDN)        |
| JS            | Alpine.js, Chart.js, Vanilla JS              |
| Auth          | Django built-in authentication               |
| Task Queue    | Celery + Redis (optional)                    |
| Exports       | ReportLab (PDF), openpyxl (Excel)            |

---

## Features

- **Donor Management** - Full CRUD with eligibility tracking (90-day rule), age validation (18-65), blood group filtering
- **Blood Inventory** - Track units by group, collection/expiry dates, FEFO allocation, status management, expiry warnings
- **Donation Tracking** - Record donations with AJAX donor search, auto-create linked blood units, eligibility checks
- **Request & Allocation** - Blood requests from hospitals with priority levels, FEFO-based allocation, approve/reject workflow
- **Reports & Analytics** - Chart.js dashboards, donation trends, blood group distribution, critical stock alerts, PDF & Excel exports
- **User Management** - Login/logout, password reset via email, password change, user profiles, staff role management
- **Admin Panel** - All models registered in Django Admin with filters and search

---

## Project Structure

```
BDMng/
├── apps/
│   ├── accounts/        # Auth, profiles, user management
│   ├── blood_requests/  # Blood requests & allocation
│   ├── dashboard/       # Main dashboard with KPIs
│   ├── donations/       # Donation tracking
│   ├── donors/          # Donor CRUD
│   ├── inventory/       # Blood unit inventory
│   └── reports/         # Reports, charts, PDF/Excel exports
├── config/
│   ├── settings/
│   │   ├── base.py          # Shared settings
│   │   ├── development.py   # Dev settings (DEBUG=True, SQLite)
│   │   └── production.py    # Prod settings (DEBUG=False, PostgreSQL)
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── templates/           # All HTML templates
│   ├── base.html
│   ├── partials/        # Reusable partials (_messages, _pagination)
│   ├── accounts/
│   ├── dashboard/
│   ├── donations/
│   ├── donors/
│   ├── inventory/
│   ├── reports/
│   └── requests/
├── static/              # Static assets (CSS, JS, images)
├── media/               # User-uploaded files
├── manage.py
├── requirements.txt
├── .env
└── db.sqlite3
```

---

## Getting Started

### Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Git (optional)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd BDMng
```

### 2. Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root (or edit the existing one):

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_URL=redis://localhost:6379/0
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

> For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) instead of your account password.

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

### 7. Start the Development Server

```bash
python manage.py runserver
```

Open your browser and go to: **http://127.0.0.1:8000/**

---

## Default URLs

| URL                    | Description               |
|------------------------|---------------------------|
| `/`                    | Dashboard                 |
| `/donors/`             | Donor list                |
| `/inventory/`          | Blood inventory           |
| `/requests/`           | Blood requests            |
| `/donations/`          | Donation records          |
| `/reports/`            | Reports & analytics       |
| `/accounts/login/`     | Login page                |
| `/accounts/profile/`   | User profile              |
| `/accounts/users/`     | User management (admin)   |
| `/admin/`              | Django admin panel        |

---

## Business Rules

| Rule                     | Description                                                     |
|--------------------------|-----------------------------------------------------------------|
| Donor Eligibility        | Donor cannot donate if last donation was fewer than 90 days ago |
| Age Restriction          | Donors must be between 18 and 65 years old                     |
| FEFO Allocation          | Blood units with the earliest expiry date are allocated first   |
| Expiry Check             | Blood units that expire today or earlier cannot be allocated    |
| Stock Threshold Alert    | Warning triggered if any blood group has fewer than 5 units     |
| Blood Unit Shelf Life    | Blood units expire 42 days after collection (auto-calculated)   |

---

## Useful Management Commands

```bash
# Run the development server
python manage.py runserver

# Create new migrations after model changes
python manage.py makemigrations

# Apply pending migrations
python manage.py migrate

# Create a superuser account
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic

# Open Django shell for debugging
python manage.py shell

# Run system checks
python manage.py check

# Run tests for a specific app
python manage.py test apps.donors
python manage.py test apps.blood_requests

# Run all tests
python manage.py test
```

---

## Granting Permissions to Staff Users

By default, only the superuser has full access. To grant specific permissions to staff users:

1. Log in to `/admin/` as superuser
2. Go to **Users** and select the staff user
3. Under **User permissions**, add the relevant permissions:
   - `donors.view_donor`, `donors.add_donor`, `donors.change_donor`, `donors.delete_donor`
   - `inventory.view_bloodunit`, `inventory.add_bloodunit`, `inventory.change_bloodunit`, `inventory.delete_bloodunit`
   - `blood_requests.view_bloodrequest`, `blood_requests.add_bloodrequest`, `blood_requests.change_bloodrequest`
   - `donations.view_donation`, `donations.add_donation`
4. Save

Alternatively, create **Groups** (e.g., "Lab Technician", "Receptionist") with preset permissions and assign users to groups.

---

## Exporting Reports

- **PDF Report**: Navigate to `/reports/` and click **PDF Report** - generates a downloadable PDF with KPIs and donor leaderboard
- **Excel Export**: Click **Excel Export** - generates a multi-sheet `.xlsx` workbook with KPIs, top donors, and current inventory

---

## Production Deployment Checklist

1. Set `DJANGO_SETTINGS_MODULE=config.settings.production` as an environment variable
2. Set `DEBUG=False` in `.env`
3. Generate a strong `SECRET_KEY`
4. Configure PostgreSQL via `DATABASE_URL`
5. Set `ALLOWED_HOSTS` to your domain(s)
6. Run `python manage.py collectstatic --noinput`
7. Configure a reverse proxy (Nginx/Apache) with Gunicorn or uWSGI
8. Set up HTTPS (SSL/TLS)
9. Configure email backend for password reset functionality
10. (Optional) Set up Celery + Redis for background tasks

---

## License

This project is for educational and internal use.

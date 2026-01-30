# HRMS Lite – Backend

## Project Overview

This repository contains the **backend** for HRMS Lite, a lightweight Human Resource Management System built using Django and Django REST Framework.

The backend exposes RESTful APIs to manage employee records and track daily attendance. It is designed as a simple, realistic internal HR tool with proper validation, error handling, and clean API design. Authentication and advanced HR features are intentionally out of scope to keep the system focused and easy to extend.

---

## Tech Stack Used

- Django
- Django REST Framework
- Gunicorn
- django-cors-headers
- Whitenoise
- SQLite (local development)
- Python 3

---

## Steps to Run the Project Locally

### Prerequisites
- Python 3.10 or higher
- pip
- Virtual environment (recommended)

---

### Setup Instructions

1. Clone the repository:

git clone <backend-repository-url>
cd backend

2. Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate


3. Install dependencies:

pip install -r requirements.txt


4. Apply database migrations:

python manage.py migrate


5. Start the development server:

python manage.py runserver


6. The backend will be available at:

http://localhost:8000

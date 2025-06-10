# Simple Chat Application — iSi Technology Test Task

This project implements a simple chat backend using Django and Django REST Framework (DRF) with JWT authentication.  
It supports thread creation between two users, sending messages, marking messages as read, and more.

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/torykoghukhar/backend_isi.git
cd backend_isi
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Load test data

```bash
python manage.py loaddata db.json
```

### 7. Run the development server

```bash
python manage.py runserver
```

---

## API Endpoints

| Method | Endpoint                                               | Description                       |
|--------|--------------------------------------------------------|-----------------------------------|
| POST   | `/api/threads/`                                        | Create or retrieve a thread       |
| GET    | `/api/threads/`                                        | List all threads for current user |
| DELETE | `/api/threads/<thread_id>/`                            | Delete a thread                   |
| POST   | `/api/threads/<thread_id>/messages/`                   | Create a new message              |
| GET    | `/api/threads/<thread_id>/messages/`                   | List all messages in a thread     |
| POST   | `/api/threads/<thread_id>/messages/<id>/mark_as_read/` | Mark a message as read            |
| GET    | `/api/threads/<thread_id>/messages/unread-count/`      | Get unread messages count         |

---

# EventEase Backend

## Overview

EventEase Backend is a FastAPI-powered REST API that supports the EventEase web application. It manages authentication, event data, RSVP bookings, and user-specific operations. The backend is designed to be secure, scalable, and easy to integrate with the React frontend.

## Features

* FastAPI-based REST API
* Firebase Authentication validation
* JWT authorization for protected endpoints
* CRUD operations for events
* RSVP (booking) system
* Organizer-only access for specific operations
* SQLite (Development) / PostgreSQL (Production)
* Automated documentation via `/docs` and `/redoc`
* Clear modular code structure

## Technology Stack

### Framework

* FastAPI (Python 3.11+)

### Database

* SQLite (local development)
* PostgreSQL (production-ready)

### Authentication

* Firebase Authentication (ID tokens)
* JWT verification middleware

### ORM / DB Management

* SQLAlchemy
* Alembic (optional for migrations)

## Project Structure

```plaintext
backend/
 ├── app/
 │   ├── main.py
 │   ├── config.py
 │   ├── database.py
 │   ├── auth/
 │   │    ├── firebase.py
 │   │    └── jwt_handler.py
 │   ├── models/
 │   │    ├── user.py
 │   │    ├── event.py
 │   │    └── booking.py
 │   ├── routers/
 │   │    ├── auth_router.py
 │   │    ├── event_router.py
 │   │    └── booking_router.py
 │   └── schemas/
 │        ├── user_schema.py
 │        ├── event_schema.py
 │        └── booking_schema.py
 ├── requirements.txt
 ├── README.md
 ├── start.sh
 └── .env.example
```

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/username/eventease-backend.git
cd eventease-backend
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Required variables:

```plaintext
DATABASE_URL=sqlite:///./eventease.db
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CLIENT_EMAIL=your-email
FIREBASE_PRIVATE_KEY=your-private-key
JWT_SECRET=your-secret
JWT_ALGORITHM=HS256
```

## Running the Server

Run with uvicorn:

```bash
uvicorn app.main:app --reload
```

Default server:

```plaintext
http://localhost:8000
```

## API Documentation

FastAPI automatically generates interactive API docs.

* Swagger UI: `/docs`
* ReDoc: `/redoc`

## Database Models

### User

* id
* firebase_uid
* name
* email

### Event

* id
* title
* description
* start_datetime
* end_datetime
* category
* organizer_id (foreign key)

### Booking (RSVP)

* id
* user_id
* event_id
* timestamp

## Authentication Workflow

1. User logs in via Firebase (frontend)
2. Firebase returns ID token
3. Frontend sends token as:

```http
Authorization: Bearer <token>
```

4. Backend verifies token
5. Verified users access protected routes

## Routes Overview

### Auth Routes

```http
POST /auth/verify-token
```

Verify Firebase token and return backend JWT.

### Event Routes

```http
GET /events/           # List all events
GET /events/{id}       # Get single event
POST /events/          # Create event (Organizer only)
PUT /events/{id}       # Update event (Organizer only)
DELETE /events/{id}    # Delete event (Organizer only)
```

### Booking (RSVP) Routes

```http
POST /events/{id}/rsvp        # RSVP to event
DELETE /events/{id}/rsvp      # Cancel RSVP
GET /events/{id}/attendees    # Get attendees (Organizer only)
```

## Error Handling

### Success Response

```json
{
  "status": "success",
  "data": { }
}
```

### Error Response

```json
{
  "detail": "Error message here"
}
```

## Security

* Firebase token validation
* JWT-based route protection
* Organizer role checks
* SQL injection-safe ORM queries
* CORS configured for frontend

## Testing

Use Thunder Client, Postman, or curl to test endpoints.
Example:

```bash
curl http://localhost:8000/events/
```

## Deployment

EventEase Backend can be deployed using Render, Railway, or Docker.
Typical Render deployment:

1. Connect GitHub repo
2. Add environment variables
3. Select Python runtime
4. Deploy service

## Contribution Guidelines

1. Create a feature branch:

```bash
git checkout -b feature/your-feature
```

2. Follow folder structure
3. Format code (PEP8)
4. Test endpoints
5. Submit PR to `dev` branch

## License

This project is for educational and development purposes, and can be extended or adapted for production environments.

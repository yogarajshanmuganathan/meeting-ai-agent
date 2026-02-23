🚀 Meeting AI Agent (Enterprise-Grade)
Overview

A Dockerized FastAPI microservice that integrates Microsoft OAuth 2.0 and Microsoft Graph API to:

Authenticate users securely

Create calendar events

Generate Teams-style meeting links

Persist structured metadata in PostgreSQL

Run fully containerized via Docker Compose

🏗 Architecture

User
↓
FastAPI (Docker)
↓
Microsoft Identity Platform (OAuth 2.0 Authorization Code Flow)
↓
Microsoft Graph API
↓
Calendar Event Created
↓
Teams Join Link Generated
↓
PostgreSQL (Dockerized Persistence Layer)

⚙ Tech Stack

FastAPI

Microsoft Graph API

OAuth 2.0 (Azure Entra ID)

PostgreSQL

Docker & Docker Compose

psycopg2

MSAL

📦 Services
meeting_ai_app

FastAPI application

Handles authentication

Calls Graph API

Writes meeting data to DB

meeting_ai_db

PostgreSQL container

Stores meeting metadata

📊 Database Schema

meetings table:

id (PK)

event_id

subject

start_time

duration_minutes

join_url

organizer_email

created_at

🔐 Security

OAuth 2.0 Authorization Code Flow

Access tokens scoped:

Calendars.ReadWrite

OnlineMeetings.ReadWrite

User.Read

🚀 Run Locally (Docker)
docker compose up -d --build

Open:

http://localhost:8000/docs
📈 Future Enhancements

AI transcript summarization

Availability scoring engine

Meeting analytics dashboard

Observability & structured logging
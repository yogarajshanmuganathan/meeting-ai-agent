User
  ↓
FastAPI (Dockerized)
  ↓
Microsoft Identity Platform (OAuth 2.0)
  ↓
Microsoft Graph API
  ↓
Calendar Event Creation
  ↓
Teams Meeting Link Generation
  ↓
PostgreSQL (Dockerized Persistence)
  ↓
Structured Meeting Metadata Storage

Meeting AI Agent — Technical Overview

1. Authentication Layer
OAuth 2.0 Authorization Code Flow
Access token stored temporarily in memory
Scopes:
Calendars.ReadWrite

OnlineMeetings.ReadWrite

User.Read

2. Scheduling Layer

Accepts:

Subject

Start time

Duration

Attendees

Converts duration → end time

Calls Microsoft Graph /me/events

3. Teams Link Generation

Generates mock Teams URL

Injected into HTML body

4. Persistence Layer

PostgreSQL (Docker)

meetings table:

event_id

subject

start_time

duration_minutes

join_url

organizer_email

created_at

5. Deployment Layer

Docker Compose

Isolated DB service

App communicates using service name meeting_ai_db

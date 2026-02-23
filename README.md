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


## 🔄 Sequence Diagram

```mermaid
sequenceDiagram

    participant User
    participant FastAPI
    participant Identity as Microsoft Identity
    participant Graph as Microsoft Graph
    participant DB as PostgreSQL

    User->>FastAPI: /auth/login
    FastAPI->>Identity: Redirect (OAuth)
    Identity-->>FastAPI: Authorization Code
    FastAPI->>Identity: Exchange Code for Token
    Identity-->>FastAPI: Access Token

    User->>FastAPI: POST /meeting/book
    FastAPI->>Graph: Create Event (Bearer Token)
    Graph-->>FastAPI: Event Created
    FastAPI->>DB: Insert meeting metadata
    DB-->>FastAPI: Commit success
    FastAPI-->>User: Join URL + Event ID
```

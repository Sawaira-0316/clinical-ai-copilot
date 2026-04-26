# Backend

## Purpose
The backend provides the REST API for the Clinical AI Copilot, handling data processing, AI integration, and business logic.

## Responsibilities
- API endpoint management
- Data validation and processing
- Integration with AI engine
- Database operations
- Authentication and security

## Key Components
- `app/api/`: API routes and schemas
- `app/core/`: Configuration and utilities
- `app/db/`: Database models and repositories
- `app/services/`: Business logic services
- `tests/`: Unit and integration tests

## API Flow
Request → Route → Service → Repository → Database

## Tech Stack
- FastAPI
- PostgreSQL
- Pydantic for validation
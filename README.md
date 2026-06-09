# URL Shortener API

A URL shortening service built with FastAPI and SQLite. Converts long URLs into short, shareable links with optional custom slugs and expiry dates.


## Tech Stack

FastAPI, SQLAlchemy, SQLite, Alembic, Pydantic, Python 3.12


## Getting Started

Clone the repository and install dependencies using uv.

    uv sync

Create a .env file in the project root with the following variables.

    DATABASE_URL=sqlite:///./urlshortener.db
    SECRET_KEY=your_secret_key_here
    BASE_URL=http://localhost:8000

Run database migrations.

    uv run alembic upgrade head

Start the development server.

    uv run uvicorn main:app --reload

Visit http://localhost:8000/docs for the interactive API documentation.


## Endpoints

POST /shorten
Accepts a long URL and returns a shortened version. Optionally accepts a custom slug and expiry duration in days.

GET /{slug}
Redirects the user to the original URL associated with the given slug. Returns 404 if the slug does not exist or has expired.


## Project Structure

main.py is the entry point that registers all routers.
database.py sets up the SQLAlchemy engine and session factory.
models.py defines the database tables.
deps.py provides the database session dependency.
schemas/url.py contains Pydantic models for request and response validation.
services/url.py contains the core business logic including slug generation and redirect resolution.
routers/urls.py defines the HTTP endpoints.
migrations/ contains Alembic migration files.


## Notes

Slugs are generated using Base62 encoding of the auto incremented database ID, XORed with a secret key to prevent enumeration.
The database file urlshortener.db and the .env file are excluded from version control.

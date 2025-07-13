# HBnB Evolution API (Part 2)

HBnB Evolution is a lightweight Flask REST API modeling a simplified AirBnB-like application. This folder contains the second phase of the project where the API layer, business logic and a minimal in-memory persistence layer are implemented.

## Architecture

The code follows a layered design inspired by clean architecture principles:

- **Presentation layer**: Flask-RESTX namespaces define the HTTP endpoints under `app/api/v1`. They validate incoming requests and marshal responses.
- **Business logic layer**: `app/services/facade.py` centralizes operations for users, places, amenities and reviews. Each method performs validation before delegating to the repositories.
- **Persistence layer**: `app/persistence/repository.py` provides an in-memory repository used by the facade. It can be swapped out for a real database in the future.
- **Domain models**: Located in `app/models`, these classes (`User`, `Place`, `Amenity`, `Review`) extend `BaseModel` and include basic validation logic.

The application is initialized in `app/__init__.py` where the API namespaces are registered. `run.py` simply creates the app and starts the development server.

## Endpoints

The API exposes CRUD-style routes for each entity. Examples:

- `POST /api/v1/users/` – create a new user
- `POST /api/v1/places/` – create a place owned by a user
- `POST /api/v1/reviews/` – attach a review to a place

Each namespace also supports retrieving and updating individual resources. Swagger documentation is automatically generated and available at `/api/v1/` when the server is running.

## Setup

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Start the server:

```bash
python run.py
```

The API will listen on `http://127.0.0.1:5000`.

### Default administrator

`run.py` seeds a default admin account the first time it executes.  Set the
`ADMIN_EMAIL` and `ADMIN_PASSWORD` environment variables to control the
credentials, otherwise `admin@example.com`/`admin` are used.  Log in with these
details to obtain a token for the admin-only endpoints.

## Running Tests

Unit tests live in the `tests` directory and cover the user, place and review endpoints. Run them with:

```bash
python -m unittest discover -s tests
```

## Design Notes

- **Validation** – Models enforce simple constraints (e.g. user fields cannot be empty, latitude/longitude ranges). The facade raises `ValueError` when validation fails so the API can return a `400 Bad Request`.
- **In-memory storage** – Repositories keep objects in dictionaries. This makes the service self-contained and easy to test without a database.
- **Facade pattern** – The API only interacts with the `HBnBFacade` which orchestrates persistence and validation. This keeps the controllers thin and makes the codebase easier to evolve.

## Conclusion
Part 2 serves as a proof of concept for a clean architecture approach while remaining small enough to not overwhelm beginner devs.

## Administrator Endpoints

A JWT token contains an `is_admin` claim. Endpoints that create or update users and amenities require this flag to be true. Administrators can also modify or delete any place or review, bypassing the normal ownership checks.


# HBnB Evolution API (Part 3)

HBnB Evolution continues the gradual design of a small AirBnB clone. Part 3 replaces the in-memory storage used in previous versions with a proper relational database powered by SQLAlchemy. The goal is to keep the code simple while demonstrating how to structure a Flask project with clear separation between the API, business logic and persistence layers.

## Project Structure

```
part3/
├── app/                # Flask application package
│   ├── api/            # Flask‑RESTX namespaces
│   ├── models/         # SQLAlchemy models (User, Place, Amenity, Review)
│   ├── persistence/    # Repository implementations
│   └── services/       # High level facade used by the API
├── sql/                # SQL schema and seed data
├── config.py           # Application configuration classes
├── run.py              # Entry point to launch the API
└── tests/              # Unit tests for the endpoints
```

### Key Components

- **Flask‑RESTX** provides the REST interface and automatically documents the API.
- **SQLAlchemy** handles database interactions. By default the app uses a SQLite database created in `development.db`.
- **JWT Authentication** is used for login and for protecting certain routes. A default administrator account is seeded when the app first runs.
- **Repository Pattern** abstracts persistence. `SQLAlchemyRepository` writes to the database while `InMemoryRepository` is kept for testing purposes.

## Database Schema
All tables are defined in `sql/create_tables.sql`. The script creates the following tables with relationships:
- `users` – account information and admin flag
- `places` – lodging entries owned by a user
- `amenities` – available amenities
- `reviews` – user reviews of places
- `place_amenities` – many‑to‑many join table

The schema can be visualized using the ER diagram in `sql/er-diagram.mmd`. To seed the database with an administrator and some sample amenities, run `sql/initial_data.sql`.

```
sqlite3 development.db < sql/create_tables.sql
sqlite3 development.db < sql/initial_data.sql
```

## Running the Application

1. **Install dependencies**

```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

2. Start the server:

```bash
   python run.py
   ```

The API will be available at `http://127.0.0.1:5000` and the Swagger UI is served at `/api/v1/

Environment variables `ADMIN_EMAIL` and `ADMIN_PASSWORD` may be used to customize the credentials of the initial administrator.

## Example Endpoints

- `POST /api/v1/login` – obtain a JWT token
- `POST /api/v1/users/` – register a user
- `GET  /api/v1/places/` – list all places
- `POST /api/v1/places/` – create a place (authentication required)
- `POST /api/v1/reviews/` – add a review for a place

Every entity also supports retrieving, updating and deleting specific records. Endpoints that modify users or amenities require an administrator token.

## Running Tests

Unit tests are located in the `tests` directory. They use the in‑memory repositories to keep the suite fast and independent of the database.

```bash
python -m unittest discover -s tests
```

## Notes on Design

- **Validation** is performed in the model constructors and in the facade to keep the API layer thin.
- **Facade Pattern** – `app/services/facade.py` is the single entry point used by the routes. It coordinates repositories and applies business rules.
- **Swappable Storage** – Although the app ships with a SQLAlchemy backend, the repository pattern makes it trivial to replace it with another data store if desired.

## Additional Resources
The `sql/` folder contains a more detailed walkthrough of the database setup along with instructions for verifying the schema using the SQLite CLI. Consult `sql/README.md` for more information.

---
This marks the third milestone of the HBnB project, demonstrating how to persist the application's data in a real database while maintaining a clean and testable architecture.

# HBnB SQL Scripts

This folder contains SQL files for generating the database schema used in the HBnB project (part 3) and seeding it with initial data.

- **`create_tables.sql`** – Creates all tables and relationships.
- **`initial_data.sql`** – Inserts a default administrator account and some amenities.

These scripts are written for SQLite but avoid engine-specific syntax so they can be adapted to other relational databases.

## ER Diagram

The schema defined in `create_tables.sql` is summarized below.

```mermaid
erDiagram
    users {
        CHAR(36) id PK
        VARCHAR first_name
        VARCHAR last_name
        VARCHAR email
        VARCHAR password
        BOOLEAN is_admin
    }
    places {
        CHAR(36) id PK
        VARCHAR title
        TEXT description
        DECIMAL price
        FLOAT latitude
        FLOAT longitude
        CHAR(36) owner_id FK
    }
    reviews {
        CHAR(36) id PK
        TEXT text
        INTEGER rating
        CHAR(36) user_id FK
        CHAR(36) place_id FK
    }
    amenities {
        CHAR(36) id PK
        VARCHAR name
    }
    place_amenities {
        CHAR(36) place_id PK FK
        CHAR(36) amenity_id PK FK
    }

    users ||--o{ places : owns
    users ||--o{ reviews : writes
    places ||--o{ reviews : receives
    places ||--o{ place_amenities : has
    amenities ||--o{ place_amenities : listed_in

```

## Running the Scripts

```
sqlite3 /tmp/hbnb.db < create_tables.sql
sqlite3 /tmp/hbnb.db < initial_data.sql
```

- `create_tables.sql` must be executed first. It turns on foreign key enforcement and defines the tables.
- `initial_data.sql` populates the administrator user and amenities. The administrator's password is stored in bcrypt format.

## Verifying Table Creation

After running the schema script, check that each table exists with the expected columns and constraints:

```
sqlite3 /tmp/hbnb.db ".schema users"
sqlite3 /tmp/hbnb.db ".schema places"
sqlite3 /tmp/hbnb.db ".schema reviews"
sqlite3 /tmp/hbnb.db ".schema amenities"
sqlite3 /tmp/hbnb.db ".schema place_amenities"
```

You should see primary keys, foreign keys and the composite key on `place_amenities`.

## Verifying Initial Data

Ensure the admin row and amenities were inserted correctly:

```
sqlite3 /tmp/hbnb.db "SELECT id, email, is_admin FROM users;"
sqlite3 /tmp/hbnb.db "SELECT name FROM amenities;"
```

The admin entry should have `is_admin` set to `1` and the password value will be a bcrypt hash.

## Testing CRUD Operations

Use standard SQL statements to confirm data integrity.

1. **Insert** a new user and place. Link them via a review and some amenities.
2. **Select** rows back to ensure the foreign key relationships are valid.
3. **Update** one of the rows (e.g. change the place price) and check the change.
4. **Delete** the rows and verify that deletes cascade or fail as expected.

Example:

```
-- add a user
INSERT INTO users(id, first_name, last_name, email, password)
VALUES('11111111-1111-1111-1111-111111111111', 'Jane', 'Doe', 'jane@example.com', 'pwd');

-- create a place owned by that user
INSERT INTO places(id, title, description, price, latitude, longitude, owner_id)
VALUES('22222222-2222-2222-2222-222222222222', 'Cozy House', '', 100, 40.0, -70.0, '11111111-1111-1111-1111-111111111111');

-- clean up
DELETE FROM places WHERE id='22222222-2222-2222-2222-222222222222';
DELETE FROM users WHERE id='11111111-1111-1111-1111-111111111111';
```

These steps demonstrate that inserts, updates and deletions behave correctly against the schema.

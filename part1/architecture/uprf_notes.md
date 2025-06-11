# Sequence Diagrams

## 1. User Registration
- **Description**: Diagram for registering a new user account.
- **Flow**:
  1. User sends a POST request to `/users/register`.
  2. API layer calls `registerUser` in the business logic.
  3. Business logic validates input, hashes password, and persists to the database.
  4. Database returns the created user record.
  5. Business logic returns a `UserDTO`.
  6. API responds with `201 Created`.

## 2. Place Creation
- **Description**: Diagram for creating a new place listing.
- **Flow**:
  1. User sends a POST request to `/places`.
  2. API layer calls `createPlace` with the user ID and place data.
  3. Business logic authorizes the user, validates data, and persists a new place.
  4. Database returns the created place record.
  5. Business logic returns a `PlaceDTO`.
  6. API responds with `201 Created`.

## 3. Review Submission
- **Description**: Diagram for submitting a review for a place.
- **Flow**:
  1. User sends a POST request to `/places/{placeId}/reviews`.
  2. API layer calls `submitReview`.
  3. Business logic validates rating, checks existence, inserts review, and updates the place’s rating.
  4. Database returns confirmation for both insert and update.
  5. Business logic returns a `ReviewDTO`.
  6. API responds with `201 Created`.

## 4. Fetching a List of Places
- **Description**: Diagram for fetching a filtered list of places.
- **Flow**:
  1. User sends a GET request to `/places` with query parameters.
  2. API layer calls `listPlaces`.
  3. Business logic queries the database for matching places and related amenities.
  4. Database returns place and amenity records.
  5. Business logic assembles `PlaceDTO`s.
  6. API responds with `200 OK` and the list of places.


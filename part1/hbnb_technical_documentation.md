# HBnB Evolution: Technical Documentation

## Introduction

The HBnB Evolution application is a simplified AirBnB‑style platform enabling users to register, list properties, leave reviews, and manage amenities. This document consolidates the architectural and design artifacts needed to guide development, including:

- **High‑Level Architecture**: Layered package diagram illustrating the Presentation, Business Logic, and Persistence layers and their interactions via the facade pattern.
- **Business Logic Layer**: Detailed class diagram of core entities (`User`, `Place`, `Review`, `Amenity`), showing attributes, methods, and relationships.
- **API Interaction Flow**: Sequence diagrams for four key API calls (User Registration, Place Creation, Review Submission, Fetching a List of Places), detailing interactions across layers.

Each section contains the Mermaid.js diagram source and explanatory notes to clarify design decisions and data flows.

---

## High‑Level Architecture

### Package Diagram

```mermaid
graph LR
  subgraph Presentation Layer
    PL["Service API<br/>(HTTP Controllers, DTOs)"]
  end
  subgraph Business Logic Layer
    BLF["HBnBFacade <<interface>>"]
    UM["User, Place, Review, Amenity<br/>Models & Services"]
  end
  subgraph Persistence Layer
    PR["Repositories / DAOs<br/>(UserRepo, PlaceRepo, ReviewRepo, AmenityRepo)"]
  end

  PL -->|uses| BLF
  BLF -->|delegates business logic| UM
  UM -->|reads & writes data| PR

```

### Explanatory Notes

- **Presentation Layer**: Exposes HTTP endpoints (controllers) and DTOs for input validation and response shaping. Depends on `HBnBFacade` to invoke business logic.
- **Business Logic Layer**: Contains the `HBnBFacade` interface, domain models, and services implementing core workflows (e.g., user registration, place validation).
- **Persistence Layer**: Houses repositories/DAOs abstracting database operations (CRUD) for each entity. Returns raw data to the business layer.
- **Facade Pattern**: Simplifies controller interactions by providing a single entry point (`HBnBFacade`) to orchestrate use cases, enabling loose coupling and easier maintenance.

---

## Business Logic Layer

### Class Diagram

```mermaid
classDiagram
    class User {
        +UUID id
        +String firstName
        +String lastName
        +String email
        +String passwordHash
        +Boolean isAdmin
        +Date createdAt
        +Date updatedAt
        +create()
        +updateProfile()
        +deleteAccount()
    }
    class Place {
        +UUID id
        +String title
        +String description
        +Decimal pricePerNight
        +Float latitude
        +Float longitude
        +Date createdAt
        +Date updatedAt
        +create()
        +updateDetails()
        +deleteListing()
    }
    class Review {
        +UUID id
        +Integer rating
        +String comment
        +Date createdAt
        +Date updatedAt
        +create()
        +updateComment()
        +deleteReview()
    }
    class Amenity {
        +UUID id
        +String name
        +String description
        +Date createdAt
        +Date updatedAt
        +create()
        +updateDetails()
        +deleteAmenity()
    }

    User "1" -- "0..*" Place       : owns
    User "1" -- "0..*" Review      : writes
    Place "1" -- "0..*" Review     : hasReviews
    Place "1" -- "0..*" Amenity    : offersAmenities
    Review "1" --> "1" Place       : forPlace
    Review "1" --> "1" User        : byUser

```

### Explanatory Notes

- **Entities**:
    - **User**: Represents registered users (regular or admin) with profile attributes and account methods.
    - **Place**: Property listings with location, pricing, and lifecycle methods.
    - **Review**: User feedback tied to a place, including rating and comment lifecycle.
    - **Amenity**: Reusable service or feature attached to places.
- **Relationships**:
    - A `User` owns multiple `Places` and writes multiple `Reviews`.
    - A `Place` has many `Reviews` and can offer many `Amenities`.
    - Each `Review` is associated with one `User` (author) and one `Place` (target).

---

## API Interaction Flow

### 1. User Registration

```mermaid
sequenceDiagram
    participant User
    participant API as Presentation Layer
    participant BL as Business Logic Layer
    participant DB as Persistence Layer

    User->>API: POST /users/register {firstName, lastName, email, password}
    API->>BL: registerUser(data)
    BL->>BL: validate data, hash password
    BL->>DB: INSERT INTO users (...)
    DB-->>BL: new user record (with id, timestamps)
    BL-->>API: UserDTO {id, firstName, lastName, email}
    API-->>User: 201 Created {user info}

```

**Notes**: Validates inputs and securely hashes passwords in the business layer before persisting.

### 2. Place Creation

```mermaid
sequenceDiagram
    participant User
    participant API as Presentation Layer
    participant BL as Business Logic Layer
    participant DB as Persistence Layer

    User->>API: POST /places {title, description, pricePerNight, lat, lng}
    API->>BL: createPlace(userId, placeData)
    BL->>BL: authorize owner, validate data
    BL->>DB: INSERT INTO places (...)
    DB-->>BL: new place record (with id, timestamps)
    BL-->>API: PlaceDTO {id, title, pricePerNight, ownerId}
    API-->>User: 201 Created {place info}

```

**Notes**: Ensures only authorized users can create listings and enforces data constraints.

### 3. Review Submission

```mermaid
sequenceDiagram
    participant User
    participant API as Presentation Layer
    participant BL as Business Logic Layer
    participant DB as Persistence Layer

    User->>API: POST /places/{placeId}/reviews {rating, comment}
    API->>BL: submitReview(userId, placeId, reviewData)
    BL->>BL: validate rating bounds, verify user/place exist
    BL->>DB: INSERT INTO reviews (...)
    DB-->>BL: new review record (with id, timestamps)
    BL->>DB: UPDATE places SET avgRating = ... WHERE id=placeId
    DB-->>BL: confirmation
    BL-->>API: ReviewDTO {id, rating, comment}
    API-->>User: 201 Created {review info}

```

**Notes**: Maintains review integrity and updates aggregated ratings atomically.

### 4. Fetching a List of Places

```mermaid
sequenceDiagram
    participant User
    participant API as Presentation Layer
    participant BL as Business Logic Layer
    participant DB as Persistence Layer

    User->>API: GET /places?filters...
    API->>BL: listPlaces(filters)
    BL->>DB: SELECT * FROM places WHERE ...
    DB-->>BL: [place records]
    BL->>DB: SELECT * FROM amenities WHERE place_id IN (...)
    DB-->>BL: [amenity records]
    BL->>BL: assemble PlaceDTOs with amenities
    BL-->>API: [PlaceDTO, …]
    API-->>User: 200 OK {places list}

```

**Notes**: Batches database queries for efficiency and composes full DTOs in business logic.

---

## Conclusion

This document unifies the architectural vision and detailed design of HBnB Evolution, from high‑level layering to low‑level interactions. It will serve as the definitive reference during implementation, ensuring consistency, clarity, and adherence to core design principles.


# Detailed Class Diagram

## User
- **Role**: Registered person (regular or admin)  
- **Attributes**:  
  - `id` (UUID4), `firstName`, `lastName`, `email`, `passwordHash`, `isAdmin`  
  - `createdAt`, `updatedAt`  
- **Methods**:  
  - `create()`, `updateProfile()`, `deleteAccount()`

## Place
- **Role**: Property listing owned by a user  
- **Attributes**:  
  - `id` (UUID4), `title`, `description`  
  - `pricePerNight`, `latitude`, `longitude`  
  - `createdAt`, `updatedAt`  
- **Methods**:  
  - `create()`, `updateDetails()`, `deleteListing()`

## Review
- **Role**: Feedback from a user on a place  
- **Attributes**:  
  - `id` (UUID4), `rating`, `comment`  
  - `createdAt`, `updatedAt`  
- **Methods**:  
  - `create()`, `updateComment()`, `deleteReview()`

## Amenity
- **Role**: Feature or service attachable to places  
- **Attributes**:  
  - `id` (UUID4), `name`, `description`  
  - `createdAt`, `updatedAt`  
- **Methods**:  
  - `create()`, `updateDetails()`, `deleteAmenity()`

## Relationships
- **User–Place (`owns`)**: 1 user → 0..* places  
- **User–Review (`writes`)**: 1 user → 0..* reviews  
- **Place–Review (`hasReviews`)**: 1 place → 0..* reviews  
- **Place–Amenity (`offersAmenities`)**: 1 place → 0..* amenities  
- **Review→Place (`forPlace`)**: each review → exactly 1 place  
- **Review→User (`byUser`)**: each review → exactly 1 user  


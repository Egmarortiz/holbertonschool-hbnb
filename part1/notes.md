# High-Level Package Diagram

## Presentation Layer  
- **Responsibility**: Exposes functionality via HTTP/gRPC  
- **Components**:
  - Controllers / Handlers
  - DTOs / View Models

## Business Logic Layer  
- **Responsibility**: Core rules & workflows  
- **Components**:
  - Facade Interface (`HBnBFacade`)
  - Domain Models & Services (`User`, `Place`, `Review`, `Amenity`)

## Persistence Layer  
- **Responsibility**: DB interactions  
- **Components**:
  - Repositories / DAOs
  - ORM / Data Mappers

## Facade Pattern  
- **Purpose**: Simplify & decouple Presentation → Business Logic  
- **Benefits**:
  1. Controllers depend on one interface.  
  2. Shields controllers from changes in domain logic.  
  3. Encapsulates multi-step workflows.


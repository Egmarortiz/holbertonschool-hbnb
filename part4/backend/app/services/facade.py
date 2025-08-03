from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.services.repositories import (
        UserRepository,
        AmenityRepository,
        PlaceRepository,
        ReviewRepository,
        )

class HBnBFacade:
    def __init__(self):
        """Initialize repositories using SQLAlchemy."""
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    def create_user(self, user_data):
        """Create new usr and store in the repo."""
        password = user_data.get('password')

        if not password:
            raise ValueError("Password cannot be empty")

        user = User(
                first_name=user_data.get('first_name', ''),
                last_name=user_data.get('last_name', ''),
                email=user_data.get('email', ''),
                is_admin=user_data.get('is_admin', False)
                )

        user.hash_password(password)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a usr by id."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Find usr by email."""
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's information."""
        user = self.user_repo.get(user_id)
        if user:
            data = user_data.copy()
            if 'password' in data and data['password']:
                user.hash_password(data.pop('password'))
            self.user_repo.update(user_id, user_data)
            return user
        return None

    def create_amenity(self, amenity_data):
        """Create a new amenity and store in the repository."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        if 'name' in amenity_data:
            amenity.name = amenity_data['name']
        amenity.save()
        return amenity

    def create_place(self, place_data):
        """Create a new place and store in the repository."""
        # Validate owner exists
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")
        # Validate amenities exist
        amenities = []
        for amenity_id in place_data.get('amenities', []):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} not found")
            amenities.append(amenity)
        # Create place with name instead of title to match model
        place = Place(
                name=place_data['title'],  # Map title to name
                description=place_data.get('description', ''),
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner=owner
                )
        # Add amenities
        for amenity in amenities:
            place.add_amenity(amenity)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID, including associated owner and amenities."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        pass

    def update_place(self, place_id, place_data):
        """Update a place's information."""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        # Validate owner if provided
        if 'owner_id' in place_data:
            owner = self.user_repo.get(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
            place.owner = owner
        # Validate amenities if provided
        if 'amenities' in place_data:
            amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity {amenity_id} not found")
                amenities.append(amenity)
            place.amenities = amenities
        # Update other fields
        if 'title' in place_data:
            place.name = place_data['title']  # Map title to name
        if 'description' in place_data:
            place.description = place_data['description']
        if 'price' in place_data:
            place.price = place_data['price']
        if 'latitude' in place_data:
            place.latitude = place_data['latitude']
        if 'longitude' in place_data:
            place.longitude = place_data['longitude']
        # Update the place in the repository
        self.place_repo.update(place_id, place_data)
        return place

    def create_review(self, review_data):
        """Create a new review and store in the repository."""
        # Validate user exists
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise ValueError("User not found")

        # Validate place exists
        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")

        # Validate rating is between 1 and 5
        rating = review_data.get('rating')
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")

        # Create review (map 'text' to 'comment' to match model)
        review = Review(
                user=user,
                place=place,
                rating=rating,
                comment=review_data.get('text', '')
                )

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        pass

    def update_review(self, review_id, review_data):
        """Update a review's information."""
        review = self.review_repo.get(review_id)
        if not review:
            return None

        # Validate user if provided
        if 'user_id' in review_data:
            user = self.user_repo.get(review_data['user_id'])
            if not user:
                raise ValueError("User not found")
            review.user = user

        # Validate place if provided
        if 'place_id' in review_data:
            place = self.place_repo.get(review_data['place_id'])
            if not place:
                raise ValueError("Place not found")
            review.place = place

        # Validate rating if provided
        if 'rating' in review_data:
            rating = review_data['rating']
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                raise ValueError("Rating must be an integer between 1 and 5")
            review.rating = rating

        # Update text if provided
        if 'text' in review_data:
            review.text = review_data['text']

        # Save changes (updates the updated_at timestamp)
        review.save()

        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review_id)
            return True
        return False

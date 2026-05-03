# ... əvvəlki user metodlarının altından davam et ...

    def create_amenity(self, amenity_data):
        from app.models.amenity import Amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        # Repository-dəki update metodunu çağırırıq
        return self.amenity_repo.update(amenity_id, amenity_data)
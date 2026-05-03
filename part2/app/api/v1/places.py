from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude for location'),
    'longitude': fields.Float(required=True, description='Longitude for location'),
    'owner_id': fields.String(required=True, description='ID of the owner (user)'),
    'amenities': fields.List(fields.String, description="List of amenity IDs")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    def post(self):
        """Create a new place"""
        place_data = api.payload
        try:
            new_place = facade.create_place(place_data)
            return {'id': new_place.id, 'title': new_place.title}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [{'id': p.id, 'title': p.title, 'price': p.price} for p in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'owner': {'id': place.owner.id, 'first_name': place.owner.first_name},
            'amenities': [{'id': a.id, 'name': a.name} for a in place.amenities]
        }, 200
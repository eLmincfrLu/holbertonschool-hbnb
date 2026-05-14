from flask_restx import Namespace, Resource, fields
from app import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String(),
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True)
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    def post(self):
        try:
            new_place = facade.create_place(api.payload)
            return {'id': new_place.id, 'title': new_place.title}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        places = facade.get_all_places()
        return [{'id': p.id, 'title': p.title, 'latitude': p.latitude, 'longitude': p.longitude} for p in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        p = facade.get_place(place_id)
        if not p: return {'error': 'Place not found'}, 404
        return {
            'id': p.id, 'title': p.title, 'description': p.description,
            'price': p.price, 'latitude': p.latitude, 'longitude': p.longitude,
            'owner': {'id': p.owner.id, 'first_name': p.owner.first_name, 'last_name': p.owner.last_name}
        }, 200

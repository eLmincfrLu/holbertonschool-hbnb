from flask_restx import Namespace, Resource, fields
from app import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    def post(self):
        new_amenity = facade.create_amenity(api.payload)
        return {'id': new_amenity.id, 'name': new_amenity.name}, 201

    def get(self):
        amenities = facade.get_all_amenities()
        return [{'id': a.id, 'name': a.name} for a in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity: return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model, validate=True)
    def put(self, amenity_id):
        updated = facade.update_amenity(amenity_id, api.payload)
        if not updated: return {'error': 'Amenity not found'}, 404
        return {'message': 'Amenity updated successfully'}, 200

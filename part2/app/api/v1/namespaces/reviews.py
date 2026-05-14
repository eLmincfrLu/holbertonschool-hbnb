from flask_restx import Namespace, Resource, fields
from app import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True, min=1, max=5),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True)
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    def post(self):
        try:
            new_review = facade.create_review(api.payload)
            return {'id': new_review.id, 'text': new_review.text}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

@api.route('/<review_id>')
class ReviewResource(Resource):
    def delete(self, review_id):
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<place_id>')
class PlaceReviewList(Resource):
    def get(self, place_id):
        reviews = facade.get_reviews_by_place(place_id)
        return [{'id': r.id, 'text': r.text, 'rating': r.rating} for r in reviews], 200

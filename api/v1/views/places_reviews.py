#!/usr/bin/python3
""" Customized Place Reviews view """
from api.v1.views import app_views
from flask import jsonify, Blueprint, abort, request
from models import storage
from models.place import Place
from models.review import Review as CustomReview


@app_views.route('/places/<custom_place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_all_custom_place_reviews(custom_place_id):
    """ Retrieves the list of reviews of a specific place"""
    custom_reviews_list = []
    place = storage.get('Place', custom_place_id)
    if not place:
        abort(404)
    for custom_review in storage.all("Review").values():
        if custom_place_id == custom_review.place_id:
            custom_reviews_list.append(custom_review.to_dict())
    return jsonify(custom_reviews_list)


@app_views.route('/reviews/<custom_review_id>', methods=['GET', 'DELETE'])
def get_custom_review_by_id(custom_review_id):
    """ Retrieves a review object """
    for obj in storage.all("Review").values():
        if obj.id == custom_review_id:
            if request.method == 'GET':
                return jsonify(obj.to_dict())
            if request.method == 'DELETE':
                storage.delete(obj)
                storage.save()
                return jsonify({}), 200
    abort(404)


@app_views.route('/places/<custom_place_id>/reviews', methods=['POST'])
def post_new_custom_place_review(custom_place_id):
    """ Add new review to a specific place """
    place = storage.get('Place', custom_place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")
    user = storage.get('User', request.get_json()['user_id'])
    if not user:
        abort(404)

    if "text" not in request.get_json():
        abort(400, "Missing text")
    request.get_json()['place_id'] = custom_place_id
    custom_review = CustomReview(**request.get_json())
    custom_review.save()
    return jsonify(custom_review.to_dict()), 201


@app_views.route('/reviews/<custom_review_id>', methods=['PUT'])
def update_custom_review_by_id(custom_review_id):
    """ Update a review with its id """
    if not request.get_json():
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'place_id', 'created_at', 'updated_at', 'user_id']
    for custom_review in storage.all("Review").values():
        if custom_review.id == custom_review_id:
            for key, value in request.get_json().items():
                if key not in ignored_keys:
                    setattr(custom_review, key, value)
            custom_review.save()
            return jsonify(custom_review.to_dict())
    abort(404)

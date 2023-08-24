# API test

from flask import current_app, request, url_for, jsonify, Blueprint
from flask_login import login_required
import os, json
from functions import *

api_bp = Blueprint("api", __name__)

class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@api_bp.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code

# Main call on API
@api_bp.route("/", methods=['POST','GET'])
def main():
    return "", 200


# Animal API
@api_bp.route("/animals", methods=['GET'])
@api_bp.route("/animals/<int:id>", methods=['GET'])
def animals(id=None):
    if id:
        animals = get_ad(id)
    else:
        animals = get_ad()
    return jsonify(animals), 200

@api_bp.route("/animals/<int:id>/feedings", methods=['GET'])
@api_bp.route("/animals/<int:id>/feedings/<string:argument>", methods=['GET'])
def animal_feedings(id, argument=None):
    if argument == "last":
        return jsonify(get_fd("", id, 1))
    else:
        return jsonify(get_fd("", id))

@api_bp.route("/animals/<int:id>/history", methods=['GET'])
@api_bp.route("/animals/<int:id>/history/<int:e_type>", methods=['GET'])
def animal_history(id, e_type=None):
    if type:
        return jsonify(get_hd("", id, 10, e_type))
    else:
        return jsonify(get_hd("", id))
    

# Feeding type
@api_bp.route("/feeding_types", methods=['GET'])
def get_feeding_types():
    raise InvalidAPIUsage("Not implemented!", 404)
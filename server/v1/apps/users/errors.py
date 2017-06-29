from . import users
from flask import make_response, jsonify, abort

@users.errorhandler(404)
def not_found(error):
    message = 'Not found'
    code = 404
    return make_response(jsonify({'error': message}), code)

@users.errorhandler(401)
def unauthorized(error):
    message = 'Unauthorized access'
    code = 401
    return make_response(jsonify({'error': message}), code)

@users.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

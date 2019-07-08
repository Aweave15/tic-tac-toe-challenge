from flask_restful import Resource
from flask import jsonify


class HealthHandler(Resource):

    methods = ['GET']

    def get(self):
        return jsonify({'status': 'OK'})

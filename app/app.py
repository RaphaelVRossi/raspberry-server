import json

from bson import ObjectId
from bson.json_util import dumps
from flask import Flask, jsonify, request
from flask_cors import CORS
from healthcheck import HealthCheck
from pymongo import MongoClient

# Initialize Flask Application
application = Flask(__name__)
CORS(application)

health = HealthCheck()

mongo_client = MongoClient('mongodb://admin:JHm7rgBJbTR2@rrossi.ddns.net:27017')
session_db = mongo_client.session
session_collection = session_db.session_collection


@application.route('/session', methods=['POST', 'PUT', 'PATCH'])
def post_session():
    body = request.json

    print(f"Request Body {body}")

    print_headers(request)

    obj = None

    if '_id' in body:
        obj = session_collection.find_one({'_id': body['_id']})

    if obj is None:
        obj = body
        print(f"Object is new, creating obj {obj}")
        session_collection.insert_one(json.loads(json.dumps(obj)))
    else:
        print(f"Object exists, updating obj {obj}")
        session_collection.update_one({'_id': obj['_id']}, {'$set': json.loads(json.dumps(obj))})

    return jsonify(obj)


@application.route('/session', methods=['GET'])
def get_session():
    print_headers(request)

    session_cursor = session_collection.find()

    session_array = json.loads(dumps(session_cursor))

    session_len = len(session_array)

    print(f"Found [{session_len}] sessions")

    return {"length": session_len, "data": session_array}


@application.route('/session/<id>', methods=['DELETE'])
def delete_session(id):
    print(f'Deleting obj')
    print_headers(request)

    session_collection.delete_one({"_id": ObjectId(id)})

    return {}


@application.route('/', methods=['GET'])
def get_hello_world():
    return {
        "status": "OK",
        "message": "Hello World!"
    }


def print_headers(request_value):
    for header in request_value.headers:
        print(f"Header Found [{header}]")


application.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8080)

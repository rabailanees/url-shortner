from flask import Blueprint, request, jsonify
from app.models import URL
from app import db
from bson import json_util
import json

api_bp = Blueprint('api', __name__)
url_model = URL(db)

def parse_json(data):
    return json.loads(json_util.dumps(data))

@api_bp.route('/shorten', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing URL"}), 400
    
    try:
        new_url = url_model.create(data['url'])
        return jsonify(parse_json({
            "id": str(new_url["_id"]),
            "originalUrl": new_url["originalUrl"],
            "shortCode": new_url["shortCode"],
            "createdAt": new_url["createdAt"],
            "updatedAt": new_url["updatedAt"],
            "accessCount": new_url["accessCount"]
        })), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/shorten/<short_code>', methods=['GET'])
def get_url(short_code):
    url = url_model.find_by_short_code(short_code)
    if not url:
        return jsonify({"error": "URL not found"}), 404
    return jsonify(parse_json(url)), 200

@api_bp.route('/shorten/<short_code>', methods=['PUT'])
def update_url(short_code):
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing URL"}), 400
    
    result = url_model.update_url(short_code, data['url'])
    if result.modified_count == 0:
        return jsonify({"error": "URL not found"}), 404
    
    updated_url = url_model.find_by_short_code(short_code)
    return jsonify(parse_json(updated_url)), 200

@api_bp.route('/shorten/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    result = url_model.delete_url(short_code)
    if result.deleted_count == 0:
        return jsonify({"error": "URL not found"}), 404
    return '', 204

@api_bp.route('/shorten/<short_code>/stats', methods=['GET'])
def get_stats(short_code):
    url = url_model.find_by_short_code(short_code)
    if not url:
        return jsonify({"error": "URL not found"}), 404
    
    response = jsonify({
        "shortCode": url["shortCode"],
        "originalUrl": url["originalUrl"],
        "accessCount": url["accessCount"],
        "createdAt": url["createdAt"],
        "lastAccessed": url["updatedAt"]
    })
    
    # Add no-cache headers
    response.headers['Cache-Control'] = 'no-store, max-age=0'
    return response, 200

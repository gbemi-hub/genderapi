from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/classify', methods=['GET'])
def classify():
    name = request.args.get('name')
    
    if not name:
        return jsonify({
            'status': 'error',
            'message': 'Name parameter is required'
        }), 400
    
    if not isinstance(name, str):
        return jsonify({
            'status': 'error',
            'message': 'Name parameter must be a string'
        }), 422
    
    try:
        response = requests.get(f'http://api.genderize.io/?name={name}')
        data = response.json()
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Cannot reach Genderize API'
        }), 502
    
    if data.get('gender') is None or data.get('count') == 0:
        return jsonify({
            'status': 'error',
            'message': 'No prediction available for the provided name'
        })
    
    is_confident = (data['probability'] >= 0.7 and data['count'] >= 100)
    processed_at = datetime.utcnow().isoformat() + 'Z'
    
    return jsonify({
        'status': 'success',
        'data': {
            'name': name,
            'gender': data['gender'],
            'probability': data['probability'],
            'sample_size': data['count'],
            'is_confident': is_confident,
            'processed_at': processed_at
        }
    })

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Gender API is running',
        'endpoint': '/api/classify?name=john'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
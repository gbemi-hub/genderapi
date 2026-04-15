from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime

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
    
    try:
        response = requests.get(f'http://api.genderize.io/?name={name}')
        data = response.json()
    except:
        return jsonify({
            'status': 'error',
            'message': 'Cannot reach Genderize API'
        }), 502
    
    if data.get('gender') is None:
        return jsonify({
            'status': 'error',
            'message': 'No prediction available for the provided name'
        })
    
    is_confident = (data['probability'] >= 0.7 and data['count'] >= 100)
    now = datetime.utcnow().isoformat() + 'Z'
    
    return jsonify({
        'status': 'success',
        'data': {
            'name': name,
            'gender': data['gender'],
            'probability': data['probability'],
            'sample_size': data['count'],
            'is_confident': is_confident,
            'processed_at': now
        }
    })

if __name__ == '__main__':
    app.run(port=3000)
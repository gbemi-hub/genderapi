from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime
import uuid
import database

app = Flask(__name__)
CORS(app)

# Initialize database on startup
database.init_db()

def get_age_group(age):
    if age <= 12:
        return 'child'
    elif age <= 19:
        return 'teenager'
    elif age <= 59:
        return 'adult'
    else:
        return 'senior'

@app.route('/api/profiles', methods=['POST'])
def create_profile():
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'status': 'error', 'message': 'Missing or empty name'}), 400
    
    name = data['name'].strip()
    
    if not isinstance(name, str):
        return jsonify({'status': 'error', 'message': 'Invalid type'}), 422
    
    # Check if profile already exists
    existing = database.get_profile_by_name(name)
    if existing:
        return jsonify({
            'status': 'success',
            'message': 'Profile already exists',
            'data': dict(existing)
        }), 200
    
    # Call all three APIs
    try:
        gender_response = requests.get(f'https://api.genderize.io/?name={name}')
        gender_data = gender_response.json()
        
        if not gender_data.get('gender') or gender_data.get('count') == 0:
            return jsonify({'status': 'error', 'message': 'Genderize returned an invalid response'}), 502
        
        age_response = requests.get(f'https://api.agify.io/?name={name}')
        age_data = age_response.json()
        
        if age_data.get('age') is None:
            return jsonify({'status': 'error', 'message': 'Agify returned an invalid response'}), 502
        
        country_response = requests.get(f'https://api.nationalize.io/?name={name}')
        country_data = country_response.json()
        
        if not country_data.get('country'):
            return jsonify({'status': 'error', 'message': 'Nationalize returned an invalid response'}), 502
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'External API error: {str(e)}'}), 502
    
    # Process the data
    country_info = country_data['country'][0]
    age_group = get_age_group(age_data['age'])
    
    profile = {
        'id': str(uuid.uuid4()),
        'name': name.lower(),
        'gender': gender_data['gender'],
        'gender_probability': gender_data['probability'],
        'sample_size': gender_data['count'],
        'age': age_data['age'],
        'age_group': age_group,
        'country_id': country_info['country_id'],
        'country_probability': country_info['probability'],
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }
    
    # Save to database
    database.save_profile(profile)
    
    return jsonify({
        'status': 'success',
        'data': profile
    }), 201

@app.route('/api/profiles/<profile_id>', methods=['GET'])
def get_profile(profile_id):
    profile = database.get_profile_by_id(profile_id)
    
    if not profile:
        return jsonify({'status': 'error', 'message': 'Profile not found'}), 404
    
    return jsonify({
        'status': 'success',
        'data': dict(profile)
    }), 200

@app.route('/api/profiles', methods=['GET'])
def get_all_profiles():
    gender = request.args.get('gender')
    country_id = request.args.get('country_id')
    age_group = request.args.get('age_group')
    
    filters = {}
    if gender:
        filters['gender'] = gender
    if country_id:
        filters['country_id'] = country_id
    if age_group:
        filters['age_group'] = age_group
    
    profiles = database.get_all_profiles(filters)
    profiles_list = [dict(profile) for profile in profiles]
    
    return jsonify({
        'status': 'success',
        'count': len(profiles_list),
        'data': profiles_list
    }), 200

@app.route('/api/profiles/<profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    profile = database.get_profile_by_id(profile_id)
    
    if not profile:
        return jsonify({'status': 'error', 'message': 'Profile not found'}), 404
    
    database.delete_profile(profile_id)
    
    return '', 204

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Gender Profile API is running',
        'endpoints': {
            'POST /api/profiles': 'Create a profile',
            'GET /api/profiles': 'Get all profiles',
            'GET /api/profiles/{id}': 'Get a single profile',
            'DELETE /api/profiles/{id}': 'Delete a profile'
        }
    })

# This is for Vercel
app = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
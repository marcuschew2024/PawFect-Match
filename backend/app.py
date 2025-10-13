from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Supabase configuration
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(supabase_url, supabase_key)

# GET all pets
@app.route('/api/pets', methods=['GET'])
def get_all_pets():
    try:
        response = supabase.table('pets').select('*').execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET pet by ID
@app.route('/api/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    try:
        response = supabase.table('pets').select('*').eq('id', pet_id).execute()
        if not response.data:
            return jsonify({'error': 'Pet not found'}), 404
        return jsonify(response.data[0])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# POST - Create new pet
@app.route('/api/pets', methods=['POST'])
def create_pet():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'age', 'breed', 'size', 'gender', 'personality', 'type']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        response = supabase.table('pets').insert({
            'name': data['name'],
            'age': data['age'],
            'breed': data['breed'],
            'size': data['size'],
            'gender': data['gender'],
            'fur_color': data.get('furColor', ''),
            'personality': data['personality'],
            'image': data.get('image', ''),
            'type': data['type']
        }).execute()
        
        return jsonify(response.data[0]), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# PUT - Update pet
@app.route('/api/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    try:
        data = request.get_json()
        
        response = supabase.table('pets').update({
            'name': data.get('name'),
            'age': data.get('age'),
            'breed': data.get('breed'),
            'size': data.get('size'),
            'gender': data.get('gender'),
            'fur_color': data.get('furColor'),
            'personality': data.get('personality'),
            'image': data.get('image'),
            'type': data.get('type')
        }).eq('id', pet_id).execute()
        
        if not response.data:
            return jsonify({'error': 'Pet not found'}), 404
            
        return jsonify(response.data[0])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE - Remove pet
@app.route('/api/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    try:
        response = supabase.table('pets').delete().eq('id', pet_id).execute()
        return jsonify({'message': 'Pet deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'message': 'Backend is running!',
        'database': 'Supabase',
        'framework': 'Flask'
    })

if __name__ == '__main__':
    app.run(debug=True, port=3000)
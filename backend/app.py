from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import jwt
import requests
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')

# CORS configuration
CORS(app)

# Supabase configuration
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

# External API Keys
DOG_API_KEY = os.getenv('DOG_API_KEY')
CAT_API_KEY = os.getenv('CAT_API_KEY')

# JWT Token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

# AUTH ROUTES
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'full_name']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        email = data['email']
        password = data['password']
        full_name = data['full_name']
        phone = data.get('phone', '')
        address = data.get('address', '')
        
        # Check if user already exists
        existing_user = supabase.table('users').select('id').eq('email', email).execute()
        if existing_user.data:
            return jsonify({'error': 'User already exists with this email'}), 400
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        # Create user in database
        user_data = {
            'email': email,
            'password_hash': password_hash,
            'full_name': full_name,
            'phone': phone,
            'address': address
        }
        
        response = supabase.table('users').insert(user_data).execute()
        
        if response.data:
            user = response.data[0]
            # Generate JWT token
            token = jwt.encode({
                'user_id': user['id'],
                'email': email,
                'exp': datetime.now(timezone.utc) + timedelta(days=7)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            # Remove password hash from response
            user_response = {
                'id': user['id'],
                'email': user['email'],
                'full_name': user['full_name'],
                'phone': user['phone'],
                'address': user['address']
            }
            
            return jsonify({
                'message': 'User created successfully',
                'user': user_response,
                'token': token
            }), 201
        else:
            return jsonify({'error': 'Failed to create user'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password required'}), 400
        
        email = data['email']
        password = data['password']
        
        # Get user from database
        response = supabase.table('users').select('*').eq('email', email).execute()
        
        if not response.data:
            return jsonify({'error': 'Invalid email or password'}), 401
            
        user = response.data[0]
        
        # Check password
        if not check_password_hash(user['password_hash'], password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user['id'],
            'email': email,
            'exp': datetime.now(timezone.utc) + timedelta(days=7)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        # Remove password hash from response
        user_data = {
            'id': user['id'],
            'email': user['email'],
            'full_name': user['full_name'],
            'phone': user['phone'],
            'address': user['address']
        }
        
        return jsonify({
            'message': 'Login successful',
            'user': user_data,
            'token': token
        }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    try:
        response = supabase.table('users').select('id, email, full_name, phone, address, created_at').eq('id', current_user).execute()
        if response.data:
            return jsonify(response.data[0])
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/api/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    try:
        data = request.get_json()
        
        # Extract all fields including furColor
        update_data = {
            'name': data.get('name'),
            'type': data.get('type'),
            'breed': data.get('breed'),
            'age': data.get('age'),
            'size': data.get('size'),
            'personality': data.get('personality'),
            'furColor': data.get('furColor'),
            'image': data.get('image'),
            'available': data.get('available'),
            'updated_at': datetime.now(timezone.utc).isoformat()
        }
        
        # Remove None values
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        # Update in Supabase
        response = supabase.table('pets').update(update_data).eq('id', pet_id).execute()
        
        if response.data:
            return jsonify(response.data[0])
        else:
            return jsonify({'error': 'Pet not found'}), 404
            
    except Exception as e:
        print('Error updating pet:', e)
        return jsonify({'error': 'Failed to update pet'}), 500

# PET ROUTES - UPDATED TO FILTER ADOPTED PETS
# PET ROUTES - UPDATED TO FILTER ADOPTED PETS
@app.route('/api/pets', methods=['GET'])
def get_pets():
    try:
        # Get only available pets from Supabase
        # Use both available and is_adopted for compatibility
        response = supabase.table('pets').select('*').eq('available', True).execute()
        
        if response.data:
            # Filter out adopted pets if is_adopted column exists
            available_pets = []
            for pet in response.data:
                # If is_adopted column exists and is True, skip this pet
                if pet.get('is_adopted'):
                    continue
                available_pets.append(pet)
            
            return jsonify(available_pets)
        else:
            return jsonify([])
        
    except Exception as e:
        print('Error fetching pets:', e)
        return jsonify({'error': 'Failed to fetch pets'}), 500

@app.route('/api/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    try:
        response = supabase.table('pets').select('*').eq('id', pet_id).execute()
        if not response.data:
            return jsonify({'error': 'Pet not found'}), 404
        return jsonify(response.data[0])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ADD PET ROUTE
@app.route('/api/pets', methods=['POST'])
def create_pet():
    try:
        data = request.get_json()
        
        # Create pet data for Supabase with ALL fields
        pet_data = {
            'name': data.get('name'),
            'type': data.get('type'),
            'breed': data.get('breed'),
            'age': data.get('age'),
            'size': data.get('size'),
            'gender': data.get('gender'),  # Add this
            'personality': data.get('personality'),
            'activity_level': data.get('activity_level', 'medium'),  # Add this
            'furColor': data.get('furColor', ''),  # Add this
            'vaccination_status': data.get('vaccination_status', 'Unknown'),  # Add this
            'adoption_fee': data.get('adoption_fee', 0),  # Add this
            'health_info': data.get('health_info', ''),  # Add this
            'location': data.get('location', 'Singapore'),  # Add this
            'image': data.get('image', ''),
            'available': True,
            'is_adopted': False,  # Important for filtering
            'created_at': datetime.now(timezone.utc).isoformat()
        }
        
        # Insert into Supabase
        response = supabase.table('pets').insert(pet_data).execute()
        
        if response.data:
            return jsonify(response.data[0]), 201
        else:
            print("Supabase error:", response)
            return jsonify({'error': 'Failed to create pet'}), 400
        
    except Exception as e:
        print('Error creating pet:', e)
        return jsonify({'error': f'Failed to create pet: {str(e)}'}), 500

@app.route('/api/pets/with-scores', methods=['GET'])
@token_required
def get_pets_with_scores(current_user):
    try:
        # Get user profile
        profile_response = supabase.table('user_profiles').select('*').eq('user_id', current_user).execute()
        
        if not profile_response.data:
            return jsonify({'error': 'Please complete the lifestyle quiz first'}), 400
        
        user_profile = profile_response.data[0]
        
        # Get only available pets (not adopted)
        pets_response = supabase.table('pets').select('*').eq('is_adopted', False).execute()
        pets = pets_response.data
        
        # Calculate scores for each pet
        pets_with_scores = []
        for pet in pets:
            compatibility_score = calculate_compatibility_score(user_profile, pet)
            
            # Get favorite status
            favorite_response = supabase.table('user_favorites').select('id').eq('user_id', current_user).eq('pet_id', pet['id']).execute()
            is_favorite = len(favorite_response.data) > 0
            
            pets_with_scores.append({
                **pet,
                'compatibility_score': compatibility_score,
                'is_favorite': is_favorite
            })
        
        # Sort by compatibility score (highest first)
        pets_with_scores.sort(key=lambda x: x['compatibility_score'], reverse=True)
        
        return jsonify(pets_with_scores)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ADOPTION ROUTES
# ADOPTION ROUTES
@app.route('/api/adopt/<int:pet_id>', methods=['POST'])
@token_required
def adopt_pet(current_user, pet_id):
    try:
        data = request.get_json()
        print(f"🚀 Adoption request from user {current_user} for pet {pet_id}")
        
        # 1. Check if pet exists
        pet_response = supabase.table('pets').select('*').eq('id', pet_id).execute()
        
        if not pet_response.data:
            return jsonify({'error': 'Pet not found'}), 404
        
        pet = pet_response.data[0]
        
        # 2. Check if pet is already adopted (using available field as fallback)
        if pet.get('is_adopted') or not pet.get('available', True):
            return jsonify({'error': 'This pet has already been adopted'}), 400
        
        # 3. Prepare update data - use available field as fallback
        update_data = {
            'available': False,  # Always set this
            'is_adopted': True   # Set this if column exists
        }
        
        # Only add these if the columns exist in your database
        try:
            update_data['adopted_by'] = current_user
            update_data['adopted_at'] = datetime.now(timezone.utc).isoformat()
        except Exception as e:
            print(f"Note: Some adoption columns might not exist: {e}")
        
        # 4. Update pet as adopted
        update_response = supabase.table('pets').update(update_data).eq('id', pet_id).execute()
        
        if not update_response.data:
            return jsonify({'error': 'Failed to update pet adoption status'}), 500
        
        # 5. Create adoption record with form data
        adoption_data = {
            'pet_id': pet_id,
            'user_id': current_user,
            'adopted_at': datetime.now(timezone.utc).isoformat(),
            'status': 'completed'
        }
        
        # Only add form data if columns exist
        form_fields = [
            'applicant_name', 'applicant_email', 'applicant_phone', 'applicant_address',
            'living_situation', 'experience_with_pets', 'reason_for_adoption'
        ]
        
        for field in form_fields:
            if data.get(field):
                adoption_data[field] = data[field]
        
        adoption_response = supabase.table('adoptions').insert(adoption_data).execute()
        
        print(f"✅ Adoption successful: User {current_user} adopted pet {pet_id}")
        
        return jsonify({
            'message': f'Congratulations! You have successfully adopted {pet["name"]}!',
            'adoption_id': adoption_response.data[0]['id'] if adoption_response.data else None,
            'pet': {
                'id': pet['id'],
                'name': pet['name'],
                'is_adopted': True
            }
        }), 200
        
    except Exception as e:
        print(f"❌ Adoption error: {str(e)}")
        return jsonify({'error': f'Adoption failed: {str(e)}'}), 500

# ADOPTION APPLICATIONS ROUTE
# @app.route('/api/adoption-applications', methods=['POST'])
# @token_required
# def create_adoption_application(current_user):
#     try:
#         data = request.get_json()
        
#         # Validate required fields
#         required_fields = ['pet_id', 'applicant_name', 'applicant_email', 'applicant_phone', 
#                           'applicant_address', 'living_situation', 'experience_with_pets', 
#                           'reason_for_adoption']
#         for field in required_fields:
#             if field not in data or not data[field]:
#                 return jsonify({'error': f'Missing required field: {field}'}), 400
        
#         pet_id = data['pet_id']
        
#         # Check if pet exists and is available
#         pet_response = supabase.table('pets').select('*').eq('id', pet_id).execute()
#         if not pet_response.data:
#             return jsonify({'error': 'Pet not found'}), 404
        
#         pet = pet_response.data[0]
#         if pet.get('is_adopted'):
#             return jsonify({'error': 'This pet has already been adopted'}), 400
        
#         # Check if user already has a pending application for this pet
#         existing_application = supabase.table('adoption_applications').select('*').eq('user_id', current_user).eq('pet_id', pet_id).execute()
#         if existing_application.data:
#             return jsonify({'error': 'You already have a pending application for this pet'}), 400
        
#         # Create adoption application
#         application_data = {
#             'user_id': current_user,
#             'pet_id': pet_id,
#             'applicant_name': data['applicant_name'],
#             'applicant_email': data['applicant_email'],
#             'applicant_phone': data['applicant_phone'],
#             'applicant_address': data['applicant_address'],
#             'living_situation': data['living_situation'],
#             'experience_with_pets': data['experience_with_pets'],
#             'reason_for_adoption': data['reason_for_adoption'],
#             'status': 'pending'
#         }
        
#         response = supabase.table('adoption_applications').insert(application_data).execute()
        
#         if response.data:
#             return jsonify({
#                 'message': 'Adoption application submitted successfully! We will review your application and contact you soon.',
#                 'application_id': response.data[0]['id']
#             }), 201
#         else:
#             return jsonify({'error': 'Failed to submit adoption application'}), 400
            
#     except Exception as e:
#         print(f"Error creating adoption application: {str(e)}")
#         return jsonify({'error': str(e)}), 500

@app.route('/api/user/adoptions', methods=['GET'])
@token_required
def get_user_adoptions(current_user):
    try:
        # Get all adoptions for the current user with pet details
        response = supabase.table('adoptions').select(
            'id, status, adopted_at, pets(*)'
        ).eq('user_id', current_user).execute()
        
        adoptions = response.data
        print(f"Found {len(adoptions)} adoptions for user {current_user}")  # Debug log
        
        # Format the response to match what frontend expects
        formatted_adoptions = []
        for adoption in adoptions:
            pet = adoption.get('pets', {})
            formatted_adoptions.append({
                'id': adoption['id'],
                'status': adoption.get('status', 'completed'),
                'adopted_at': adoption['adopted_at'],
                'pet': {
                    'id': pet.get('id'),
                    'name': pet.get('name'),
                    'type': pet.get('type'),
                    'breed': pet.get('breed'),
                    'age': pet.get('age'),
                    'size': pet.get('size'),
                    'image': pet.get('image'),
                    'personality': pet.get('personality'),
                    'is_adopted': True
                }
            })
        
        return jsonify(formatted_adoptions), 200
        
    except Exception as e:
        print(f"Error in get_user_adoptions: {str(e)}")
        return jsonify({'error': str(e)}), 500


# USER ADOPTIONS ROUTE (alternative endpoint)
@app.route('/api/user/my-adoptions', methods=['GET'])
@token_required
def get_my_adoptions(current_user):
    try:
        # Get adoptions with pet details
        response = supabase.table('adoptions').select(
            '*, pets(*)'
        ).eq('user_id', current_user).execute()
        
        adoptions = response.data
        
        # Format response
        formatted_adoptions = []
        for adoption in adoptions:
            pet = adoption.get('pets', {})
            formatted_adoptions.append({
                'id': adoption['id'],
                'adoption_date': adoption['adopted_at'],
                'status': adoption['status'],
                'pets': {
                    'id': pet.get('id'),
                    'name': pet.get('name'),
                    'type': pet.get('type'),
                    'breed': pet.get('breed'),
                    'age': pet.get('age'),
                    'size': pet.get('size'),
                    'image': pet.get('image'),
                    'personality': pet.get('personality')
                }
            })
        
        return jsonify(formatted_adoptions), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/profile', methods=['GET'])
@token_required
def get_user_profile(current_user):
    try:
        # Get user basic info
        user_response = supabase.table('users').select('*').eq('id', current_user).execute()
        
        if not user_response.data:
            return jsonify({'error': 'User not found'}), 404
        
        user = user_response.data[0]
        
        # Get user's adoptions count
        adoptions_response = supabase.table('adoptions').select('id', count='exact').eq('user_id', current_user).execute()
        
        # Get user's favorites count
        favorites_response = supabase.table('user_favorites').select('id', count='exact').eq('user_id', current_user).execute()
        
        # Get recent adoptions
        recent_adoptions_response = supabase.table('adoptions').select(
            '*, pets(name, type, image)'
        ).eq('user_id', current_user).order('adopted_at', desc=True).limit(3).execute()
        
        profile_data = {
            'user': {
                'id': user['id'],
                'email': user['email'],
                'full_name': user['full_name'],
                'phone': user.get('phone'),
                'address': user.get('address'),
                'created_at': user.get('created_at')
            },
            'stats': {
                'adoptions_count': len(adoptions_response.data) if adoptions_response.data else 0,
                'favorites_count': len(favorites_response.data) if favorites_response.data else 0
            },
            'recent_adoptions': recent_adoptions_response.data if recent_adoptions_response.data else []
        }
        
        return jsonify(profile_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# QUIZ ROUTES
@app.route('/api/user/quiz', methods=['POST'])
@token_required
def save_quiz_results(current_user):
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['living_space', 'activity_level', 'preferred_pet_type', 'has_allergies']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Save or update user profile with quiz results
        profile_data = {
            'user_id': current_user,
            'living_space': data['living_space'],
            'activity_level': data['activity_level'],
            'preferred_pet_type': data['preferred_pet_type'],
            'has_allergies': data['has_allergies'],
            'allergies': data.get('allergies', ''),
            'experience_level': data.get('experience_level', 'first_time'),
            'home_environment': data.get('home_environment', 'quiet'),
            'has_children': data.get('has_children', False),
            'children_ages': data.get('children_ages', ''),
            'has_other_pets': data.get('has_other_pets', False),
            'other_pets_details': data.get('other_pets_details', ''),
            'time_commitment': data.get('time_commitment', 'medium')
        }
        
        # Check if profile exists
        existing_profile = supabase.table('user_profiles').select('*').eq('user_id', current_user).execute()
        
        if existing_profile.data:
            # Update existing profile
            response = supabase.table('user_profiles').update(profile_data).eq('user_id', current_user).execute()
        else:
            # Create new profile
            response = supabase.table('user_profiles').insert(profile_data).execute()
        
        return jsonify({
            'message': 'Quiz results saved successfully',
            'profile': response.data[0] if response.data else None
        }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/quiz', methods=['GET'])
@token_required
def get_quiz_results(current_user):
    try:
        response = supabase.table('user_profiles').select('*').eq('user_id', current_user).execute()
        
        if response.data:
            return jsonify(response.data[0])
        else:
            return jsonify({'error': 'No quiz results found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# FAVORITES ROUTES
@app.route('/api/user/favorites', methods=['GET'])
@token_required
def get_favorites(current_user):
    try:
        response = supabase.table('user_favorites').select('pet_id').eq('user_id', current_user).execute()
        favorite_ids = [item['pet_id'] for item in response.data]
        return jsonify(favorite_ids)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/favorites', methods=['POST'])
@token_required
def add_favorite(current_user):
    try:
        data = request.get_json()
        
        if 'pet_id' not in data:
            return jsonify({'error': 'Pet ID is required'}), 400
        
        response = supabase.table('user_favorites').insert({
            'user_id': current_user,
            'pet_id': data['pet_id']
        }).execute()
        
        return jsonify({'message': 'Pet added to favorites'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/favorites/<int:pet_id>', methods=['DELETE'])
@token_required
def remove_favorite(current_user, pet_id):
    try:
        response = supabase.table('user_favorites').delete().eq('user_id', current_user).eq('pet_id', pet_id).execute()
        return jsonify({'message': 'Pet removed from favorites'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# MATCHING ALGORITHM
def calculate_compatibility_score(user_profile, pet):
    """Calculate compatibility score between user and pet (0-100)"""
    score = 0
    max_score = 100
    
    # 1. Pet Type Compatibility (20 points)
    if user_profile['preferred_pet_type'] == 'both':
        score += 20
    elif user_profile['preferred_pet_type'] == pet['type']:
        score += 20
    else:
        score += 0
    
    # 2. Activity Level Compatibility (25 points)
    activity_map = {'low': 1, 'medium': 2, 'high': 3}
    user_activity = activity_map.get(user_profile['activity_level'], 2)
    pet_activity = activity_map.get(pet.get('activity_level', 'medium'), 2)
    
    activity_diff = abs(user_activity - pet_activity)
    if activity_diff == 0:
        score += 25
    elif activity_diff == 1:
        score += 15
    else:
        score += 5
    
    # 3. Living Space Compatibility (20 points)
    space_requirements = {
        'apartment': ['Small', 'Medium'],
        'house': ['Small', 'Medium', 'Large'],
        'farm': ['Medium', 'Large']
    }
    
    if pet['size'] in space_requirements.get(user_profile['living_space'], []):
        score += 20
    else:
        score += 5
    
    # 4. Experience Level Compatibility (15 points)
    experience_map = {'beginner': 1, 'intermediate': 2, 'experienced': 3}
    user_exp = experience_map.get(user_profile['experience_level'], 1)
    pet_exp = experience_map.get(pet.get('experience_needed', 'beginner'), 1)
    
    if user_exp >= pet_exp:
        score += 15
    else:
        score += max(0, 15 - (pet_exp - user_exp) * 5)
    
    # 5. Family Compatibility (10 points)
    if user_profile.get('has_children', False) and not pet.get('good_with_children', True):
        score += 0
    else:
        score += 10
    
    # 6. Other Pets Compatibility (10 points)
    if user_profile.get('has_other_pets', False) and not pet.get('good_with_other_pets', True):
        score += 0
    else:
        score += 10
    
    return min(score, max_score)

# EXTERNAL API ROUTES
@app.route('/api/external/dog-breeds', methods=['GET'])
def get_dog_breeds():
    try:
        response = requests.get(
            "https://api.thedogapi.com/v1/breeds",
            headers={"x-api-key": DOG_API_KEY}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/external/cat-breeds', methods=['GET'])
def get_cat_breeds():
    try:
        response = requests.get(
            "https://api.thecatapi.com/v1/breeds",
            headers={"x-api-key": CAT_API_KEY}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/external/dog-images', methods=['GET'])
def get_dog_images():
    try:
        breed_id = request.args.get('breed_id')
        limit = request.args.get('limit', 1)
        
        params = {'limit': limit, 'size': 'med'}
        if breed_id:
            params['breed_ids'] = breed_id
            
        response = requests.get(
            "https://api.thedogapi.com/v1/images/search",
            headers={"x-api-key": DOG_API_KEY},
            params=params
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/external/cat-images', methods=['GET'])
def get_cat_images():
    try:
        breed_id = request.args.get('breed_id')
        limit = request.args.get('limit', 1)
        
        params = {'limit': limit, 'size': 'med'}
        if breed_id:
            params['breed_ids'] = breed_id
            
        response = requests.get(
            "https://api.thecatapi.com/v1/images/search",
            headers={"x-api-key": CAT_API_KEY},
            params=params
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'message': 'Backend is running!',
        'database': 'Supabase',
        'framework': 'Flask',
        'authentication': 'JWT + Password Hash'
    })

if __name__ == '__main__':
    app.run(debug=True, port=3000)

    
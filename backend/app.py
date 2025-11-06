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
import base64
from io import BytesIO
from PIL import Image
import uuid


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')

# CORS configuration
CORS(app, origins=["*"])  

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

# Image upload configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compress_image(image_data, max_size=(1200, 1200), quality=85):
    """Compress image to reduce file size while maintaining quality"""
    try:
        image = Image.open(BytesIO(image_data))
        
        # Convert to RGB if necessary
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        
        # Resize if too large
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Compress
        output = BytesIO()
        image.save(output, format='JPEG', quality=quality, optimize=True)
        return output.getvalue()
    except Exception as e:
        print(f"Image compression error: {e}")
        return image_data  # Return original if compression fails

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
        
        # Extract pet data (excluding images)
        update_data = {
            'name': data.get('name'),
            'type': data.get('type'),
            'breed': data.get('breed'),
            'age': data.get('age'),
            'size': data.get('size'),
            'personality': data.get('personality'),
            'fur_color': data.get('fur_color'),
            'available': data.get('available'),
            'updated_at': datetime.now(timezone.utc).isoformat()
        }
        
        # Handle single image update
        if data.get('image'):
            update_data['image'] = data['image']
            update_data['main_image'] = data['image']
        
        # Remove None values
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        # Update pet in Supabase
        response = supabase.table('pets').update(update_data).eq('id', pet_id).execute()
        
        if response.data:
            # Handle multiple images update if provided
            if 'images' in data:
                # Delete existing images
                supabase.table('pet_images').delete().eq('pet_id', pet_id).execute()
                
                # Insert new images
                images = data['images']
                if images:
                    image_records = []
                    for i, image in enumerate(images):
                        if isinstance(image, dict) and 'image_url' in image:
                            image_records.append({
                                'pet_id': pet_id,
                                'image_url': image['image_url'],
                                'image_order': image.get('image_order', i)
                            })
                        elif isinstance(image, str) and image.strip():
                            image_records.append({
                                'pet_id': pet_id,
                                'image_url': image.strip(),
                                'image_order': i
                            })
                    
                    if image_records:
                        supabase.table('pet_images').insert(image_records).execute()
                        
                        # Update main_image to first image
                        first_image = image_records[0]['image_url']
                        supabase.table('pets').update({
                            'main_image': first_image,
                            'image': first_image
                        }).eq('id', pet_id).execute()
            
            # Return updated pet with images
            updated_pet = supabase.table('pets').select('''
                *,
                pet_images(*)
            ''').eq('id', pet_id).execute()
            
            if updated_pet.data:
                pet = updated_pet.data[0]
                images = pet.get('pet_images', [])
                if not images and pet.get('image'):
                    images = [{'image_url': pet['image'], 'image_order': 0}]
                
                images.sort(key=lambda x: x.get('image_order', 0))
                
                pet_response = {
                    **pet,
                    'images': images,
                    'main_image': pet.get('main_image') or (images[0]['image_url'] if images else None)
                }
                
                if 'pet_images' in pet_response:
                    del pet_response['pet_images']
                
                return jsonify(pet_response)
            
            return jsonify(response.data[0])
        else:
            return jsonify({'error': 'Pet not found'}), 404
            
    except Exception as e:
        print('Error updating pet:', e)
        return jsonify({'error': 'Failed to update pet'}), 500

# PET ROUTES - UPDATED TO FILTER ADOPTED PETS
# PET ROUTES - UPDATED TO FILTER ADOPTED PETS
# PET ROUTES - UPDATED FOR MULTIPLE IMAGES
@app.route('/api/pets', methods=['GET'])
def get_pets():
    try:
        # Get pets with their images
        response = supabase.table('pets').select('''
            *,
            pet_images(*)
        ''').eq('available', True).execute()
        
        if response.data:
            # Filter out adopted pets and format response
            available_pets = []
            for pet in response.data:
                # Skip adopted pets
                if pet.get('is_adopted'):
                    continue
                
                # Format images array
                images = pet.get('pet_images', [])
                if not images and pet.get('image'):
                    # Fallback for pets with only old image field
                    images = [{'image_url': pet['image'], 'image_order': 0}]
                
                # Sort images by order
                images.sort(key=lambda x: x.get('image_order', 0))
                
                # Create pet response with images array
                pet_response = {
                    **pet,
                    'images': images,
                    'main_image': pet.get('main_image') or (images[0]['image_url'] if images else None)
                }
                
                # Remove the pet_images key to avoid confusion
                if 'pet_images' in pet_response:
                    del pet_response['pet_images']
                
                available_pets.append(pet_response)
            
            return jsonify(available_pets)
        else:
            return jsonify([])
        
    except Exception as e:
        print('Error fetching pets:', e)
        return jsonify({'error': 'Failed to fetch pets'}), 500

@app.route('/api/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    try:
        print(f"🔍 Fetching pet with ID: {pet_id}")
        
        # Get pet data
        pet_response = supabase.table('pets').select('*').eq('id', pet_id).execute()
        
        if not pet_response.data:
            return jsonify({'error': 'Pet not found'}), 404
        
        pet_data = pet_response.data[0]
        print(f"🐕 Pet found: {pet_data['name']}")
        
        # Get images separately
        images_response = supabase.table('pet_images').select('*').eq('pet_id', pet_id).order('image_order').execute()
        images_array = images_response.data if images_response.data else []
        
        print(f"📸 Found {len(images_array)} images for pet {pet_id}")
        
        # Create response with images array
        pet_response = {
            **pet_data,
            'images': images_array,
            'main_image': pet_data.get('main_image') or (images_array[0]['image_url'] if images_array else None)
        }
        
        print(f"✅ Final pet response with {len(images_array)} images")
        return jsonify(pet_response)
    except Exception as e:
        print(f"❌ Error in get_pet: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ADD PET ROUTE
# Update the create_pet route to handle multiple images better
@app.route('/api/pets', methods=['POST'])
def create_pet():
    try:
        data = request.get_json()
        print(f"📝 Creating pet with data keys: {list(data.keys())}")
        images = data.get('images', [])
        print(f"🖼️ Images received: {len(images)} images")
        
        # Validate required fields
        required_fields = ['name', 'type', 'breed', 'age', 'size', 'gender', 'personality']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create pet data for Supabase
        pet_data = {
            'name': data.get('name'),
            'type': data.get('type'),
            'breed': data.get('breed'),
            'age': data.get('age'),
            'size': data.get('size'),
            'gender': data.get('gender'),
            'personality': data.get('personality'),
            'activity_level': data.get('activity_level', 'medium'),
            'fur_color': data.get('fur_color', ''),
            'vaccination_status': data.get('vaccination_status', 'Unknown'),
            'adoption_fee': data.get('adoption_fee', 0),
            'health_info': data.get('health_info', ''),
            'location': data.get('location', 'Singapore'),
            'available': True,
            'is_adopted': False,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'background': data.get('background', ''),
            'good_with_children': data.get('good_with_children'),
            'good_with_other_pets': data.get('good_with_other_pets'),
            'vaccinated': data.get('vaccinated'),
            'neutered': data.get('neutered'),
            'hdb_approved': data.get('hdb_approved', False)
        }
        
        print(f"🐕 Pet data prepared, inserting into database...")
        
        # Insert into Supabase
        response = supabase.table('pets').insert(pet_data).execute()
        
        if response.data:
            new_pet = response.data[0]
            pet_id = new_pet['id']
            print(f"✅ Pet created with ID: {pet_id}")
            
            # Handle multiple images
            images = data.get('images', [])
            print(f"🖼️ Processing {len(images)} images for pet {pet_id}")
            
            if images and len(images) > 0:
                image_records = []
                for i, image_url in enumerate(images):
                    if isinstance(image_url, str) and image_url.strip():
                        image_record = {
                            'pet_id': pet_id,
                            'image_url': image_url.strip(),
                            'image_order': i
                        }
                        image_records.append(image_record)
                        print(f"📸 Prepared image {i} for saving")
                
                print(f"💾 Attempting to save {len(image_records)} images to pet_images table")
                
                if image_records:
                    try:
                        # Insert all images in one batch
                        image_response = supabase.table('pet_images').insert(image_records).execute()
                        
                        if image_response.data:
                            print(f"✅ SUCCESS: Saved {len(image_response.data)} images to pet_images table")
                            for img in image_response.data:
                                print(f"   - Image ID: {img['id']}, Order: {img['image_order']}, URL length: {len(img['image_url'])}")
                        else:
                            print(f"❌ FAILED: No data returned from image insert: {image_response}")
                            
                    except Exception as e:
                        print(f"❌ EXCEPTION when saving images: {str(e)}")
                    
                    # Set first image as main_image
                    first_image = image_records[0]['image_url']
                    print(f"⭐ Setting main image from first image")
                    update_response = supabase.table('pets').update({
                        'main_image': first_image,
                        'image': first_image
                    }).eq('id', pet_id).execute()
                    print(f"✅ Main image updated: {update_response.data is not None}")
            
            # FIXED: Return the complete pet with images using a different approach
            print(f"🔍 Fetching complete pet data with images...")
            
            # First get the pet
            pet_response = supabase.table('pets').select('*').eq('id', pet_id).execute()
            if not pet_response.data:
                return jsonify({'error': 'Pet not found after creation'}), 500
                
            pet_data = pet_response.data[0]
            
            # Then get the images separately
            images_response = supabase.table('pet_images').select('*').eq('pet_id', pet_id).order('image_order').execute()
            images_array = images_response.data if images_response.data else []
            
            print(f"📊 Pet data retrieved, found {len(images_array)} images separately")
            
            # Combine the data
            final_response = {
                **pet_data,
                'images': images_array,
                'main_image': pet_data.get('main_image') or (images_array[0]['image_url'] if images_array else None)
            }
            
            print(f"🎉 Final response ready with {len(images_array)} images")
            return jsonify(final_response), 201
        else:
            print(f"❌ Supabase error creating pet: {response}")
            return jsonify({'error': 'Failed to create pet'}), 400
        
    except Exception as e:
        print(f'❌ Error creating pet: {str(e)}')
        return jsonify({'error': f'Failed to create pet: {str(e)}'}), 500
    
    
# PET IMAGES MANAGEMENT
@app.route('/api/pets/<int:pet_id>/images', methods=['POST'])
def add_pet_images(pet_id):
    try:
        data = request.get_json()
        images = data.get('images', [])
        
        if not images:
            return jsonify({'error': 'No images provided'}), 400
        
        # Get current max order
        current_images = supabase.table('pet_images').select('image_order').eq('pet_id', pet_id).order('image_order', desc=True).execute()
        start_order = current_images.data[0]['image_order'] + 1 if current_images.data else 0
        
        # Prepare image records
        image_records = []
        for i, image_url in enumerate(images):
            if isinstance(image_url, str) and image_url.strip():
                image_records.append({
                    'pet_id': pet_id,
                    'image_url': image_url.strip(),
                    'image_order': start_order + i
                })
        
        if image_records:
            # Insert new images
            response = supabase.table('pet_images').insert(image_records).execute()
            
            # Update main_image if this is the first image
            if start_order == 0 and image_records:
                first_image = image_records[0]['image_url']
                supabase.table('pets').update({
                    'main_image': first_image,
                    'image': first_image
                }).eq('id', pet_id).execute()
            
            return jsonify({'message': f'Added {len(image_records)} images', 'images': response.data}), 201
        else:
            return jsonify({'error': 'No valid images provided'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pets/<int:pet_id>/images/<int:image_id>', methods=['DELETE'])
def delete_pet_image(pet_id, image_id):
    try:
        # Delete the image
        response = supabase.table('pet_images').delete().eq('id', image_id).eq('pet_id', pet_id).execute()
        
        if response.data:
            # Check if we need to update main_image
            remaining_images = supabase.table('pet_images').select('*').eq('pet_id', pet_id).order('image_order').execute()
            
            if remaining_images.data:
                # Set new main_image to first remaining image
                new_main_image = remaining_images.data[0]['image_url']
                supabase.table('pets').update({
                    'main_image': new_main_image,
                    'image': new_main_image
                }).eq('id', pet_id).execute()
            else:
                # No images left, clear main_image
                supabase.table('pets').update({
                    'main_image': None,
                    'image': None
                }).eq('id', pet_id).execute()
            
            return jsonify({'message': 'Image deleted successfully'}), 200
        else:
            return jsonify({'error': 'Image not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/pets/with-scores', methods=['GET'])
@token_required
def get_pets_with_scores(current_user):
    try:
        # Get user profile
        profile_response = supabase.table('user_profiles').select('*').eq('user_id', current_user).execute()
        
        if not profile_response.data:
            return jsonify({'error': 'Please complete the lifestyle quiz first'}), 400
        
        user_profile = profile_response.data[0]
        
        # Get available pets with their images
        pets_response = supabase.table('pets').select('''
            *,
            pet_images(*)
        ''').eq('is_adopted', False).execute()
        
        pets = pets_response.data
        
        # Calculate scores for each pet
        pets_with_scores = []
        for pet in pets:
            # Format images
            images = pet.get('pet_images', [])
            if not images and pet.get('image'):
                images = [{'image_url': pet['image'], 'image_order': 0}]
            
            images.sort(key=lambda x: x.get('image_order', 0))
            
            compatibility_score = calculate_compatibility_score(user_profile, pet)
            
            # Get favorite status
            favorite_response = supabase.table('user_favorites').select('id').eq('user_id', current_user).eq('pet_id', pet['id']).execute()
            is_favorite = len(favorite_response.data) > 0
            
            # Create pet response with images
            pet_response = {
                **pet,
                'images': images,
                'main_image': pet.get('main_image') or (images[0]['image_url'] if images else None),
                'compatibility_score': compatibility_score,
                'is_favorite': is_favorite
            }
            
            if 'pet_images' in pet_response:
                del pet_response['pet_images']
            
            pets_with_scores.append(pet_response)
        
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

@app.route('/adoptions', methods=['GET'])
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
        print(f"📝 Received quiz data: {data}")
        
        # Validate required fields
        required_fields = ['living_space', 'activity_level', 'preferred_pet_type', 'has_allergies']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Map frontend field names to database field names with proper value mapping
        profile_data = {
            'user_id': current_user,
            'living_space': data['living_space'],
            'activity_level': data['activity_level'],
            'preferred_pet_type': data['preferred_pet_type'],  # Note: Database expects 'both' not 'both'
            'has_allergies': data['has_allergies'],
            'allergies': data.get('allergies', ''),
            # Map pet_experience to experience_level with exact database values
            'experience_level': map_experience_level(data.get('pet_experience', 'none')),
            # Map home_environment to database values
            'home_environment': map_home_environment(data.get('home_environment', 'quiet')),
            'has_children': data.get('has_children', False),
            'children_ages': data.get('children_ages', ''),
            'has_other_pets': data.get('has_pets', False),
            'other_pets_details': data.get('pets_details', ''),
            # Map hours_alone to time_commitment with value conversion
            'time_commitment': map_time_commitment(data.get('hours_alone', '4-8'))
        }
        
        print(f"🗃️ Mapped profile data: {profile_data}")
        
        # Validate and ensure values match database constraints
        profile_data = validate_profile_data(profile_data)
        
        print(f"✅ Validated profile data: {profile_data}")
        
        # Check if profile exists
        existing_profile = supabase.table('user_profiles').select('*').eq('user_id', current_user).execute()
        
        if existing_profile.data:
            # Update existing profile
            response = supabase.table('user_profiles').update(profile_data).eq('user_id', current_user).execute()
            print(f"📝 Updated existing profile: {response.data}")
        else:
            # Create new profile
            response = supabase.table('user_profiles').insert(profile_data).execute()
            print(f"🆕 Created new profile: {response.data}")
        
        if response.data:
            return jsonify({
                'message': 'Quiz results saved successfully',
                'profile': response.data[0]
            }), 200
        else:
            return jsonify({'error': 'Failed to save quiz results'}), 400
            
    except Exception as e:
        print(f"❌ Error saving quiz: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Helper functions for value mapping
# Update the map_experience_level function with exact database values
# Update all mapping functions with exact database constraints
def map_experience_level(frontend_value):
    """Map frontend experience values to database values"""
    mapping = {
        'none': 'first_time',
        'some_experience': 'some_experience', 
        'experienced': 'experienced'
    }
    return mapping.get(frontend_value, 'first_time')

def map_time_commitment(frontend_value):
    """Map frontend hours_alone values to time_commitment values"""
    mapping = {
        '0-4': 'low',
        '4-8': 'medium', 
        '8+': 'high'
    }
    return mapping.get(frontend_value, 'medium')

def map_home_environment(frontend_value):
    """Map frontend home_environment to database values"""
    mapping = {
        'quiet': 'quiet',
        'moderate': 'active',  # Map 'moderate' to 'active' since 'moderate' not allowed
        'active': 'very_active'  # Map 'active' to 'very_active'
    }
    return mapping.get(frontend_value, 'quiet')

def validate_profile_data(data):
    """Ensure all values match database constraints"""
    # Exact allowed values from database constraints
    allowed_values = {
        'experience_level': ['first_time', 'some_experience', 'experienced'],
        'home_environment': ['quiet', 'active', 'very_active'],  # Exact database values
        'time_commitment': ['low', 'medium', 'high'],
        'activity_level': ['low', 'medium', 'high'],
        'living_space': ['apartment', 'house', 'farm'],
        'preferred_pet_type': ['dog', 'cat', 'both']  # Note: Database has 'bath' instead of 'both'
    }
    
    # Validate each field
    for field, allowed in allowed_values.items():
        if field in data and data[field] not in allowed:
            print(f"Invalid value for {field}: '{data[field]}'. Allowed: {allowed}")
            # Set to first allowed value as default
            data[field] = allowed[0] if allowed else ''
            print(f"Changed to: '{data[field]}'")
    
    return data

@app.route('/api/user/quiz', methods=['GET'])
@token_required
def get_quiz_results(current_user):
    try:
        response = supabase.table('user_profiles').select('*').eq('user_id', current_user).execute()
        
        if response.data:
            return jsonify({
                'has_completed_quiz': True,
                'profile': response.data[0]
            })
        else:
            return jsonify({
                'has_completed_quiz': False,
                'message': 'Quiz not completed yet'
            }), 200
            
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
    
# Add this route after the existing routes (before the health check)
@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    """Handle image upload and return URL"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use: PNG, JPG, JPEG, GIF, WEBP'}), 400
        
        # Read and validate file size
        file_data = file.read()
        if len(file_data) > MAX_IMAGE_SIZE:
            return jsonify({'error': 'File too large. Maximum 5MB allowed'}), 400
        
        # Compress image
        compressed_data = compress_image(file_data)
        
        # Convert to base64 for storage (in production, use cloud storage)
        image_b64 = base64.b64encode(compressed_data).decode('utf-8')
        image_url = f"data:{file.mimetype};base64,{image_b64}"
        
        return jsonify({
            'url': image_url,
            'message': 'Image uploaded successfully'
        }), 200
        
    except Exception as e:
        print(f"Upload error: {e}")
        return jsonify({'error': 'Failed to upload image'}), 500

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'message': 'Backend is running!',
        'database': 'Supabase',
        'framework': 'Flask',
        'authentication': 'JWT + Password Hash'
    })
#forum
# Get all questions with answers and user info
@app.route('/api/forum/questions', methods=['GET'])

def get_forum_questions():
    try:
        category = request.args.get('category', 'all')
        search = request.args.get('search', '')
        
        # Build query
        query = supabase.table('forum_questions').select('''
            *,
            users!forum_questions_user_id_fkey(id, full_name)
        ''')
        
        # Filter by category if not 'all'
        if category and category != 'all':
            query = query.eq('category', category)
        
        # Search in title or content
        if search:
            query = query.or_(f'title.ilike.%{search}%,content.ilike.%{search}%')
        
        # Order by newest first
        response = query.order('created_at', desc=True).execute()
        
        # Format response with answers
        questions = []
        for q in response.data:
            # Get answers for this question
            answers_response = supabase.table('forum_answers').select('''
                *,
                users!forum_answers_user_id_fkey(id, full_name)
            ''').eq('question_id', q['id']).order('created_at', desc=False).execute()
            
            # Format answers
            formatted_answers = []
            if answers_response.data:
                for a in answers_response.data:
                    formatted_answers.append({
                        'id': a['id'],
                        'content': a['content'],
                        'likes': a['likes'],
                        'createdAt': a['created_at'],
                        'author': a['users']['full_name'] if a.get('users') else 'Anonymous',
                        'author_id': a['user_id']
                    })
            
            question = {
                'id': q['id'],
                'title': q['title'],
                'content': q['content'],
                'category': q['category'],
                'likes': q['likes'],
                'createdAt': q['created_at'],
                'author': q['users']['full_name'] if q.get('users') else 'Anonymous',
                'author_id': q['user_id'],
                'answers': formatted_answers
            }
            questions.append(question)
        
        return jsonify(questions), 200
        
    except Exception as e:
        print(f"Error fetching questions: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Create new question
@app.route('/api/forum/questions', methods=['POST'])
@token_required
def create_forum_question(current_user):
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('title') or not data.get('content'):
            return jsonify({'error': 'Title and content are required'}), 400
        
        if not data.get('category'):
            return jsonify({'error': 'Category is required'}), 400
        
        # Create question
        question_data = {
            'user_id': current_user,
            'title': data['title'],
            'content': data['content'],
            'category': data['category']
        }
        
        response = supabase.table('forum_questions').insert(question_data).execute()
        
        if response.data:
            # Get full question with user info
            full_question = supabase.table('forum_questions').select('''
                *,
                users!forum_questions_user_id_fkey(id, full_name)
            ''').eq('id', response.data[0]['id']).execute()
            
            q = full_question.data[0]
            return jsonify({
                'id': q['id'],
                'title': q['title'],
                'content': q['content'],
                'category': q['category'],
                'likes': q['likes'],
                'createdAt': q['created_at'],
                'author': q['users']['full_name'] if q.get('users') else 'Anonymous',
                'author_id': q['user_id'],
                'answers': []
            }), 201
        
        return jsonify({'error': 'Failed to create question'}), 400
        
    except Exception as e:
        print(f"Error creating question: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Get single question with details
@app.route('/api/forum/questions/<int:question_id>', methods=['GET'])
def get_forum_question(question_id):
    try:
        response = supabase.table('forum_questions').select('''
            *,
            users!forum_questions_user_id_fkey(id, full_name)
        ''').eq('id', question_id).execute()
        
        if not response.data:
            return jsonify({'error': 'Question not found'}), 404
        
        q = response.data[0]
        
        # Get answers for this question
        answers_response = supabase.table('forum_answers').select('''
            *,
            users!forum_answers_user_id_fkey(id, full_name)
        ''').eq('question_id', question_id).order('created_at', desc=False).execute()
        
        formatted_answers = []
        if answers_response.data:
            for a in answers_response.data:
                formatted_answers.append({
                    'id': a['id'],
                    'content': a['content'],
                    'likes': a['likes'],
                    'createdAt': a['created_at'],
                    'author': a['users']['full_name'] if a.get('users') else 'Anonymous',
                    'author_id': a['user_id']
                })
        
        question = {
            'id': q['id'],
            'title': q['title'],
            'content': q['content'],
            'category': q['category'],
            'likes': q['likes'],
            'createdAt': q['created_at'],
            'author': q['users']['full_name'] if q.get('users') else 'Anonymous',
            'author_id': q['user_id'],
            'answers': formatted_answers
        }
        
        return jsonify(question), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Update question (only owner can update)
@app.route('/api/forum/questions/<int:question_id>', methods=['PUT'])
@token_required
def update_forum_question(current_user, question_id):
    try:
        data = request.get_json()
        
        # Check ownership
        question = supabase.table('forum_questions').select('user_id').eq('id', question_id).execute()
        
        if not question.data:
            return jsonify({'error': 'Question not found'}), 404
        
        if question.data[0]['user_id'] != current_user:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Update question
        update_data = {
            'title': data.get('title'),
            'content': data.get('content'),
            'category': data.get('category'),
            'updated_at': datetime.now(timezone.utc).isoformat()
        }
        
        # Remove None values
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        supabase.table('forum_questions').update(update_data).eq('id', question_id).execute()
        
        return jsonify({'message': 'Question updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Delete question (only owner can delete)
@app.route('/api/forum/questions/<int:question_id>', methods=['DELETE'])
@token_required
def delete_forum_question(current_user, question_id):
    try:
        # Check ownership
        question = supabase.table('forum_questions').select('user_id').eq('id', question_id).execute()
        
        if not question.data:
            return jsonify({'error': 'Question not found'}), 404
        
        if question.data[0]['user_id'] != current_user:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Delete question (answers will be deleted automatically via CASCADE)
        supabase.table('forum_questions').delete().eq('id', question_id).execute()
        
        return jsonify({'message': 'Question deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==========================================================
# FORUM ANSWERS
# ==========================================================

# Create answer to a question
@app.route('/api/forum/questions/<int:question_id>/answers', methods=['POST'])
@token_required
def create_forum_answer(current_user, question_id):
    try:
        data = request.get_json()
        
        if not data.get('content'):
            return jsonify({'error': 'Content is required'}), 400
        
        # Check if question exists
        question = supabase.table('forum_questions').select('id').eq('id', question_id).execute()
        if not question.data:
            return jsonify({'error': 'Question not found'}), 404
        
        # Create answer
        answer_data = {
            'question_id': question_id,
            'user_id': current_user,
            'content': data['content']
        }
        
        response = supabase.table('forum_answers').insert(answer_data).execute()
        
        if response.data:
            # Get full answer with user info
            full_answer = supabase.table('forum_answers').select('''
                *,
                users!forum_answers_user_id_fkey(id, full_name)
            ''').eq('id', response.data[0]['id']).execute()
            
            a = full_answer.data[0]
            return jsonify({
                'id': a['id'],
                'content': a['content'],
                'likes': a['likes'],
                'createdAt': a['created_at'],
                'author': a['users']['full_name'] if a.get('users') else 'Anonymous',
                'author_id': a['user_id']
            }), 201
        
        return jsonify({'error': 'Failed to create answer'}), 400
        
    except Exception as e:
        print(f"Error creating answer: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Delete answer (only owner can delete)
@app.route('/api/forum/answers/<int:answer_id>', methods=['DELETE'])
@token_required
def delete_forum_answer(current_user, answer_id):
    try:
        # Check ownership
        answer = supabase.table('forum_answers').select('user_id').eq('id', answer_id).execute()
        
        if not answer.data:
            return jsonify({'error': 'Answer not found'}), 404
        
        if answer.data[0]['user_id'] != current_user:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Delete answer
        supabase.table('forum_answers').delete().eq('id', answer_id).execute()
        
        return jsonify({'message': 'Answer deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==========================================================
# FORUM LIKES
# ==========================================================

# Like/Unlike a question
@app.route('/api/forum/questions/<int:question_id>/like', methods=['POST'])
@token_required
def like_forum_question(current_user, question_id):
    try:
        # Check if already liked
        existing_like = supabase.table('forum_question_likes').select('id').eq('question_id', question_id).eq('user_id', current_user).execute()
        
        if existing_like.data:
            # Unlike - remove like
            supabase.table('forum_question_likes').delete().eq('question_id', question_id).eq('user_id', current_user).execute()
            
            # Decrement likes count
            question = supabase.table('forum_questions').select('likes').eq('id', question_id).execute()
            if question.data:
                new_likes = max(0, question.data[0]['likes'] - 1)
                supabase.table('forum_questions').update({'likes': new_likes}).eq('id', question_id).execute()
                return jsonify({'liked': False, 'likes': new_likes}), 200
        else:
            # Like - add like
            supabase.table('forum_question_likes').insert({
                'question_id': question_id,
                'user_id': current_user
            }).execute()
            
            # Increment likes count
            question = supabase.table('forum_questions').select('likes').eq('id', question_id).execute()
            if question.data:
                new_likes = question.data[0]['likes'] + 1
                supabase.table('forum_questions').update({'likes': new_likes}).eq('id', question_id).execute()
                return jsonify({'liked': True, 'likes': new_likes}), 200
        
        return jsonify({'error': 'Question not found'}), 404
        
    except Exception as e:
        print(f"Error liking question: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Like/Unlike an answer
@app.route('/api/forum/answers/<int:answer_id>/like', methods=['POST'])
@token_required
def like_forum_answer(current_user, answer_id):
    try:
        # Check if already liked
        existing_like = supabase.table('forum_answer_likes').select('id').eq('answer_id', answer_id).eq('user_id', current_user).execute()
        
        if existing_like.data:
            # Unlike
            supabase.table('forum_answer_likes').delete().eq('answer_id', answer_id).eq('user_id', current_user).execute()
            
            # Decrement likes count
            answer = supabase.table('forum_answers').select('likes').eq('id', answer_id).execute()
            if answer.data:
                new_likes = max(0, answer.data[0]['likes'] - 1)
                supabase.table('forum_answers').update({'likes': new_likes}).eq('id', answer_id).execute()
                return jsonify({'liked': False, 'likes': new_likes}), 200
        else:
            # Like
            supabase.table('forum_answer_likes').insert({
                'answer_id': answer_id,
                'user_id': current_user
            }).execute()
            
            # Increment likes count
            answer = supabase.table('forum_answers').select('likes').eq('id', answer_id).execute()
            if answer.data:
                new_likes = answer.data[0]['likes'] + 1
                supabase.table('forum_answers').update({'likes': new_likes}).eq('id', answer_id).execute()
                return jsonify({'liked': True, 'likes': new_likes}), 200
        
        return jsonify({'error': 'Answer not found'}), 404
        
    except Exception as e:
        print(f"Error liking answer: {str(e)}")
        return jsonify({'error': str(e)}), 500
    

# Get user's question likes
@app.route('/api/forum/question-likes/user', methods=['GET'])
@token_required
def get_user_question_likes(current_user):
    try:
        # Get all question likes for the current user
        response = supabase.table('forum_question_likes').select('question_id, user_id').eq('user_id', current_user).execute()
        
        return jsonify(response.data if response.data else []), 200
        
    except Exception as e:
        print(f"Error fetching user question likes: {str(e)}")
        return jsonify({'error': str(e)}), 500


# Get user's answer likes
@app.route('/api/forum/answer-likes/user', methods=['GET'])
@token_required
def get_user_answer_likes(current_user):
    try:
        # Get all answer likes for the current user
        response = supabase.table('forum_answer_likes').select('answer_id, user_id').eq('user_id', current_user).execute()
        
        return jsonify(response.data if response.data else []), 200
        
    except Exception as e:
        print(f"Error fetching user answer likes: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)  

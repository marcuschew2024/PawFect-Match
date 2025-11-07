<template>
  <div class="adoption-form-page">
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="adoption-header text-center mb-5">
            <h1>Adopt {{ pet.name }}</h1>
            <p class="lead">Complete this form to adopt {{ pet.name }} and give them a forever home</p>
          </div>

          <!-- Loading State -->
          <div v-if="loadingPet" class="text-center">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Loading pet details...</p>
          </div>

          <div v-else-if="petError" class="alert alert-danger text-center">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ petError }}
            <div class="mt-3">
              <router-link to="/pets" class="btn btn-primary">Browse Available Pets</router-link>
            </div>
          </div>

          <div v-else class="adoption-card">
            <!-- Pet Summary -->
            <div class="pet-summary mb-4 p-4 bg-light rounded">
              <div class="row align-items-center">
                <div class="col-md-3">
                  <div class="position-relative">
                    <img :src="pet.displayImage" 
                         :alt="pet.name" 
                         class="img-fluid rounded"
                         style="height: 120px; width: 100%; object-fit: cover;"
                         :class="{ 'image-loaded': pet.imageLoaded }"
                         @load="onImageLoad"
                         @error="onImageError">
                    
                    <!-- Image Source Badge -->
                    <div v-if="pet.imageLoaded && pet.imageSource === 'api'" class="api-badge-small">
                      AI Generated
                    </div>
                    <div v-else-if="pet.imageLoaded && pet.imageSource === 'database'" class="api-badge-small database-badge">
                      Real Image
                    </div>

                    <!-- Loading Spinner -->
                    <div v-if="!pet.imageLoaded" class="image-loading-small">
                      <i class="bi bi-arrow-repeat spinner"></i>
                    </div>
                  </div>
                </div>
                <div class="col-md-9">
                  <h4>{{ pet.name }}</h4>
                  <p class="mb-1"><strong>Breed:</strong> {{ pet.breed }}</p>
                  <p class="mb-1"><strong>Age:</strong> {{ pet.age }}</p>
                  <p class="mb-1"><strong>Size:</strong> {{ pet.size }}</p>
                  <p class="mb-0"><strong>Personality:</strong> {{ pet.personality }}</p>
                  
                  <!-- Adoption Status -->
                  <div v-if="pet.is_adopted" class="mt-2">
                    <span class="badge bg-danger">Already Adopted</span>
                  </div>
                  <div v-else class="mt-2">
                    <span class="badge bg-success">Available for Adoption</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Show form only if pet is available -->
            <div v-if="!pet.is_adopted">
              <form @submit.prevent="submitAdoption" class="adoption-form">
                <!-- NEW: Block notice when rejected -->
                <div v-if="existingStatus === 'rejected'" class="alert alert-danger mb-4">
                  <i class="bi bi-x-circle me-2"></i>
                  Your previous application for {{ pet.name }} was <strong>rejected</strong>. You can’t submit another application for this pet.
                </div>

                <!-- Personal Information -->
                <div class="form-section mb-4">
                  <h4 class="section-title">Personal Information</h4>
                  
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="applicantName" class="form-label">Full Name *</label>
                      <input type="text" class="form-control" id="applicantName" 
                             v-model="form.applicant_name" 
                             :class="{ 'is-invalid': errors.applicant_name }"
                             required>
                      <div class="invalid-feedback" v-if="errors.applicant_name">
                        {{ errors.applicant_name }}
                      </div>
                    </div>
                    
                    <div class="col-md-6 mb-3">
                      <label for="applicantEmail" class="form-label">Email Address *</label>
                      <input type="email" class="form-control" id="applicantEmail" 
                             v-model="form.applicant_email"
                             :class="{ 'is-invalid': errors.applicant_email }"
                             required>
                      <div class="invalid-feedback" v-if="errors.applicant_email">
                        {{ errors.applicant_email }}
                      </div>
                    </div>
                  </div>

                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label for="applicantPhone" class="form-label">Phone Number *</label>
                      <input type="tel" class="form-control" id="applicantPhone" 
                             v-model="form.applicant_phone"
                             :class="{ 'is-invalid': errors.applicant_phone }"
                             required>
                      <div class="invalid-feedback" v-if="errors.applicant_phone">
                        {{ errors.applicant_phone }}
                      </div>
                    </div>
                    
                    <div class="col-md-6 mb-3">
                      <label for="applicantAddress" class="form-label">Address *</label>
                      <textarea class="form-control" id="applicantAddress" 
                             v-model="form.applicant_address"
                             :class="{ 'is-invalid': errors.applicant_address }"
                             required
                             rows="2"
                             placeholder="Street, City, Postal Code"></textarea>
                      <div class="invalid-feedback" v-if="errors.applicant_address">
                        {{ errors.applicant_address }}
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Living Situation -->
                <div class="form-section mb-4">
                  <h4 class="section-title">Living Situation</h4>
                  
                  <div class="mb-3">
                    <label for="livingSituation" class="form-label">Describe your living situation *</label>
                    <textarea class="form-control" id="livingSituation" rows="3" 
                              v-model="form.living_situation"
                              :class="{ 'is-invalid': errors.living_situation }"
                              required
                              placeholder="Tell us about your home, yard space, and any restrictions..."></textarea>
                    <div class="invalid-feedback" v-if="errors.living_situation">
                      {{ errors.living_situation }}
                    </div>
                    <div class="form-text">Include details about your home type, yard space, and any pet restrictions</div>
                  </div>
                </div>

                <!-- Pet Experience -->
                <div class="form-section mb-4">
                  <h4 class="section-title">Pet Experience</h4>
                  
                  <div class="mb-3">
                    <label for="petExperience" class="form-label">Your experience with pets *</label>
                    <textarea class="form-control" id="petExperience" rows="3" 
                              v-model="form.experience_with_pets"
                              :class="{ 'is-invalid': errors.experience_with_pets }"
                              required
                              placeholder="Tell us about your experience with pets..."></textarea>
                    <div class="invalid-feedback" v-if="errors.experience_with_pets">
                      {{ errors.experience_with_pets }}
                    </div>
                    <div class="form-text">Have you owned pets before? What types? For how long?</div>
                  </div>
                </div>

                <!-- Adoption Reason -->
                <div class="form-section mb-4">
                  <h4 class="section-title">Adoption Reason</h4>
                  
                  <div class="mb-3">
                    <label for="adoptionReason" class="form-label">Why do you want to adopt {{ pet.name }}? *</label>
                    <textarea class="form-control" id="adoptionReason" rows="3" 
                              v-model="form.reason_for_adoption"
                              :class="{ 'is-invalid': errors.reason_for_adoption }"
                              required
                              placeholder="Tell us why you're interested in adopting this pet..."></textarea>
                    <div class="invalid-feedback" v-if="errors.reason_for_adoption">
                      {{ errors.reason_for_adoption }}
                    </div>
                    <div class="form-text">What makes you a good match for this pet?</div>
                  </div>
                </div>

                <!-- Terms and Conditions -->
                <div class="form-section mb-4">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" id="termsAgreement" 
                           v-model="form.agree_terms"
                           :class="{ 'is-invalid': errors.agree_terms }"
                           required>
                    <label class="form-check-label" for="termsAgreement">
                      I understand that I am committing to provide a loving and responsible home for {{ pet.name }}. 
                      I agree to care for this pet's needs including food, shelter, medical care, and companionship.
                    </label>
                    <div class="invalid-feedback" v-if="errors.agree_terms">
                      {{ errors.agree_terms }}
                    </div>
                  </div>
                </div>

                <!-- Success Message -->
                <div v-if="success" class="alert alert-success">
                  <i class="bi bi-check-circle me-2"></i>
                  {{ success }}
                  <div class="mt-2">
                    <router-link to="/profile?tab=pending" class="btn btn-success me-2">
                      View My Applications
                    </router-link>
                    <router-link to="/pets" class="btn btn-outline-primary">
                      Browse More Pets
                    </router-link>
                  </div>
                </div>

                <!-- Error Message -->
                <div v-if="error" class="alert alert-danger">
                  <i class="bi bi-exclamation-triangle me-2"></i>
                  {{ error }}
                </div>

                <!-- Submit Button -->
                <div class="d-grid" v-if="!success">
                  <button
                    type="submit"
                    class="btn btn-success btn-lg"
                    :disabled="loading || existingStatus === 'rejected'"
                  >
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                    {{
                      existingStatus === 'rejected'
                        ? 'Application rejected — resubmission not allowed'
                        : (loading ? 'Submitting Adoption...' : `Adopt ${pet.name}`)
                    }}
                  </button>
                </div>
              </form>
            </div>

            <!-- Show message if pet is already adopted -->
            <div v-else class="alert alert-warning text-center">
              <i class="bi bi-info-circle me-2"></i>
              This pet has already been adopted and is no longer available.
              <div class="mt-3">
                <router-link to="/pets" class="btn btn-primary">
                  Browse Available Pets
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const API_BASE_URL = 'http://localhost:3000/api';

export default {
  name: 'AdoptionFormPage',
  data() {
    return {
      pet: {
        displayImage: '',
        imageLoaded: false,
        placeholderImage: true,
        imageSource: 'placeholder'
      },
      form: {
        applicant_name: '',
        applicant_email: '',
        applicant_phone: '',
        applicant_address: '',
        living_situation: '',
        experience_with_pets: '',
        reason_for_adoption: '',
        agree_terms: false
      },
      errors: {},
      loading: false,
      loadingPet: true,
      error: null,
      success: null,
      petError: null,
      imageCache: new Map(),
      allDogBreeds: [],
      allCatBreeds: [],
      // NEW: track prior application status
      existingStatus: null,   // 'pending' | 'approved' | 'rejected' | null
    }
  },
  async mounted() {
    const petId = this.$route.params.petId;
    await this.loadAllBreeds();
    await this.loadPetDetails(petId);

    // NEW: check if user has an existing application for this pet
    await this.checkExistingApplication(petId);
    
    // Pre-fill user data if available
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if (user) {
      this.form.applicant_name = user.full_name || '';
      this.form.applicant_email = user.email || '';
      this.form.applicant_phone = user.phone || '';
      this.form.applicant_address = user.address || '';
    }
  },
  methods: {
    async loadPetDetails(petId) {
      this.loadingPet = true;
      this.petError = null;
      
      try {
        const response = await fetch(`${API_BASE_URL}/pets/${petId}`);
        if (response.ok) {
          const petData = await response.json();
          this.pet = await this.processPetWithImages(petData);
          
          // Check if pet is already adopted
          if (this.pet.is_adopted) {
            this.petError = `${this.pet.name} has already been adopted by someone else.`;
          }
        } else {
          this.petError = 'Pet not found.';
        }
      } catch (error) {
        console.error('Error loading pet details:', error);
        this.petError = 'Error loading pet details. Please check if the server is running.';
      } finally {
        this.loadingPet = false;
      }
    },

    // NEW: query the user's existing application (if any) for this pet
    async checkExistingApplication(petId) {
      try {
        const token = localStorage.getItem('authToken');
        if (!token) return;

        const r = await fetch(`${API_BASE_URL}/adoption-applications/mine?pet_id=${encodeURIComponent(petId)}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });

        if (r.ok) {
          // Expect either null/{} if none, or an object with 'status'
          const app = await r.json();
          if (app && app.status) {
            this.existingStatus = String(app.status).toLowerCase();
          } else {
            this.existingStatus = null;
          }
        } else {
          // ignore non-200s silently
          this.existingStatus = null;
        }
      } catch (e) {
        console.warn('checkExistingApplication failed:', e);
        this.existingStatus = null;
      }
    },

    async processPetWithImages(pet) {
      let displayImage = null;
      let imageSource = 'placeholder';

      if (pet.main_image && pet.main_image.trim() !== '') {
        displayImage = pet.main_image;
        imageSource = 'database';
      } else if (pet.image && pet.image.trim() !== '') {
        displayImage = pet.image;
        imageSource = 'database';
      } else {
        displayImage = this.getColoredPlaceholder(pet);
        imageSource = 'placeholder';
      }

      const processedPet = {
        ...pet,
        displayImage: displayImage,
        imageLoaded: false,
        placeholderImage: imageSource === 'placeholder',
        imageSource: imageSource
      };

      // If it's a placeholder, try to fetch API image
      if (imageSource === 'placeholder') {
        this.fetchApiImageForPet(processedPet);
      }

      return processedPet;
    },

    async fetchApiImageForPet(pet) {
      try {
        const apiImage = await this.fetchPetImage(pet);
        if (apiImage) {
          pet.displayImage = apiImage;
          pet.image = apiImage;
          pet.placeholderImage = false;
          pet.imageSource = 'api';
          this.$forceUpdate();
        } else {
          pet.displayImage = this.getColoredPlaceholder(pet);
          pet.placeholderImage = false;
        }
      } catch (error) {
        console.error(`Error fetching API image for ${pet.name}:`, error);
        pet.displayImage = this.getColoredPlaceholder(pet);
        pet.placeholderImage = false;
      }
    },

    async fetchPetImage(pet) {
      const cacheKey = `${pet.type}-${pet.breed}`;
      if (this.imageCache.has(cacheKey)) {
        return this.imageCache.get(cacheKey);
      }

      try {
        const breedId = this.findBreedId(pet.breed, pet.type);
        const apiUrl = pet.type === "dog"
          ? `${API_BASE_URL}/external/dog-images`
          : `${API_BASE_URL}/external/cat-images`;

        const params = new URLSearchParams({ limit: "1" });
        if (breedId) params.append("breed_id", breedId);

        const token = localStorage.getItem('authToken');
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`${apiUrl}?${params}`, { headers });

        if (!response.ok) {
          console.warn(`API error for ${pet.name}: ${response.status}`);
          return "";
        }

        const data = await response.json();
        if (data && data.length > 0 && data[0].url) {
          const imageUrl = data[0].url;
          this.imageCache.set(cacheKey, imageUrl);
          return imageUrl;
        }
        
        console.log(`No image found for ${pet.name}`);
        return "";
      } catch (error) {
        console.error(`Error fetching image for ${pet.name}:`, error);
        return "";
      }
    },

    findBreedId(breedName, type) {
      const breeds = type === "dog" ? this.allDogBreeds : this.allCatBreeds;

      if (!breeds || !breeds.length) {
        console.warn(`No breeds loaded for type: ${type}`);
        return null;
      }

      try {
        const normalizedBreedName = breedName.toString().toLowerCase().trim();

        if (!normalizedBreedName) {
          return null;
        }

        let breed = breeds.find(b =>
          b.name && b.name.toString().toLowerCase().trim() === normalizedBreedName
        );

        if (breed) {
          return breed.id;
        }

        breed = breeds.find(b => {
          if (!b.name) return false;
          const apiName = b.name.toString().toLowerCase().trim();
          return apiName.includes(normalizedBreedName) && normalizedBreedName.length >= 3;
        });

        if (breed) {
          return breed.id;
        }

        breed = breeds.find(b => {
          if (!b.name) return false;
          const apiName = b.name.toString().toLowerCase().trim();
          return normalizedBreedName.includes(apiName) && apiName.length >= 3;
        });

        if (breed) {
          return breed.id;
        }

        const breedWords = normalizedBreedName.split(/\s+/).filter(word => word.length >= 3);
        if (breedWords.length > 0) {
          breed = breeds.find(b => {
            if (!b.name) return false;
            const apiWords = b.name.toString().toLowerCase().trim().split(/\s+/);
            return breedWords.some(word => apiWords.includes(word));
          });

          if (breed) {
            return breed.id;
          }
        }

        console.log(`No breed match found for: ${breedName} (${type})`);
        return null;
      } catch (error) {
        console.error('Error in findBreedId:', error, { breedName, type });
        return null;
      }
    },

    async loadAllBreeds() {
      try {
        const token = localStorage.getItem('authToken');
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const [dogResponse, catResponse] = await Promise.all([
          fetch(`${API_BASE_URL}/external/dog-breeds`, { headers }),
          fetch(`${API_BASE_URL}/external/cat-breeds`, { headers })
        ]);

        if (dogResponse.ok) {
          this.allDogBreeds = await dogResponse.json();
        }

        if (catResponse.ok) {
          this.allCatBreeds = await catResponse.json();
        }

      } catch (error) {
        console.error("Error fetching breed lists:", error);
      }
    },

    onImageLoad() {
      this.pet.imageLoaded = true;
      this.$forceUpdate();
    },

    onImageError() {
      if (this.pet.imageSource === 'database') {
        this.pet.placeholderImage = true;
        this.pet.imageSource = 'placeholder';
        this.fetchApiImageForPet(this.pet);
      } else if (this.pet.imageSource === 'api') {
        this.pet.displayImage = this.getColoredPlaceholder(this.pet);
        this.pet.placeholderImage = false;
      } else {
        this.pet.displayImage = this.getColoredPlaceholder(this.pet);
        this.pet.placeholderImage = false;
      }

      this.pet.imageLoaded = true;
      this.$forceUpdate();
    },
    
    validateForm() {
      this.errors = {};
      
      const requiredFields = [
        'applicant_name', 'applicant_email', 'applicant_phone', 'applicant_address',
        'living_situation', 'experience_with_pets', 'reason_for_adoption'
      ];
      
      requiredFields.forEach(field => {
        if (!this.form[field] || this.form[field].trim() === '') {
          this.errors[field] = 'This field is required';
        }
      });
      
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (this.form.applicant_email && !emailRegex.test(this.form.applicant_email)) {
        this.errors.applicant_email = 'Please enter a valid email address';
      }
      
      if (!this.form.agree_terms) {
        this.errors.agree_terms = 'You must agree to the terms and conditions';
      }
      
      return Object.keys(this.errors).length === 0;
    },
    
    async submitAdoption() {
      // NEW: hard block if previously rejected
      if (this.existingStatus === 'rejected') {
        this.error = `Your previous application for ${this.pet.name} was rejected. You can't submit another application for this pet.`;
        return;
      }

      // Validate form before submission
      if (!this.validateForm()) {
        this.error = 'Please fix the errors in the form before submitting.';
        return;
      }
      
      this.loading = true;
      this.error = null;
      this.success = null;
      
      try {
        const token = localStorage.getItem('authToken');
        if (!token) {
          this.error = 'Please log in to adopt a pet.';
          this.$router.push('/login');
          return;
        }
        
        const response = await fetch(`${API_BASE_URL}/adopt/${this.pet.id}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            applicant_name: this.form.applicant_name,
            applicant_email: this.form.applicant_email,
            applicant_phone: this.form.applicant_phone,
            applicant_address: this.form.applicant_address,
            living_situation: this.form.living_situation,
            experience_with_pets: this.form.experience_with_pets,
            reason_for_adoption: this.form.reason_for_adoption
          })
        });
        
        if (response.ok) {
          const result = await response.json();
          this.success = result.message || `Adoption application submitted for ${this.pet.name}! Your application is pending admin approval.`;
          
          // Clear form
          this.form = {
            applicant_name: '',
            applicant_email: '',
            applicant_phone: '',
            applicant_address: '',
            living_situation: '',
            experience_with_pets: '',
            reason_for_adoption: '',
            agree_terms: false
          };

          // Refresh existing status (in case backend decided something)
          await this.checkExistingApplication(this.pet.id);
          
          setTimeout(() => {
            this.$router.push('/profile?tab=pending');
          }, 2000);
          
        } else {
          const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));

          // Handle unique constraint / already applied
          const duplicate =
            response.status === 409 ||
            (errorData?.error && String(errorData.error).includes('23505')) ||
            (errorData?.message && String(errorData.message).toLowerCase().includes('duplicate key')) ||
            (errorData?.details && String(errorData.details).toLowerCase().includes('already exists'));

          if (duplicate) {
            // If backend returns previous application in payload, respect its status
            const prevStatus = (errorData?.application?.status || '').toLowerCase();
            if (prevStatus === 'rejected' || this.existingStatus === 'rejected') {
              this.existingStatus = 'rejected';
              this.error = `Your previous application for ${this.pet.name} was rejected. You can't submit another application for this pet.`;
            } else {
              this.error = `You are not eligble to apply for ${this.pet.name} again.`;
            }
            return;
          }

          this.error = errorData.error || `Adoption application failed with status: ${response.status}`;
          
          if (response.status === 401) {
            this.$router.push('/login');
          }
        }
      } catch (error) {
        console.error('Error submitting adoption application:', error);
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
          this.error = 'Cannot connect to server. Please make sure the backend is running on port 3000.';
        } else {
          this.error = 'Network error. Please try again.';
        }
      } finally {
        this.loading = false;
      }
    },
    
    getColoredPlaceholder(pet) {
      const colors = {
        dog: ['#ffb6c1', '#ffd1dc', '#ffecb3', '#c8e6c9'],
        cat: ['#bbdefb', '#c5cae9', '#e1bee7', '#f8bbd0']
      };
      const typeColors = colors[pet.type] || colors.dog;
      const colorIndex = pet.id ? (typeof pet.id === 'number' ? pet.id : 
                        pet.id.toString().split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)) : 0;
      const color = typeColors[colorIndex % typeColors.length];
      const emoji = pet.type === 'dog' ? '🐕' : '🐱';
      
      return `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='250' viewBox='0 0 300 250'%3E%3Crect fill='${color}' width='300' height='250'/%3E%3Ctext fill='%23666' font-size='24' font-family='system-ui' x='150' y='125' text-anchor='middle' dominant-baseline='middle'%3E${emoji}%3C/text%3E%3Ctext fill='%23333' font-size='16' font-family='system-ui' x='150' y='160' text-anchor='middle'%3E${pet.name}%3C/text%3E%3C/svg%3E`;
    }
  }
}
</script>

<style scoped>
.adoption-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(255, 182, 193, 0.15);
  border: 1px solid var(--border-light);
}

.adoption-header h1 {
  color: var(--text-dark);
  font-weight: 700;
}

.section-title {
  color: var(--primary-pink-dark);
  border-bottom: 2px solid var(--primary-pink);
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
}

.form-section {
  padding: 1.5rem;
  border: 1px solid var(--border-light);
  border-radius: 8px;
  background: var(--background-light);
}

.pet-summary {
  background: linear-gradient(135deg, #ffeef1, #fff5f7);
  border: 1px solid var(--border-light);
}

.form-control:focus {
  border-color: var(--primary-pink);
  box-shadow: 0 0 0 0.2rem rgba(255, 182, 193, 0.25);
}

.btn-success {
  background: linear-gradient(135deg, #ff868a 0%, #ffa6a6 100%);
  color: white;
  border: none;
  padding: 12px 25px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-success:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 154, 158, 0.4);
  background: linear-gradient(135deg, #eb7e7e 0%, #FF9A9E 100%);
  color: white;
}

.btn-success:disabled {
  background: #6c757d;
  transform: none;
  box-shadow: none;
}

/* Image loading styles */
.api-badge-small {
  position: absolute;
  top: 8px;
  right: 8px;
  background-color: rgba(255, 255, 255, 0.95);
  color: var(--text-light);
  font-size: 0.6rem;
  font-weight: 500;
  padding: 3px 6px;
  border-radius: 8px;
  border: 1px solid var(--border-light);
  z-index: 3;
}

.database-badge {
  background-color: rgba(76, 175, 80, 0.95) !important;
  color: white !important;
}

.image-loading-small {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #666;
  font-size: 1rem;
  z-index: 2;
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.position-relative {
  position: relative;
}
</style>

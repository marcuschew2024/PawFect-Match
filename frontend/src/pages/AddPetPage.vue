<template>
  <div class="add-adoption-page">
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="adoption-header text-center mb-5">
            <h1>Add a Pet for Adoption</h1>
            <p class="lead">Help a furry friend find their forever home by listing them for adoption</p>
          </div>

          <div class="adoption-card">
            <form @submit.prevent="submitPet" class="adoption-form">
              <!-- Basic Information -->
              <div class="form-section mb-4">
                <h4 class="section-title">Basic Information</h4>
                
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="petName" class="form-label">Pet Name *</label>
                    <input type="text" class="form-control" id="petName" 
                           v-model="form.name" required>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label for="petType" class="form-label">Pet Type *</label>
                    <select class="form-select" id="petType" v-model="form.type" required>
                      <option value="">Select Type</option>
                      <option value="dog">Dog</option>
                      <option value="cat">Cat</option>
                    </select>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="petBreed" class="form-label">Breed *</label>
                    <input type="text" class="form-control" id="petBreed" 
                           v-model="form.breed" required>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label for="petAge" class="form-label">Age *</label>
                    <input type="text" class="form-control" id="petAge" 
                           v-model="form.age" required placeholder="e.g., 2 years, 6 months">
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="petSize" class="form-label">Size *</label>
                    <select class="form-select" id="petSize" v-model="form.size" required>
                      <option value="">Select Size</option>
                      <option value="Small">Small</option>
                      <option value="Medium">Medium</option>
                      <option value="Large">Large</option>
                    </select>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label for="petGender" class="form-label">Gender *</label>
                    <select class="form-select" id="petGender" v-model="form.gender" required>
                      <option value="">Select Gender</option>
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- Additional Details -->
              <div class="form-section mb-4">
                <h4 class="section-title">Additional Details</h4>
                
                <div class="mb-3">
                  <label for="petPersonality" class="form-label">Personality & Description *</label>
                  <textarea class="form-control" id="petPersonality" rows="3" 
                            v-model="form.personality" required
                            placeholder="Describe the pet's personality, temperament, and any special characteristics..."></textarea>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="petActivity" class="form-label">Activity Level</label>
                    <select class="form-select" id="petActivity" v-model="form.activity_level">
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                    </select>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label for="petColor" class="form-label">Fur Color</label>
                    <input type="text" class="form-control" id="petColor" 
                           v-model="form.furColor" placeholder="e.g., Brown, Black, White">
                  </div>
                </div>
              </div>

              <!-- Health & Adoption Info -->
              <div class="form-section mb-4">
                <h4 class="section-title">Health & Adoption Information</h4>
                
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="vaccinationStatus" class="form-label">Vaccination Status</label>
                    <select class="form-select" id="vaccinationStatus" v-model="form.vaccination_status">
                      <option value="Up to date">Up to date</option>
                      <option value="Partially vaccinated">Partially vaccinated</option>
                      <option value="Not vaccinated">Not vaccinated</option>
                      <option value="Unknown">Unknown</option>
                    </select>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label for="adoptionFee" class="form-label">Adoption Fee ($)</label>
                    <input type="number" class="form-control" id="adoptionFee" 
                           v-model="form.adoption_fee" min="0" step="0.01" placeholder="0.00">
                  </div>
                </div>

                <div class="mb-3">
                  <label for="healthInfo" class="form-label">Health Information</label>
                  <textarea class="form-control" id="healthInfo" rows="2" 
                            v-model="form.health_info"
                            placeholder="Any health conditions, medications, or special care requirements..."></textarea>
                </div>

                <div class="mb-3">
                  <label for="petLocation" class="form-label">Location</label>
                  <input type="text" class="form-control" id="petLocation" 
                         v-model="form.location" placeholder="e.g., Singapore, Central Area">
                </div>
              </div>

              <!-- Image Upload -->
              <div class="form-section mb-4">
                <h4 class="section-title">Pet Image</h4>
                
                <div class="mb-3">
                  <label for="petImage" class="form-label">Image URL</label>
                  <input type="url" class="form-control" id="petImage" 
                         v-model="form.image" 
                         placeholder="https://example.com/pet-image.jpg">
                  <div class="form-text">Provide a direct URL to the pet's photo</div>
                </div>

                <div v-if="form.image" class="image-preview mt-3">
                  <img :src="form.image" alt="Preview" class="img-thumbnail" style="max-height: 200px;">
                </div>
              </div>

              <!-- Error Message -->
              <div v-if="error" class="alert alert-danger">
                {{ error }}
              </div>

              <!-- Success Message -->
              <div v-if="success" class="alert alert-success">
                <i class="bi bi-check-circle me-2"></i>
                {{ success }}
              </div>

              <!-- Submit Button -->
              <div class="d-grid">
                <button type="submit" class="btn btn-primary btn-lg" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ loading ? 'Adding Pet...' : 'Add Pet for Adoption' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const API_BASE_URL = 'http://localhost:3000/api';

export default {
  name: 'AddAdoptionPage',
  data() {
    return {
      form: {
        name: '',
        type: '',
        breed: '',
        age: '',
        size: '',
        gender: '',
        personality: '',
        activity_level: 'medium',
        furColor: '',
        vaccination_status: 'Up to date',
        adoption_fee: 0,
        health_info: '',
        location: 'Singapore',
        image: ''
      },
      loading: false,
      error: null,
      success: null
    }
  },
  methods: {
    async submitPet() {
  this.loading = true;
  this.error = null;
  this.success = null;
  
  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      this.$router.push('/login');
      return;
    }
    
    console.log('Submitting pet data:', this.form); // Debug log
    
    const response = await fetch(`${API_BASE_URL}/pets`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(this.form)
    });
    
    console.log('Response status:', response.status); // Debug log
    
    if (response.ok) {
      const newPet = await response.json();
      console.log('Successfully created pet:', newPet); // Debug log
      this.success = `Successfully added ${newPet.name} for adoption!`;
      this.resetForm();
      
      // Optional: Redirect to pet listing after success
      setTimeout(() => {
        this.$router.push('/pets');
      }, 2000);
    } else {
      const error = await response.json();
      console.error('Server error:', error); // Debug log
      this.error = error.error || `Failed to add pet for adoption (Status: ${response.status})`;
    }
  } catch (error) {
    console.error('Error adding pet:', error);
    this.error = 'Network error. Please try again.';
  } finally {
    this.loading = false;
  }
},
    
    resetForm() {
      this.form = {
        name: '',
        type: '',
        breed: '',
        age: '',
        size: '',
        gender: '',
        personality: '',
        activity_level: 'medium',
        furColor: '',
        vaccination_status: 'Up to date',
        adoption_fee: 0,
        health_info: '',
        location: 'Singapore',
        image: ''
      };
    }
  }
}
</script>

<style scoped>
.add-adoption-page {
  min-height: 80vh;
}

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

.form-control:focus,
.form-select:focus {
  border-color: var(--primary-pink);
  box-shadow: 0 0 0 0.2rem rgba(255, 182, 193, 0.25);
}

.btn-primary {
  background: var(--primary-pink);
  border-color: var(--primary-pink);
  padding: 1rem 2rem;
  font-weight: 600;
}

.btn-primary:hover {
  background: var(--primary-pink-dark);
  border-color: var(--primary-pink-dark);
}

.image-preview {
  text-align: center;
}

.image-preview img {
  border-radius: 8px;
  border: 2px solid var(--border-light);
}
</style>
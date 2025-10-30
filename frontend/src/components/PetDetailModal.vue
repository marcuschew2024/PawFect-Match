<template>
  <!-- Hello guys just wondering if this page is useful at all? i dont think it appears in our webpage rightt -->
  <div class="modal fade" id="petDetailModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ pet?.name || 'Pet Details' }}</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div v-if="loading" class="text-center">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
          
          <div v-else-if="error" class="alert alert-danger">
            {{ error }}
          </div>
          
          <div v-else-if="!pet" class="text-center">
            <p>No pet information available.</p>
          </div>
          
          <div v-else class="row">
            <div class="col-md-6">
              <img :src="petDetails.displayImage || petDetails.image" 
                   :alt="petDetails.name" 
                   class="img-fluid rounded mb-3"
                   @error="onImageError">
              
              <div v-if="hasCompletedQuiz && petDetails.compatibility_score" class="compatibility-section mb-3">
                <h6>Compatibility Score</h6>
                <div class="progress mb-2">
                  <div class="progress-bar bg-primary" 
                       :style="{ width: petDetails.compatibility_score + '%' }">
                    {{ petDetails.compatibility_score }}%
                  </div>
                </div>
                <small class="text-muted">Based on your lifestyle quiz</small>
              </div>
            </div>
            
            <div class="col-md-6">
              <h6>Basic Information</h6>
              <ul class="list-unstyled">
                <li><strong>Breed:</strong> {{ petDetails.breed }}</li>
                <li><strong>Age:</strong> {{ petDetails.age }}</li>
                <li><strong>Size:</strong> {{ petDetails.size }}</li>
                <li><strong>Gender:</strong> {{ petDetails.gender }}</li>
                <li><strong>Type:</strong> {{ petDetails.type }}</li>
                <li v-if="petDetails.fur_color"><strong>Color:</strong> {{ petDetails.fur_color }}</li>
              </ul>
              
              <h6 class="mt-4">Health & Care</h6>
              <ul class="list-unstyled">
                <li><strong>Vaccination:</strong> {{ petDetails.vaccination_status || 'Not specified' }}</li>
                <li><strong>Adoption Fee:</strong> ${{ petDetails.adoption_fee || '0' }}</li>
                <li><strong>Location:</strong> {{ petDetails.location || 'Not specified' }}</li>
                <li v-if="petDetails.health_info"><strong>Health Info:</strong> {{ petDetails.health_info }}</li>
              </ul>
              
              <h6 class="mt-4">Personality</h6>
              <p class="personality-text">"{{ petDetails.personality }}"</p>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button v-if="isAuthenticated && petDetails && !petDetails.is_adopted" 
                  class="btn btn-primary" 
                  @click="startAdoption">
            <i class="bi bi-heart me-2"></i>Adopt {{ petDetails.name }}
          </button>
          <button v-else-if="petDetails && petDetails.is_adopted" 
                  class="btn btn-success" disabled>
            <i class="bi bi-check-circle me-2"></i>Already Adopted
          </button>
          <button v-else-if="petDetails"
                  class="btn btn-outline-primary"
                  @click="$router.push('/login')">
            <i class="bi bi-person me-2"></i>Login to Adopt
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const API_BASE_URL = 'http://localhost:3000/api';

export default {
  name: 'PetDetailModal',
  props: {
    pet: {
      type: Object,
      required: false,
      default: null
    },
    isAuthenticated: {
      type: Boolean,
      default: false
    },
    hasCompletedQuiz: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      petDetails: {},
      loading: false,
      error: null
    }
  },
  methods: {
    async loadPetDetails() {
      if (!this.pet) {
        this.error = 'No pet selected';
        return;
      }

      this.loading = true;
      this.error = null;
      
      try {
        const token = localStorage.getItem('authToken');
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;
        
        let url = `${API_BASE_URL}/pets/${this.pet.id}/details`;
        if (this.isAuthenticated && this.hasCompletedQuiz) {
          url = `${API_BASE_URL}/pets/with-scores`;
        }
        
        const response = await fetch(url, { headers });
        
        if (!response.ok) {
          throw new Error('Failed to load pet details');
        }
        
        const data = await response.json();
        
        if (Array.isArray(data)) {
          // If we got the with-scores array, find the specific pet
          this.petDetails = data.find(p => p.id === this.pet.id) || this.pet;
        } else {
          this.petDetails = data;
        }
        
        // Ensure displayImage is set
        if (!this.petDetails.displayImage && this.petDetails.image) {
          this.petDetails.displayImage = this.petDetails.image;
        }
        
      } catch (error) {
        console.error('Error loading pet details:', error);
        this.error = 'Failed to load pet details';
        this.petDetails = { ...this.pet };
      } finally {
        this.loading = false;
      }
    },
    
    onImageError() {
      if (this.petDetails.displayImage) {
        this.petDetails.displayImage = this.getColoredPlaceholder(this.petDetails);
      }
    },
    
    getColoredPlaceholder(pet) {
      const colors = {
        dog: ['#ffb6c1', '#ffd1dc', '#ffecb3', '#c8e6c9'],
        cat: ['#bbdefb', '#c5cae9', '#e1bee7', '#f8bbd0']
      };
      const typeColors = colors[pet.type] || colors.dog;
      const color = typeColors[pet.id % typeColors.length];
      const emoji = pet.type === 'dog' ? '🐕' : '🐱';
      
      return `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='250' viewBox='0 0 300 250'%3E%3Crect fill='${color}' width='300' height='250'/%3E%3Ctext fill='%23666' font-size='24' font-family='system-ui' x='150' y='125' text-anchor='middle' dominant-baseline='middle'%3E${emoji}%3C/text%3E%3Ctext fill='%23333' font-size='16' font-family='system-ui' x='150' y='160' text-anchor='middle'%3E${pet.name}%3C/text%3E%3C/svg%3E`;
    },
    
    startAdoption() {
      if (this.petDetails) {
        this.$emit('start-adoption', this.petDetails);
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('petDetailModal'));
        if (modal) {
          modal.hide();
        }
      }
    },
    
    show() {
      this.loadPetDetails();
      const modalElement = document.getElementById('petDetailModal');
      if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
      }
    }
  }
}
</script>

<style scoped>
.personality-text {
  font-style: italic;
  color: #666;
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid var(--primary-pink);
}

.compatibility-section {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
}

.modal-content {
  border-radius: 12px;
  border: none;
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.modal-header {
  background: linear-gradient(135deg, var(--primary-pink), #ff9aa2);
  color: white;
  border-bottom: none;
  border-radius: 12px 12px 0 0;
}

.modal-header .btn-close {
  filter: invert(1);
}
</style>
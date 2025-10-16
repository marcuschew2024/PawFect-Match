<template>
  <div class="pet-profile-page">
    <div class="container my-4">
      <!-- Back Button -->
      <div class="mb-4">
        <button @click="$router.back()" class="btn btn-outline-secondary btn-sm">
          <i class="bi bi-arrow-left me-2"></i>Back to Pets
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Loading pet details...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="alert alert-danger text-center">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
        <div class="mt-3">
          <router-link to="/pets" class="btn btn-primary">Browse All Pets</router-link>
        </div>
      </div>

      <!-- Pet Profile Content -->
      <div v-else-if="pet" class="row g-4">
        <!-- Left Column - Pet Image & Actions -->
        <div class="col-xl-5 col-lg-6">
          <div class="card shadow-sm border-0">
            <div class="card-body p-0">
              <div class="pet-image-container position-relative">
                <img 
                  :src="pet.displayImage" 
                  :alt="pet.name"
                  class="card-img-top pet-image"
                  :class="{ 'image-loaded': pet.imageLoaded }"
                  @load="onImageLoad(pet)"
                  @error="onImageError(pet)"
                  loading="lazy"
                />
                
                <!-- Image Loading Overlay -->
                <div v-if="!pet.imageLoaded" class="image-loading-overlay">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading image...</span>
                  </div>
                  <p class="mt-2 small">Loading image...</p>
                </div>

                <!-- API Badge for placeholder images -->
                <div v-if="pet.placeholderImage && pet.imageLoaded" class="api-badge">
                  Breed Image
                </div>

                <!-- Compatibility Badge -->
                <div v-if="hasCompletedQuiz && pet.compatibility_score" 
                     class="compatibility-badge">
                  {{ pet.compatibility_score }}% Match
                </div>

                <!-- Adoption Status Badge -->
                <div v-if="pet.is_adopted" class="status-badge adopted">
                  <i class="bi bi-check-circle me-1"></i>Adopted
                </div>
                <div v-else class="status-badge available">
                  <i class="bi bi-heart me-1"></i>Available
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="p-4">
                <div class="d-grid gap-3">
                  <!-- Adopt Button -->
                  <button 
                    v-if="isAuthenticated && !pet.is_adopted"
                    class="btn btn-success btn-lg py-3 fw-bold"
                    @click="startAdoption"
                    :disabled="adopting"
                  >
                    <span v-if="adopting" class="spinner-border spinner-border-sm me-2"></span>
                    <i v-else class="bi bi-heart me-2"></i>
                    {{ adopting ? 'Adopting...' : `Adopt ${pet.name}` }}
                  </button>

                  <!-- Login to Adopt -->
                  <button 
                    v-else-if="!isAuthenticated && !pet.is_adopted"
                    class="btn btn-success btn-lg py-3 fw-bold"
                    @click="$router.push('/login')"
                  >
                    <i class="bi bi-person me-2"></i>Login to Adopt
                  </button>

                  <!-- Already Adopted -->
                  <div v-else class="text-center py-3">
                    <i class="bi bi-check-circle-fill text-success display-6 mb-2"></i>
                    <p class="text-muted mb-0">This pet has found a loving home!</p>
                  </div>

                  <!-- Favorite Button -->
                  <button 
                    v-if="isAuthenticated"
                    class="btn py-2"
                    :class="isFavorite ? 'btn-danger' : 'btn-outline-primary'"
                    @click="toggleFavorite"
                    :disabled="favoriteLoading"
                  >
                    <i class="bi" :class="isFavorite ? 'bi-heart-fill' : 'bi-heart'"></i>
                    {{ favoriteLoading ? '...' : (isFavorite ? 'Remove from Favorites' : 'Add to Favorites') }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column - Pet Details -->
        <div class="col-xl-7 col-lg-6">
          <div class="card shadow-sm border-0 h-100">
            <div class="card-body p-4">
              <!-- Pet Header -->
              <div class="d-flex justify-content-between align-items-start mb-4 pb-3 border-bottom">
                <div>
                  <h1 class="pet-name mb-2">{{ pet.name }}</h1>
                  <div class="d-flex align-items-center gap-3">
                    <span class="pet-type-badge" :class="pet.type === 'dog' ? 'dog-badge' : 'cat-badge'">
                      <i :class="pet.type === 'dog' ? 'bi bi-bone' : 'bi bi-bootstrap'"></i>
                      {{ pet.type === 'dog' ? 'Dog' : 'Cat' }}
                    </span>
                    <span class="text-muted">
                      <i class="bi bi-geo-alt me-1"></i>{{ pet.location || 'Local Shelter' }}
                    </span>
                  </div>
                </div>
                <div v-if="hasCompletedQuiz && pet.compatibility_score" class="text-end">
                  <div class="compatibility-score">
                    <div class="score-value">{{ pet.compatibility_score }}%</div>
                    <div class="score-label">Match</div>
                  </div>
                </div>
              </div>

              <!-- Basic Information Grid -->
              <div class="row g-3 mb-4">
                <div class="col-sm-6">
                  <div class="info-item">
                    <i class="bi bi-calendar3 text-primary"></i>
                    <div>
                      <label>Age: </label>
                      <span class="value-spacing">{{ pet.age }}</span>
                    </div>
                  </div>
                </div>
                <div class="col-sm-6">
                  <div class="info-item">
                    <i class="bi bi-tag text-primary"></i>
                    <div>
                      <label>Breed: </label>
                      <span class="value-spacing">{{ pet.breed }}</span>
                    </div>
                  </div>
                </div>
                <div class="col-sm-6">
                  <div class="info-item">
                    <i class="bi bi-rulers text-primary"></i>
                    <div>
                      <label>Size: </label>
                      <span class="value-spacing">{{ pet.size }}</span>
                    </div>
                  </div>
                </div>
                <div class="col-sm-6">
                  <div class="info-item">
                    <i class="bi bi-gender-ambiguous text-primary"></i>
                    <div>
                      <label>Gender: </label>
                      <span class="value-spacing">{{ pet.gender }}</span>
                    </div>
                  </div>
                </div>
                <div class="col-12">
                  <div class="info-item">
                    <i class="bi bi-lightning-charge text-primary"></i>
                    <div>
                      <label>Activity Level: </label>
                      <span style="margin-left: 8px;" class="badge" :class="getActivityClass(pet.activity_level)">
                        {{ formatActivityLevel(pet.activity_level) }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Personality -->
              <div class="mb-4">
                <h5 class="section-title mb-3">
                  <i class="bi bi-chat-heart text-primary me-2"></i>Personality
                </h5>
                <div class="personality-card">
                  <p class="mb-0">"{{ pet.personality }}"</p>
                </div>
              </div>
              <!-- background story -->
              <div class="mb-4" v-if="pet.background">
                <h5 class="section-title mb-3">
                  <i class="bi bi-heart text-danger me-2"></i>Background story
                </h5>
                <div class="background-story-card">
                  <p class="mb-0">"{{ pet.background }}"</p>
                </div>
              </div>

              <!-- Compatibility Progress -->
              <div v-if="hasCompletedQuiz && pet.compatibility_score" class="mb-4">
                <h5 class="section-title mb-3">
                  <i class="bi bi-graph-up text-primary me-2"></i>Compatibility
                </h5>
                <div class="compatibility-progress">
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="fw-semibold">Your match score with {{ pet.name }}</span>
                    <span class="compatibility-value">{{ pet.compatibility_score }}%</span>
                  </div>
                  <div class="progress" style="height: 8px;">
                    <div 
                      class="progress-bar" 
                      :class="getCompatibilityClass(pet.compatibility_score)"
                      :style="{ width: pet.compatibility_score + '%' }"
                    ></div>
                  </div>
                  <div class="compatibility-description mt-2">
                    <small class="text-muted">
                      {{ getCompatibilityDescription(pet.compatibility_score) }}
                    </small>
                  </div>
                </div>
              </div>

              <!-- Health & Care -->
              <div class="row g-3">
                <div class="col-lg-6">
                  <div class="info-card">
                    <h6 class="info-card-title">
                      <i class="bi bi-heart-pulse text-danger me-2"></i>Health Info
                    </h6>
                    <div class="info-list">
                      <div class="info-list-item">
                        <span>Vaccinated</span>
                        <span class="status" :class="getVaccinationStatusClass()">
                          {{ pet.vaccination_status || 'Unknown' }}
                        </span>
                      </div>
                      <div class="info-list-item">
                        <span>Health Status</span>
                        <span class="status yes">{{ pet.health_info || 'Excellent' }}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col-lg-6">
                  <div class="info-card">
                    <h6 class="info-card-title">
                      <i class="bi bi-house-heart text-success me-2"></i>Home Compatibility
                    </h6>
                    <div class="info-list">
                      <div class="info-list-item">
                        <span>Good with Children</span>
                        <span class="status" :class="pet.good_with_children ? 'yes' : 'no'">
                          {{ pet.good_with_children ? 'Yes' : 'Unknown' }}
                        </span>
                      </div>
                      <div class="info-list-item">
                        <span>Good with Other Pets</span>
                        <span class="status" :class="pet.good_with_other_pets ? 'yes' : 'no'">
                          {{ pet.good_with_other_pets ? 'Yes' : 'Unknown' }}
                        </span>
                      </div>
                      <div class="info-list-item">
                        <span>Fur Color</span>
                        <span class="text-muted">{{ pet.furColor || 'Various' }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Care Requirements -->
              <div class="mt-4">
                <h5 class="section-title mb-3">
                  <i class="bi bi-info-circle text-primary me-2"></i>Care Requirements
                </h5>
                <div class="care-requirements">
                  <div class="care-item" v-if="pet.activity_level === 'high'">
                    <i class="bi bi-lightning-charge text-warning"></i>
                    <span>High energy - needs daily exercise and playtime</span>
                  </div>
                  <div class="care-item" v-else-if="pet.activity_level === 'low'">
                    <i class="bi bi-moon text-secondary"></i>
                    <span>Low energy - perfect for relaxed home environment</span>
                  </div>
                  <div class="care-item" v-else>
                    <i class="bi bi-sun text-info"></i>
                    <span>Moderate energy - enjoys regular walks and play</span>
                  </div>
                  <div class="care-item" v-if="pet.good_with_children">
                    <i class="bi bi-emoji-smile text-warning"></i>
                    <span>Great with children and families</span>
                  </div>
                  <div class="care-item" v-if="pet.good_with_other_pets">
                    <i class="bi bi-people text-success"></i>
                    <span>Gets along well with other pets</span>
                  </div>
                  <div class="care-item">
                    <i class="bi bi-house-door text-success"></i>
                    <span>Ideal for {{ getLivingSituation(pet.size) }}</span>
                  </div>
                </div>
              </div>
                 <!--to add extra things here, such as HDB requirements -->
              <div class="mt-4">
                <h5 class="section-title mb-3">
                  <i class="bi bi-clipboard-check text-primary me-2"></i>Other Requirements
                </h5>
                <div class="care-item2">
                      <span>Adoption Fee</span>
                      <span class="status yes">${{ pet.adoption_fee || 'Free' }}</span>
                </div>
                <div class="care-requirements">
                  <div class="care-item2" v-if="pet.HDB_approved">
                    <i class="bi bi-building text-success"></i>
                    <span>{{ getHDBStatus() }}</span>
                
                  </div>
                  <div class="care-item2" v-else>
                    <i class="bi bi-building text-danger"></i>
                    <span>{{ getHDBStatus() }}</span>
                    
                  </div>
                  
                  <div class="care-item2" v-if="pet.HDB_approved && pet.type === 'cat'">
                    <ul class="hdb-checklist">
                      <li><i class="bi bi-exclamation-circle-fill text-warning me-2"></i>HDB permits up to 2 cats per household</li>
                      <li><i class="bi bi-exclamation-circle-fill text-warning me-2"></i>Windows and gates must be mashed up</li>
                    </ul>
                  </div>
                  <div class="care-item2" v-if="pet.type === 'dog'">
                      <span> HDB regulations permit only one dog per flat</span>
                  </div>

                </div>
                
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
  name: 'PetProfile',
  data() {
    return {
      pet: null,
      loading: true,
      error: null,
      isAuthenticated: false,
      hasCompletedQuiz: false,
      isFavorite: false,
      favoriteLoading: false,
      adopting: false,
      imageCache: new Map(),
      allDogBreeds: [],
      allCatBreeds: [],
      HDB_approved:null
    }
  },
  async mounted() {
    await this.initializePage();
  },
  watch: {
    '$route.params.petId': {
      handler() {
        this.initializePage();
      },
      immediate: false
    }
  },
  methods: {
    async initializePage() {
      this.checkAuth();
      await this.loadAllBreeds();
      await this.loadPetDetails();
      if (this.isAuthenticated) {
        await Promise.all([
          this.checkQuizCompletion(),
          this.checkFavoriteStatus()
        ]);
      }
    },

    checkAuth() {
      const token = localStorage.getItem('authToken');
      this.isAuthenticated = !!token;
    },

    async loadPetDetails() {
      this.loading = true;
      this.error = null;
      
      try {
        // get petID from the URL
        const petId = this.$route.params.petId;
        console.log('Loading pet details for ID:', petId);
        // If user has logged in, they would be sent to the login page
        const token = localStorage.getItem('authToken');
        const headers = {
          'Content-Type': 'application/json'
        };
        
        if (token) {
          headers['Authorization'] = `Bearer ${token}`;
        }

        // Try to get pet with compatibility scores if authenticated and quiz completed + fetch pet data from API
        let url = `${API_BASE_URL}/pets/${petId}`;
        let response = await fetch(url, { headers });
        
        if (!response.ok && this.isAuthenticated) {
          // If regular endpoint fails and user is authenticated, try with scores
          const allPetsResponse = await fetch(`${API_BASE_URL}/pets/with-scores`, { headers });
          if (allPetsResponse.ok) {
            const allPets = await allPetsResponse.json();
            const specificPet = allPets.find(p => p.id === parseInt(petId));
            if (specificPet) {
              this.pet = await this.processPetWithImages(specificPet);
              this.loading = false;
              return;
            }
          }
        }

        if (response.ok) {
          const petData = await response.json();
          this.pet = await this.processPetWithImages(petData);
          console.log('Pet data loaded with images:', this.pet);
        } else if (response.status === 404) {
          this.error = 'Pet not found.';
        } else {
          const errorData = await response.json().catch(() => ({}));
          this.error = errorData.error || 'Error loading pet details.';
        }
      } catch (error) {
        console.error('Error loading pet:', error);
        this.error = 'Network error. Please try again.';
      } finally {
        this.loading = false;
      }
    },

    async processPetWithImages(pet) {
      // Use the same image processing logic as PetListingPage
      if (pet.image && pet.image.trim() !== '') {
        return {
          ...pet,
          displayImage: pet.image,
          imageLoaded: false,
          placeholderImage: false
        };
      } else {
        const processedPet = {
          ...pet,
          displayImage: this.getColoredPlaceholder(pet),
          imageLoaded: false,
          placeholderImage: true
        };
        
        // Try to fetch API image for this pet
        await this.fetchApiImageForPet(processedPet);
        return processedPet;
      }
    },

    async fetchApiImageForPet(pet) {
      if (!pet.placeholderImage) return;
      
      try {
        const apiImage = await this.fetchPetImage(pet);
        if (apiImage) {
          pet.displayImage = apiImage;
          pet.image = apiImage;
          pet.placeholderImage = false;
        }
      } catch (error) {
        console.error(`Failed to fetch API image for ${pet.name}:`, error);
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
        
        if (!response.ok) throw new Error(`API error: ${response.status}`);
        
        const data = await response.json();
        if (data && data.length > 0 && data[0].url) {
          const imageUrl = data[0].url;
          this.imageCache.set(cacheKey, imageUrl);
          return imageUrl;
        }
        return "";
      } catch (error) {
        console.error(`Error fetching image for ${pet.name}:`, error);
        return "";
      }
    },

    findBreedId(breedName, type) {
      const breeds = type === "dog" ? this.allDogBreeds : this.allCatBreeds;
      if (!breeds.length) return null;
      const breed = breeds.find(b => 
        b.name.toLowerCase().includes(breedName.toLowerCase()) ||
        breedName.toLowerCase().includes(b.name.toLowerCase())
      );
      return breed ? breed.id : null;
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
        
        if (dogResponse.ok && catResponse.ok) {
          this.allDogBreeds = await dogResponse.json();
          this.allCatBreeds = await catResponse.json();
        }
      } catch (error) {
        console.error("Error fetching breed lists:", error);
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
      
      return `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300' viewBox='0 0 400 300'%3E%3Crect fill='${color}' width='400' height='300'/%3E%3Ctext fill='%23666' font-size='48' font-family='system-ui' x='200' y='150' text-anchor='middle' dominant-baseline='middle'%3E${emoji}%3C/text%3E%3Ctext fill='%23333' font-size='24' font-family='system-ui' x='200' y='200' text-anchor='middle'%3E${pet.name}%3C/text%3E%3C/svg%3E`;
    },

    onImageLoad(pet) {
      pet.imageLoaded = true;
    },

    onImageError(pet) {
      if (pet.displayImage !== this.getColoredPlaceholder(pet)) {
        pet.displayImage = this.getColoredPlaceholder(pet);
        pet.placeholderImage = false;
      }
      pet.imageLoaded = true;
    },

    async checkQuizCompletion() {
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/user/quiz`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        this.hasCompletedQuiz = response.ok;
      } catch (error) {
        console.log('No quiz results found');
        this.hasCompletedQuiz = false;
      }
    },

    async checkFavoriteStatus() {
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/user/favorites`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          const favoriteIds = await response.json();
          this.isFavorite = favoriteIds.includes(parseInt(this.$route.params.petId));
        }
      } catch (error) {
        console.error('Error checking favorite status:', error);
      }
    },

    async toggleFavorite() {
      if (!this.isAuthenticated) {
        this.$router.push('/login');
        return;
      }

      this.favoriteLoading = true;
      try {
        const token = localStorage.getItem('authToken');
        const petId = this.$route.params.petId;

        if (this.isFavorite) {
          // Remove from favorites
          await fetch(`${API_BASE_URL}/user/favorites/${petId}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          this.isFavorite = false;
          this.showToast('Removed from favorites', 'success');
        } else {
          // Add to favorites
          await fetch(`${API_BASE_URL}/user/favorites`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ pet_id: parseInt(petId) })
          });
          this.isFavorite = true;
          this.showToast('Added to favorites!', 'success');
        }
      } catch (error) {
        console.error('Error toggling favorite:', error);
        this.showToast('Failed to update favorites. Please try again.', 'error');
      } finally {
        this.favoriteLoading = false;
      }
    },

    async startAdoption() {
      if (!this.isAuthenticated) {
        this.$router.push('/login');
        return;
      }

      if (this.pet.is_adopted) {
        this.showToast('This pet has already been adopted!', 'error');
        return;
      }

      // Use the same approach as PetListingPage - navigate to adoption form
      console.log('Starting adoption for pet:', this.pet.id);
      this.$router.push(`/adopt/${this.pet.id}`);
    },

    showToast(message, type = 'info') {
      // Simple toast notification
      const toast = document.createElement('div');
      toast.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show position-fixed`;
      toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
      toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      `;
      document.body.appendChild(toast);
      
      // Auto remove after 5 seconds
      setTimeout(() => {
        if (toast.parentNode) {
          toast.parentNode.removeChild(toast);
        }
      }, 5000);
    },

    getActivityClass(activity) {
      const activityMap = {
        'low': 'bg-secondary text-white',
        'medium': 'bg-warning text-dark', 
        'high': 'bg-success text-white'
      };
      return activityMap[activity] || 'bg-info text-white';
    },

    formatActivityLevel(activity) {
      const activityMap = {
        'low': 'Low',
        'medium': 'Medium',
        'high': 'High'
      };
      return activityMap[activity] || 'Medium';
    },

    getVaccinationStatusClass() {
      const status = this.pet.vaccination_status?.toLowerCase();
      if (status?.includes('up to date') || status?.includes('vaccinated')) {
        return 'yes';
      } else if (status?.includes('not') || status?.includes('unknown')) {
        return 'no';
      }
      return 'yes';
    },

    getCompatibilityClass(score) {
      if (score >= 80) return 'bg-success';
      if (score >= 60) return 'bg-warning';
      return 'bg-danger';
    },

    getCompatibilityDescription(score) {
      if (score >= 80) return 'Excellent match! This pet fits perfectly with your lifestyle.';
      if (score >= 60) return 'Good match! This pet would be a great companion.';
      if (score >= 40) return 'Fair match. Consider if you can accommodate their needs.';
      return 'This pet may not be the best fit for your current situation.';
    },

    getLivingSituation(size) {
      const sizeMap = {
        'Small': 'apartments and small homes',
        'Medium': 'most homes with some space',
        'Large': 'homes with yards or large spaces'
      };
      return sizeMap[size] || 'various living situations';
    },
    getHDBStatus() {
      return this.pet.HDB_approved ? "HDB approved" : "Not HDB approved";
}
  }
    
}
</script>

<style scoped>
.pet-profile-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 1rem 0;
}

/* Image Container */
.pet-image-container {
  border-radius: 12px 12px 0 0;
  overflow: hidden;
  position: relative;
  background: #f8f9fa;
  min-height: 350px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pet-image {
  height: 350px;
  object-fit: cover;
  transition: all 0.3s ease;
}

.pet-image:hover {
  transform: scale(1.02);
}

/* Image Loading Overlay */
.image-loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 2;
}

/* API Badge */
.api-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  background-color: rgba(255, 255, 255, 0.95);
  color: #666;
  font-size: 0.7rem;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 6px;
  border: 1px solid #e9ecef;
  z-index: 3;
}

/* Badges */
.compatibility-badge {
  position: absolute;
  top: 16px;
  left: 16px;
  background: rgba(255, 255, 255, 0.95);
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
  border: 1px solid #e9ecef;
  color: #333;
  z-index: 3;
}

.status-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  z-index: 3;
}

.status-badge.available {
  background: linear-gradient(135deg, #4ECDC4, #6EE7E7);
  color: white;
}

.status-badge.adopted {
  background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
  color: white;
}

/* Compatibility Description */
.compatibility-description {
  font-style: italic;
}

.pet-type-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.8rem;
}

.dog-badge {
  background: #ffeef1;
  color: #e91e63;
  border: 1px solid #e91e63;
}

.cat-badge {
  background: #e3f2fd;
  color: #2196f3;
  border: 1px solid #2196f3;
}

.compatibility-score {
  text-align: center;
}

.score-value {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1;
}

.score-label {
  font-size: 0.8rem;
  color: #6c757d;
  font-weight: 600;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #4ECDC4;
}

.section-title {
  color: #2c5530;
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.personality-card {
  background: linear-gradient(135deg, #ffeef1, #fff5f7);
  padding: 1.5rem;
  border-radius: 12px;
  border-left: 4px solid #e91e63;
  font-style: italic;
  color: #666;
}
.background-story-card {
  background: linear-gradient(135deg, #e6f0ff, #cce0ff);
  padding: 1.5rem;
  border-radius: 12px;
  border-left: 4px solid #0071b6;
  font-style: italic;
  color: #666;
}

.compatibility-progress {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.compatibility-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #4ECDC4;
}

.info-card {
  background: white;
  padding: 1.25rem;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  height: 100%;
}

.info-list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f8f9fa;
}

.status {
  font-weight: 600;
  font-size: 0.85rem;
  padding: 4px 8px;
  border-radius: 6px;
}

.status.yes {
  background: #d4edda;
  color: #155724;
}

.status.no {
  background: #f8d7da;
  color: #721c24;
}

.care-requirements {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.care-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #4ECDC4;
}
.care-item2 {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #d94e98;
}

.btn-success {
  background: linear-gradient(135deg, #4ECDC4, #6EE7E7);
  border: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-success:hover:not(:disabled) {
  background: linear-gradient(135deg, #26A69A, #4ECDC4);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(78, 205, 196, 0.4);
}

.progress {
  background: #e9ecef;
  border-radius: 10px;
  overflow: hidden;
}

.progress-bar {
  border-radius: 10px;
  transition: width 0.6s ease;
}

.value-spacing {
  margin-left: 8px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .pet-name {
    font-size: 1.75rem;
  }
  
  .pet-image {
    height: 280px;
  }
  
  .compatibility-score {
    margin-top: 1rem;
  }
}

@media (max-width: 576px) {
  .container {
    padding: 0 10px;
  }
  
  .pet-image {
    height: 250px;
  }
  
  .btn-lg {
    padding: 0.75rem 1rem;
    font-size: 1rem;
  }
  .hdb-checklist {
  list-style: none!important; /* remove default bullets */
  padding-left: 0;
  margin: 0;
}

.hdb-checklist li {
  display: flex;
  align-items: center;
  gap: 0.5rem; /* space between icon and text */
  background: #f8f9fa;
  padding: 8px 12px;
  border-left: 4px solid #ffc107; /* yellow accent like warning */
  border-radius: 6px;
  margin-bottom: 6px;
  font-weight: 500;
  font-size: 0.95rem;
  
}


}
</style>
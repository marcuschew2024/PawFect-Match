<template>
  <div class="container my-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="mb-0">Find Your Pawfect Match</h1>
      <div v-if="isAuthenticated" class="d-flex gap-2">
        <button class="btn btn-warning" @click="$router.push('/quiz')">
          <i class="bi bi-clipboard-check me-2"></i>
          {{ hasCompletedQuiz ? 'Update Quiz' : 'Take Lifestyle Quiz' }}
        </button>
        <router-link v-if="hasCompletedQuiz" to="/favorites" class="btn btn-outline-primary">
          <i class="bi bi-heart me-2"></i>View Favorites
        </router-link>
      </div>
    </div>

    <!-- Quiz Prompt for Authenticated Users -->
    <div v-if="isAuthenticated && !hasCompletedQuiz && !loading" class="alert alert-info">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <i class="bi bi-info-circle me-2"></i>
          Complete our lifestyle quiz to see compatibility scores with each pet!
        </div>
        <button class="btn btn-primary btn-sm" @click="$router.push('/quiz')">
          Take Quiz Now
        </button>
      </div>
    </div>

    <!-- Enhanced Filter Section -->
    <div class="filter-section">
      <div class="row g-3 align-items-end">
        <!-- Search Input -->
        <div class="col-lg-3 col-md-6">
          <label for="searchInput" class="form-label">SEARCH PETS</label>
          <input type="text" class="form-control" id="searchInput" v-model="searchTerm"
            placeholder="Name, breed, or personality..." autocomplete="off">
        </div>

        <!-- Type Filter -->
        <div class="col-lg-2 col-md-4 col-sm-6">
          <label for="typeFilter" class="form-label">TYPE</label>
          <select class="form-select" id="typeFilter" v-model="filters.type">
            <option value="">All Types</option>
            <option value="dog">Dogs</option>
            <option value="cat">Cats</option>
          </select>
        </div>

        <!-- Size Filter -->
        <div class="col-lg-2 col-md-4 col-sm-6">
          <label for="sizeFilter" class="form-label">SIZE</label>
          <select class="form-select" id="sizeFilter" v-model="filters.size">
            <option value="">All Sizes</option>
            <option value="Small">Small</option>
            <option value="Medium">Medium</option>
            <option value="Large">Large</option>
          </select>
        </div>

        <!-- Compatibility Filter -->
        <div v-if="hasCompletedQuiz" class="col-lg-2 col-md-4 col-sm-6">
          <label for="compatibilityFilter" class="form-label">MIN SCORE</label>
          <select class="form-select" id="compatibilityFilter" v-model="filters.minScore">
            <option value="0">Any Score</option>
            <option value="70">70%+</option>
            <option value="80">80%+</option>
            <option value="90">90%+</option>
          </select>
        </div>

        <!-- Action Buttons -->
        <div class="col-lg-3 col-md-6">
          <div class="d-flex gap-2">
            <button class="btn btn-primary flex-fill" @click="applyFilters">
              <i class="bi bi-funnel me-2"></i>APPLY FILTERS
            </button>
            <button class="btn btn-outline-secondary" @click="resetFilters">
              <i class="bi bi-arrow-clockwise"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Pets Grid -->
    <div class="row mt-4">
      <div v-if="loading" class="col-12">
        <div class="loading-text">
          <i class="bi bi-arrow-repeat spinner me-2"></i>
          Loading pets for You...
        </div>
      </div>

      <div v-else-if="error" class="col-12">
        <div class="error-message text-center">
          <i class="bi bi-exclamation-triangle display-4 text-warning mb-3"></i>
          <h4>Unable to Load Pets</h4>
          <p class="mt-3">{{ error }}</p>
          <div class="mt-4">
            <button class="btn btn-primary me-2" @click="fetchPets">
              <i class="bi bi-arrow-clockwise me-2"></i>Try Again
            </button>
          </div>
        </div>
      </div>

      <div v-else-if="filteredPets.length === 0" class="col-12">
        <div class="no-results">No pets found matching your criteria.</div>
      </div>

      <div v-else class="col-md-6 col-lg-4 mb-4" v-for="pet in filteredPets" :key="pet.id">
        <div class="card h-100 pet-card">
          <div class="position-relative">
            <img :src="pet.displayImage" :alt="pet.name" class="card-img-top"
              :class="{ 'image-loaded': pet.imageLoaded }" @load="onImageLoad(pet)" @error="onImageError(pet)"
              loading="lazy">

            <!-- Compatibility Score Badge -->
            <div v-if="hasCompletedQuiz && pet.compatibility_score" class="compatibility-badge">
              {{ pet.compatibility_score }}% Match
            </div>

            <!-- Favorite Button -->
            <button v-if="isAuthenticated" class="favorite-btn" @click="toggleFavorite(pet)"
              :class="{ 'favorited': pet.is_favorite }">
              <i class="bi" :class="pet.is_favorite ? 'bi-heart-fill' : 'bi-heart'"></i>
            </button>

            <div v-if="pet.placeholderImage && pet.imageLoaded" class="api-badge">
              Placeholder Image
            </div>
            <div v-if="!pet.imageLoaded" class="image-loading">
              <i class="bi bi-arrow-repeat spinner"></i>
            </div>
          </div>

          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ pet.name }}</h5>

            <!-- Compatibility Meter -->
            <div v-if="hasCompletedQuiz && pet.compatibility_score" class="compatibility-meter mb-3">
              <div class="d-flex justify-content-between align-items-center mb-1">
                <small class="text-muted">Compatibility</small>
                <small class="fw-bold text-muted">
                  {{ pet.compatibility_score }}%
                </small>
              </div>
              <div class="progress" style="height: 6px;">
                <div class="progress-bar bg-primary" :style="{ width: pet.compatibility_score + '%' }"></div>
              </div>
            </div>

            <p class="card-text mb-2 flex-grow-1">
              <strong>Age:</strong> {{ pet.age }}<br>
              <strong>Breed:</strong> {{ pet.breed }}<br>
              <strong>Size:</strong> {{ pet.size }}<br>
              <strong>Gender:</strong> {{ pet.gender }}<br>
              <strong>Activity:</strong>
              <span class="badge" :class="getActivityClass(pet.activity_level)">
                {{ pet.activity_level }}
              </span>
            </p>
            <p class="card-text personality">"{{ pet.personality }}"</p>
          </div>

          <!-- Replace the current adoption button section in your PetListingPage.vue -->
          <div class="card-footer bg-transparent">
            <div class="d-grid gap-2">
              <!-- View More Button -->
              <button class="btn view-more-btn" @click="$router.push(`/pet/${pet.id}`)">
                <i class="bi bi-eye me-1"></i>View More
              </button>

              <!-- Adoption Button - FIXED VERSION -->
              <button v-if="isAuthenticated && !pet.is_adopted" class="btn btn-success" @click="startAdoption(pet)">
                <i class="bi bi-heart me-1"></i>Adopt {{ pet.name }}
              </button>

              <button v-else-if="!isAuthenticated" class="btn btn-outline-success" @click="$router.push('/login')">
                <i class="bi bi-person me-1"></i>Login to Adopt
              </button>

              <button v-else-if="pet.is_adopted" class="btn btn-secondary" disabled>
                <i class="bi bi-check-circle me-1"></i>Already Adopted
              </button>

              <!-- Favorite Buttons -->
              <button v-if="isAuthenticated && !pet.is_favorite" class="btn btn-outline-primary btn-sm"
                @click="toggleFavorite(pet)">
                <i class="bi bi-heart me-1"></i>Add to Favorites
              </button>
              <button v-else-if="isAuthenticated && pet.is_favorite" class="btn btn-outline-danger btn-sm"
                @click="toggleFavorite(pet)">
                <i class="bi bi-heart-fill me-1"></i>Remove Favorite
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pet Detail Modal -->
    <PetDetailModal ref="petDetailModal" :pet="selectedPet" :isAuthenticated="isAuthenticated"
      :hasCompletedQuiz="hasCompletedQuiz" @start-adoption="startAdoption" />
  </div>
</template>

<script>
const API_BASE_URL = 'http://localhost:3000/api';

// Import the modal component
import PetDetailModal from '@/components/PetDetailModal.vue';

export default {
  name: 'PetListingPage',
  components: {
    PetDetailModal
  },
  data() {
    return {
      pets: [],
      filteredPets: [],
      searchTerm: '',
      filters: {
        type: '',
        size: '',
        minScore: '0'
      },
      loading: true,
      error: null,
      imageCache: new Map(),
      allDogBreeds: [],
      allCatBreeds: [],
      isAuthenticated: false,
      hasCompletedQuiz: false,
      userProfile: null,
      selectedPet: null  // Track selected pet for modal
    }
  },
  async mounted() {
    this.checkAuth();
    await this.initializePage();
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem('authToken');
      this.isAuthenticated = !!token;
    },

    async initializePage() {
      //Load all breed data FIRST (and WAIT for it)
      await this.loadAllBreeds();

      //Check if user has completed quiz
      if (this.isAuthenticated) {
        await this.checkQuizCompletion();
      }

      //Now fetch pets (breeds will be available for matching)
      await this.fetchPets();
    },

    async checkQuizCompletion() {
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/user/quiz`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          this.userProfile = await response.json();
          this.hasCompletedQuiz = true;
        }
      } catch (error) {
        console.log('No quiz results found');
      }
    },

    async fetchPets() {
      this.loading = true;
      this.error = null;

      try {
        const token = localStorage.getItem('authToken');
        let url = `${API_BASE_URL}/pets`;

        // Use the enhanced endpoint if user has completed quiz
        if (this.isAuthenticated && this.hasCompletedQuiz) {
          url = `${API_BASE_URL}/pets/with-scores`;
        }

        const headers = {
          'Content-Type': 'application/json'
        };

        if (token) {
          headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(url, { headers });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        let data = await response.json();

        // Process pets data
        this.pets = await this.processPetsWithImages(data);
        this.filteredPets = [...this.pets];

      } catch (error) {
        console.error('Error fetching pets:', error);
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },

    async toggleFavorite(pet) {
      if (!this.isAuthenticated) {
        this.$router.push('/login');
        return;
      }

      try {
        const token = localStorage.getItem('authToken');

        if (pet.is_favorite) {
          // Remove from favorites
          await fetch(`${API_BASE_URL}/user/favorites/${pet.id}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          pet.is_favorite = false;
        } else {
          // Add to favorites
          await fetch(`${API_BASE_URL}/user/favorites`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ pet_id: pet.id })
          });
          pet.is_favorite = true;
        }

        // Update the array to trigger reactivity
        this.pets = [...this.pets];
        this.filteredPets = [...this.filteredPets];

      } catch (error) {
        console.error('Error toggling favorite:', error);
      }
    },

    getActivityClass(activity) {
      switch (activity) {
        case 'low': return 'bg-secondary';
        case 'medium': return 'bg-warning';
        case 'high': return 'bg-success';
        default: return 'bg-info';
      }
    },

    applyFilters() {
      const filtered = this.pets.filter(pet => {
        const matchesSearch = !this.searchTerm ||
          pet.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          pet.breed.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          pet.personality.toLowerCase().includes(this.searchTerm.toLowerCase());

        const matchesType = !this.filters.type || pet.type === this.filters.type;
        const matchesSize = !this.filters.size || pet.size === this.filters.size;
        const matchesScore = !this.hasCompletedQuiz ||
          pet.compatibility_score >= parseInt(this.filters.minScore);

        return matchesSearch && matchesType && matchesSize && matchesScore;
      });

      this.filteredPets = filtered;
    },

    resetFilters() {
      this.searchTerm = '';
      this.filters = {
        type: '',
        size: '',
        minScore: '0'
      };
      this.filteredPets = [...this.pets];
    },

    async processPetsWithImages(pets) {
      const processedPets = pets.map(pet => {
        if (pet.image && pet.image.trim() !== '') {
          return {
            ...pet,
            displayImage: pet.image,
            imageLoaded: false,
            placeholderImage: false
          };
        } else {
          return {
            ...pet,
            displayImage: this.getColoredPlaceholder(pet),
            imageLoaded: false,
            placeholderImage: true
          };
        }
      });

      this.fetchApiImagesForPets(processedPets);
      return processedPets;
    },

    async fetchApiImagesForPets(pets) {
      const petsNeedingImages = pets.filter(pet => pet.placeholderImage);
      const batchSize = 3;

      for (let i = 0; i < petsNeedingImages.length; i += batchSize) {
        const batch = petsNeedingImages.slice(i, i + batchSize);
        const promises = batch.map(async (pet) => {
          try {
            const apiImage = await this.fetchPetImage(pet);
            if (apiImage) {
              pet.displayImage = apiImage;
              pet.image = apiImage;
              this.pets = [...this.pets];
              this.filteredPets = [...this.filteredPets];
            }
          } catch (error) {
            console.error(`Failed to fetch API image for ${pet.name}:`, error);
          }
        });

        await Promise.allSettled(promises);
        if (i + batchSize < petsNeedingImages.length) {
          await new Promise(resolve => setTimeout(resolve, 500));
        }
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

    //new API code
    findBreedId(breedName, type) {
      const breeds = type === "dog" ? this.allDogBreeds : this.allCatBreeds;
      if (!breeds.length) {
        console.log(`No breeds loaded for ${type}`);
        return null;
      }

      const normalizedBreedName = breedName.toLowerCase().trim();
      console.log(`Searching for breed: "${breedName}" (${type})`);

      // 1. EXACT match
      let breed = breeds.find(b =>
        b.name.toLowerCase().trim() === normalizedBreedName
      );

      return null;
    },

    // old API code 
    // findBreedId(breedName, type) {
    //   const breeds = type === "dog" ? this.allDogBreeds : this.allCatBreeds;
    //   if (!breeds.length) return null;
    //   const breed = breeds.find(b => 
    //     b.name.toLowerCase().includes(breedName.toLowerCase()) ||
    //     breedName.toLowerCase().includes(b.name.toLowerCase())
    //   );
    //   return breed ? breed.id : null;
    // },
    //
    async loadAllBreeds() {
      try {
        const token = localStorage.getItem('authToken');
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const [dogResponse, catResponse] = await Promise.all([
          fetch(`${API_BASE_URL}/external/dog-breeds`, { headers }),
          fetch(`${API_BASE_URL}/external/cat-breeds`, { headers })
        ]);

        // CHECK INDIVIDUAL RESPONSES
        if (dogResponse.ok) {
          this.allDogBreeds = await dogResponse.json();
          console.log(`✓ Loaded ${this.allDogBreeds.length} dog breeds`);
        } else {
          console.error('❌ Dog breeds failed:', dogResponse.status);
        }

        if (catResponse.ok) {
          this.allCatBreeds = await catResponse.json();
          console.log(`✓ Loaded ${this.allCatBreeds.length} cat breeds`);
        } else {
          console.error('❌ Cat breeds failed:', catResponse.status);
        }

      } catch (error) {
        console.error("❌ Error fetching breed lists:", error);
      }
    },

    // async loadAllBreeds() {
    //   try {
    //     const token = localStorage.getItem('authToken');
    //     const headers = { 'Content-Type': 'application/json' };
    //     if (token) headers['Authorization'] = `Bearer ${token}`;

    //     const [dogResponse, catResponse] = await Promise.all([
    //       fetch(`${API_BASE_URL}/external/dog-breeds`, { headers }),
    //       fetch(`${API_BASE_URL}/external/cat-breeds`, { headers })
    //     ]);

    //     if (dogResponse.ok && catResponse.ok) {
    //       this.allDogBreeds = await dogResponse.json();
    //       this.allCatBreeds = await catResponse.json();
    //     }
    //   } catch (error) {
    //     console.error("Error fetching breed lists:", error);
    //   }
    // },

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

    // NEW METHODS FOR ADOPTION FLOW
    showPetDetails(pet) {
      this.selectedPet = pet;
      this.$refs.petDetailModal.show();
    },

    startAdoption(pet) {
      // Directly navigate to adoption form for this pet
      this.$router.push(`/adopt/${pet.id}`);
    }
  }
}
</script>

<style scoped>
.compatibility-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  background: rgba(255, 255, 255, 0.95);
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  z-index: 3;
  border: 1px solid var(--border-light);
  color: var(--text-dark);
}

.favorite-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(255, 255, 255, 0.95);
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3;
  transition: all 0.3s ease;
}

.favorite-btn:hover {
  background: white;
  transform: scale(1.1);
}

.favorite-btn.favorited {
  color: #dc3545;
}

.compatibility-meter {
  background: var(--background-light);
  padding: 0.75rem;
  border-radius: 8px;
  border-left: 3px solid var(--primary-pink);
}

.api-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background-color: rgba(255, 255, 255, 0.95);
  color: var(--text-light);
  font-size: 0.7rem;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 6px;
  border: 1px solid var(--border-light);
  z-index: 3;
}

.image-loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #666;
  font-size: 1.5rem;
  z-index: 2;
}

.loading-text,
.no-results,
.error-message {
  color: var(--text-light);
  font-size: 1.1rem;
  text-align: center;
  padding: 3rem 0;
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

.filter-section {
  background: linear-gradient(135deg, #ffeef1 0%, #fff5f7 100%);
  border: 2px solid var(--border-light);
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 3rem;
  box-shadow: var(--shadow-medium);
  animation: fadeInUp 0.6s ease-out;
}

.pet-card {
  border: 1px solid var(--border-light);
  border-radius: 12px;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-medium);
  overflow: hidden;
  background: var(--background-white);
  transform: translateY(20px);
  opacity: 0;
  animation: fadeInUp 0.5s ease forwards;
}

.pet-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-heavy);
  border-color: var(--primary-pink);
}

.pet-card:nth-child(odd) {
  animation-delay: 0.1s;
}

.pet-card:nth-child(even) {
  animation-delay: 0.2s;
}

.view-more-btn {
  background: var(--primary-pink);
  border: 2px solid var(--primary-pink);
  color: var(--text-dark);
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-size: 0.85rem;
  width: 100%;
}

.view-more-btn:hover {
  background: var(--primary-pink-dark);
  border-color: var(--primary-pink-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-heavy);
}

.btn-success {
  background: linear-gradient(135deg, #4ECDC4, #6EE7E7);
  border-color: #4ECDC4;
  color: white;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  width: 100%;
}

.btn-success:hover {
  background: linear-gradient(135deg, #1e8b81, #3cb7b0);
  /* darker gradient */
  border-color: #1e8b81;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(78, 205, 196, 0.4);
  color: white;
  /* keep text visible */
}

.personality {
  font-style: italic;
  color: var(--text-light);
  background: var(--background-light);
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  font-size: 0.9rem;
  border-left: 3px solid var(--primary-pink);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

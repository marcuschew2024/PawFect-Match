<template>
  <div class="container my-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="mb-0">My Favorite Pets</h1>
      <router-link to="/pets" class="btn btn-outline-primary">
        <i class="bi bi-arrow-left me-2"></i>Back to All Pets
      </router-link>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="col-12">
      <div class="loading-text">
        <i class="bi bi-arrow-repeat spinner me-2"></i>
        Loading your favorites...
      </div>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="col-12">
      <div class="error-message text-center">
        <i class="bi bi-exclamation-triangle display-4 text-warning mb-3"></i>
        <h4>Unable to Load Favorites</h4>
        <p class="mt-3">{{ error }}</p>
        <div class="mt-4">
          <button class="btn btn-primary me-2" @click="loadFavorites">
            <i class="bi bi-arrow-clockwise me-2"></i>Try Again
          </button>
        </div>
      </div>
    </div>
    
    <!-- Empty State -->
    <div v-else-if="favoritePets.length === 0" class="col-12">
      <div class="no-results text-center py-5">
        <i class="bi bi-heart display-1 text-muted mb-3"></i>
        <h4 class="text-muted">No favorites yet</h4>
        <p class="text-muted">Start browsing pets and add some to your favorites!</p>
        <router-link to="/pets" class="btn btn-primary mt-3">
          <i class="bi bi-search me-2"></i>Browse Pets
        </router-link>
      </div>
    </div>

    <!-- Favorites Grid -->
    <div v-else class="row mt-4">
      <div class="col-md-6 col-lg-4 mb-4" v-for="pet in favoritePets" :key="pet.id">
        <div class="card h-100 pet-card">
          <div class="position-relative">
            <img 
              :src="pet.displayImage" 
              :alt="pet.name"
              class="card-img-top"
              :class="{ 'image-loaded': pet.imageLoaded }"
              @load="onImageLoad(pet)"
              @error="onImageError(pet)"
              loading="lazy"
            >
            
            <!-- Compatibility Score Badge -->
            <div v-if="pet.compatibility_score" 
                 class="compatibility-badge">
              {{ pet.compatibility_score }}% Match
            </div>
            
            <!-- Favorite Button -->
            <button class="favorite-btn favorited" @click="removeFavorite(pet)">
              <i class="bi bi-heart-fill"></i>
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
            <div v-if="pet.compatibility_score" class="compatibility-meter mb-3">
              <div class="d-flex justify-content-between align-items-center mb-1">
                <small class="text-muted">Compatibility</small>
                <small class="fw-bold text-muted">
                  {{ pet.compatibility_score }}%
                </small>
              </div>
              <div class="progress" style="height: 6px;">
                <div class="progress-bar bg-primary" 
                     :style="{ width: pet.compatibility_score + '%' }"></div>
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
          
          <div class="card-footer bg-transparent">
            <div class="d-grid gap-2">
              <!-- View More Button -->
              <button class="btn view-more-btn" @click="viewPetDetails(pet)">
                <i class="bi bi-eye me-1"></i>View More
              </button>
              
              <!-- Remove Favorite Button -->
              <button class="btn btn-outline-danger btn-sm" @click="removeFavorite(pet)">
                <i class="bi bi-heart-fill me-1"></i>Remove Favorite
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Statistics -->
    <div v-if="favoritePets.length > 0" class="row mt-5">
      <div class="col-12">
        <div class="stats-card">
          <h4 class="mb-4">Your Favorites Summary</h4>
          <div class="row text-center">
            <div class="col-md-3 mb-3">
              <div class="stat-item">
                <div class="stat-number">{{ favoritePets.length }}</div>
                <div class="stat-label">Total Favorites</div>
              </div>
            </div>
            <div class="col-md-3 mb-3">
              <div class="stat-item">
                <div class="stat-number">{{ dogCount }}</div>
                <div class="stat-label">Dogs</div>
              </div>
            </div>
            <div class="col-md-3 mb-3">
              <div class="stat-item">
                <div class="stat-number">{{ catCount }}</div>
                <div class="stat-label">Cats</div>
              </div>
            </div>
            <div class="col-md-3 mb-3">
              <div class="stat-item">
                <div class="stat-number">{{ averageScore }}%</div>
                <div class="stat-label">Avg. Match Score</div>
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
  name: 'FavoritesPage',
  data() {
    return {
      favoritePets: [],
      loading: true,
      error: null,
      imageCache: new Map(),
      allDogBreeds: [],
      allCatBreeds: []
    }
  },
  computed: {
    dogCount() {
      return this.favoritePets.filter(pet => pet.type === 'dog').length;
    },
    catCount() {
      return this.favoritePets.filter(pet => pet.type === 'cat').length;
    },
    averageScore() {
      const petsWithScores = this.favoritePets.filter(pet => pet.compatibility_score);
      if (petsWithScores.length === 0) return 0;
      const total = petsWithScores.reduce((sum, pet) => sum + pet.compatibility_score, 0);
      return Math.round(total / petsWithScores.length);
    }
  },
  async mounted() {
    await this.loadAllBreeds();
    await this.loadFavorites();
  },
  methods: {
    async loadFavorites() {
      this.loading = true;
      this.error = null;
      
      try {
        const token = localStorage.getItem('authToken');
        if (!token) {
          this.$router.push('/login');
          return;
        }

        // Get favorite pet IDs
        const favoritesResponse = await fetch(`${API_BASE_URL}/user/favorites`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!favoritesResponse.ok) {
          throw new Error('Failed to load favorites');
        }

        const favoriteIds = await favoritesResponse.json();
        
        if (favoriteIds.length === 0) {
          this.favoritePets = [];
          this.loading = false;
          return;
        }

        // Get full pet details with scores
        const petsResponse = await fetch(`${API_BASE_URL}/pets/with-scores`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!petsResponse.ok) {
          throw new Error('Failed to load pet details');
        }

        const allPets = await petsResponse.json();
        
        // Filter to only include favorited pets
        const favoritePetsData = allPets.filter(pet => favoriteIds.includes(pet.id));
        
        // Process pets with images (same as PetListing page)
        this.favoritePets = await this.processPetsWithImages(favoritePetsData);

      } catch (error) {
        console.error('Error loading favorites:', error);
        this.error = error.message || 'Failed to load favorites';
      } finally {
        this.loading = false;
      }
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
              // Update the array to trigger reactivity
              this.favoritePets = [...this.favoritePets];
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

    async removeFavorite(pet) {
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/user/favorites/${pet.id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          // Remove from local array
          this.favoritePets = this.favoritePets.filter(p => p.id !== pet.id);
        } else {
          throw new Error('Failed to remove favorite');
        }
      } catch (error) {
        console.error('Error removing favorite:', error);
        alert('Error removing favorite. Please try again.');
      }
    },

    viewPetDetails(pet) {
      this.$router.push(`/pet/${pet.id}`);
    },

    getActivityClass(activity) {
      switch (activity) {
        case 'low': return 'bg-secondary';
        case 'medium': return 'bg-warning';
        case 'high': return 'bg-success';
        default: return 'bg-info';
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

    onImageLoad(pet) {
      pet.imageLoaded = true;
    },

    onImageError(pet) {
      if (pet.displayImage !== this.getColoredPlaceholder(pet)) {
        pet.displayImage = this.getColoredPlaceholder(pet);
        pet.placeholderImage = false;
      }
      pet.imageLoaded = true;
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
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
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

/* Statistics */
.stats-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(255, 182, 193, 0.15);
  border: 1px solid var(--border-light);
}

.stat-item {
  padding: 1rem;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--primary-pink-dark);
  line-height: 1;
}

.stat-label {
  color: var(--text-medium);
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 0.5rem;
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
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

    <!-- Favorites Grid - Same as PetListing -->
    <div v-else class="row mt-4">
      <div class="col-md-6 col-lg-4 mb-4" v-for="pet in favoritePets" :key="pet.id">
        <div class="card h-100 pet-card">
          <div class="position-relative">
            <img :src="pet.displayImage" :alt="pet.name" class="card-img-top"
              :class="{ 'image-loaded': pet.imageLoaded }" @load="onImageLoad(pet)" @error="onImageError(pet)"
              loading="lazy">

            <!-- Compatibility Badge - Same as PetListing -->
            <div v-if="pet.compatibility_score" class="compatibility-badge">
              {{ pet.compatibility_score }}% Match
            </div>

            <!-- Favorite Button - Same as PetListing -->
            <button class="favorite-btn favorited" @click="removeFavorite(pet)">
              <i class="bi bi-heart-fill"></i>
            </button>

            <!-- Image Source Badge - Same as PetListing -->
            <div v-if="pet.imageSource === 'api' && pet.imageLoaded" class="api-badge">
              AI Generated Image
            </div>
            <div v-else-if="pet.imageSource === 'database' && pet.imageLoaded" class="api-badge database-badge">
              Real Image
            </div>

            <div v-if="!pet.imageLoaded" class="image-loading">
              <i class="bi bi-arrow-repeat spinner"></i>
            </div>
          </div>

          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ pet.name }}</h5>

            <!-- Compatibility Meter - Same as PetListing -->
            <div v-if="pet.compatibility_score" class="compatibility-meter mb-3">
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

            <!-- Pet Details - Same as PetListing -->
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

          <!-- Card Footer - Same as PetListing but with Remove Favorite option -->
          <div class="card-footer bg-transparent">
            <div class="d-grid gap-2">
              <!-- View More Button - Same as PetListing -->
              <button class="btn view-more-btn" @click="viewPetDetails(pet)">
                <i class="bi me-1"></i>View More
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
    showToast(message, type = "info") {
      const toast = document.createElement("div");
      toast.className = `alert alert-${type === "error" ? "danger" : "success"} alert-dismissible fade show position-fixed`;
      toast.style.cssText = "top: 20px; right: 20px; z-index: 9999; min-width: 300px;";
      toast.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  `;
      document.body.appendChild(toast);

      setTimeout(() => {
        if (toast.parentNode) {
          toast.parentNode.removeChild(toast);
        }
      }, 5000);
    },
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
        let allPets = [];
        try {
          const petsResponse = await fetch(`${API_BASE_URL}/pets/with-scores`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });

          if (petsResponse.ok) {
            allPets = await petsResponse.json();
          } else {
            // Fallback to regular pets endpoint if with-scores fails
            const regularPetsResponse = await fetch(`${API_BASE_URL}/pets`, {
              headers: {
                'Authorization': `Bearer ${token}`
              }
            });
            if (regularPetsResponse.ok) {
              allPets = await regularPetsResponse.json();
            } else {
              throw new Error('Failed to load pet details');
            }
          }
        } catch (error) {
          console.log('Falling back to regular pets endpoint');
          const regularPetsResponse = await fetch(`${API_BASE_URL}/pets`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          if (regularPetsResponse.ok) {
            allPets = await regularPetsResponse.json();
          } else {
            throw new Error('Failed to load pet details');
          }
        }

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
        let displayImage = null;
        let imageSource = 'placeholder';

        // Use the exact same logic as PetListing page
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

        return {
          ...pet,
          displayImage: displayImage,
          imageLoaded: false,
          placeholderImage: imageSource === 'placeholder',
          imageSource: imageSource
        };
      });

      // Fetch API images for pets that need them (same as PetListing)
      this.fetchApiImagesForPets(processedPets);
      return processedPets;
    },

    async fetchApiImagesForPets(pets) {
      const petsNeedingImages = pets.filter(pet => pet.placeholderImage && pet.imageSource === 'placeholder');

      const batchSize = 3;

      for (let i = 0; i < petsNeedingImages.length; i += batchSize) {
        const batch = petsNeedingImages.slice(i, i + batchSize);
        const promises = batch.map(async (pet) => {
          try {
            const apiImage = await this.fetchPetImage(pet);
            if (apiImage) {
              pet.displayImage = apiImage;
              pet.image = apiImage;
              pet.placeholderImage = false;
              pet.imageSource = 'api';

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

      if (!breeds.length) {
        return null;
      }

      const normalizedBreedName = breedName.toLowerCase().trim();

      let breed = breeds.find(b =>
        b.name.toLowerCase().trim() === normalizedBreedName
      );

      if (breed) {
        return breed.id;
      }

      breed = breeds.find(b => {
        const apiName = b.name.toLowerCase().trim();
        return apiName.includes(normalizedBreedName) && normalizedBreedName.length >= 4;
      });

      if (breed) {
        return breed.id;
      }

      breed = breeds.find(b => {
        const apiName = b.name.toLowerCase().trim();
        return normalizedBreedName.includes(apiName) && apiName.length >= 4;
      });

      if (breed) {
        return breed.id;
      }

      const breedWords = normalizedBreedName.split(/\s+/);
      breed = breeds.find(b => {
        const apiWords = b.name.toLowerCase().trim().split(/\s+/);
        return breedWords.some(word =>
          word.length >= 4 && apiWords.includes(word)
        );
      });

      if (breed) {
        return breed.id;
      }

      return null;
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
          this.showToast("Removed from favorites", "success"); // Add this line
        } else {
          throw new Error('Failed to remove favorite');
        }
      } catch (error) {
        console.error('Error removing favorite:', error);
        this.showToast("Failed to remove favorite. Please try again.", "error"); // Add this line
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

    formatActivityLevel(activity) {
      const activityMap = {
        low: "Low",
        medium: "Medium",
        high: "High",
      };
      return activityMap[activity] || "Medium";
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
      if (pet.imageSource === 'database') {
        pet.placeholderImage = true;
        pet.imageSource = 'placeholder';
        this.fetchApiImageForSinglePet(pet);
      } else if (pet.imageSource === 'api') {
        pet.displayImage = this.getColoredPlaceholder(pet);
        pet.placeholderImage = false;
      } else {
        pet.displayImage = this.getColoredPlaceholder(pet);
        pet.placeholderImage = false;
      }

      pet.imageLoaded = true;
    },

    async fetchApiImageForSinglePet(pet) {
      try {
        const apiImage = await this.fetchPetImage(pet);
        if (apiImage) {
          pet.displayImage = apiImage;
          pet.image = apiImage;
          pet.placeholderImage = false;
          pet.imageSource = 'api';

          this.favoritePets = [...this.favoritePets];
        } else {
          pet.displayImage = this.getColoredPlaceholder(pet);
          pet.placeholderImage = false;
        }
      } catch (error) {
        console.error(`Error fetching API image for ${pet.name}:`, error);
        pet.displayImage = this.getColoredPlaceholder(pet);
        pet.placeholderImage = false;
      }
    }
  }
}
</script>

<style scoped>
/* Exact same styles as PetListing page */
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
  bottom: 12px;
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
  border-radius: 12px;
  border: 1px solid var(--border-light);
  z-index: 3;
}

.database-badge {
  background-color: rgba(76, 175, 80, 0.95) !important;
  color: white !important;
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
  background: linear-gradient(135deg, #ff868a 0%, #ffa6a6 100%);
  color: white;
  border: none;
  padding: 12px 25px;
  font-weight: 600;
  transition: all 0.3s ease;
  border-radius: 8px;
  width: 100%;
}

.view-more-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 154, 158, 0.4);
  background: linear-gradient(135deg, #eb7e7e 0%, #FF9A9E 100%);
  color: white;
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
<template>
  <div class="container my-5">
    <h1 class="text-center mb-4">Find Your Pawfect Match</h1>

    <!-- Enhanced Filter Section -->
    <div class="filter-section">
      <div class="row g-3 align-items-end">
        <!-- Search Input -->
        <div class="col-lg-3 col-md-6">
          <label for="searchInput" class="form-label">SEARCH PETS</label>
          <input type="text" class="form-control" id="searchInput" v-model="searchTerm"
            placeholder="Name, breed, or personality..." @input="applyFilters">
        </div>

        <!-- Size Filter -->
        <div class="col-lg-2 col-md-4 col-sm-6">
          <label for="sizeFilter" class="form-label">SIZE</label>
          <select class="form-select" id="sizeFilter" v-model="filters.size" @change="applyFilters">
            <option value="">All Sizes</option>
            <option value="Small">Small</option>
            <option value="Medium">Medium</option>
            <option value="Large">Large</option>
          </select>
        </div>

        <!-- Age Filter -->
        <div class="col-lg-2 col-md-4 col-sm-6">
          <label for="ageFilter" class="form-label">AGE</label>
          <select class="form-select" id="ageFilter" v-model="filters.age" @change="applyFilters">
            <option value="">All Ages</option>
            <option value="1 year old">1 year</option>
            <option value="2 years old">2 years</option>
            <option value="3 years old">3 years</option>
            <option value="4 years old">4 years</option>
            <option value="5 years old">5 years</option>
          </select>
        </div>

        <!-- Gender Filter -->
        <div class="col-lg-2 col-md-4 col-sm-6">
          <label for="genderFilter" class="form-label">GENDER</label>
          <select class="form-select" id="genderFilter" v-model="filters.gender" @change="applyFilters">
            <option value="">All Genders</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
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

      <div v-else class="col-md-6 col-lg-4 mb-4" v-for="(pet, index) in filteredPets" :key="pet.id">
        <div class="card h-100 pet-card">
          <div class="position-relative">
            <img 
              :ref="el => { if (el) petImageRefs[pet.id] = el }"
              :src="pet.displayImage" 
              :alt="pet.name" 
              class="card-img-top"
              :data-pet-id="pet.id"
              :data-pet-type="pet.type"
              :data-pet-breed="pet.breed"
              :data-needs-api="pet.needsApiImage"
              loading="lazy">
            <div v-if="pet.showApiBadge" class="api-badge">
              Placeholder Image
            </div>
          </div>
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ pet.name }}</h5>
            <p class="card-text mb-2 flex-grow-1">
              <strong>Age:</strong> {{ pet.age }}<br>
              <strong>Breed:</strong> {{ pet.breed }}<br>
              <strong>Size:</strong> {{ pet.size }}<br>
              <strong>Gender:</strong> {{ pet.gender }}
            </p>
            <p class="card-text personality">"{{ pet.personality }}"</p>
          </div>
          <div class="card-footer bg-transparent">
            <button class="btn view-more-btn w-100">View More</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const DOG_API_KEY = "live_m9FVcETQaok0LTSqCHAJrMMvkhBAIF2PfmvUMfwKq7n3zQIcDuHndLIerVPtmKEH";
const CAT_API_KEY = "live_m9FVcETQaok0LTSqCHAJrMMvkhBAIF2PfmvUMfwKq7n3zQIcDuHndLIerVPtmKEH";

const API_BASE_URL = 'http://localhost:3000/api';

export default {
  name: 'PetListingPage',
  data() {
    return {
      pets: [],
      filteredPets: [],
      searchTerm: '',
      filters: {
        size: '',
        age: '',
        gender: ''
      },
      loading: true,
      error: null,
      imageCache: new Map(),
      allDogBreeds: [],
      allCatBreeds: [],
      petImageRefs: {},
      imageObserver: null
    }
  },
  async mounted() {
    await this.initializePage();
  },
  beforeUnmount() {
    if (this.imageObserver) {
      this.imageObserver.disconnect();
    }
  },
  methods: {
    async initializePage() {
      await this.loadAllBreeds();
      await this.fetchPets();
      // Set up lazy loading after pets are displayed
      this.$nextTick(() => {
        this.setupLazyLoading();
      });
    },

    async loadAllBreeds() {
      try {
        console.log('Loading all breed data...');
        const [dogResponse, catResponse] = await Promise.all([
          fetch("https://api.thedogapi.com/v1/breeds", {
            headers: { "x-api-key": DOG_API_KEY }
          }),
          fetch("https://api.thecatapi.com/v1/breeds", {
            headers: { "x-api-key": CAT_API_KEY }
          })
        ]);

        this.allDogBreeds = await dogResponse.json();
        this.allCatBreeds = await catResponse.json();
        console.log(`Loaded ${this.allDogBreeds.length} dog breeds and ${this.allCatBreeds.length} cat breeds`);
      } catch (error) {
        console.error("Error fetching breed lists:", error);
      }
    },

    findBreedId(breedName, type) {
      const breeds = type === "dog" ? this.allDogBreeds : this.allCatBreeds;
      if (!breeds.length || !breedName) return null;

      const normalized = breedName.trim().toLowerCase();
      
      const breed = breeds.find(b => 
        b.name.toLowerCase().includes(normalized) ||
        normalized.includes(b.name.toLowerCase())
      );
      
      if (breed) {
        console.log(`Found breed match: ${breed.name} (ID: ${breed.id}) for search: ${breedName}`);
      } else {
        console.log(`No breed match found for: ${breedName}`);
      }
      
      return breed ? breed.id : null;
    },

    async fetchPetImage(pet) {
      const cacheKey = `${pet.type}-${pet.breed}`;
      if (this.imageCache.has(cacheKey)) {
        console.log(`Using cached image for ${pet.breed}`);
        return this.imageCache.get(cacheKey);
      }

      try {
        console.log(`Fetching API image for ${pet.name} (${pet.breed})`);
        const breedId = this.findBreedId(pet.breed, pet.type);
        const apiUrl = pet.type === "dog"
          ? "https://api.thedogapi.com/v1/images/search"
          : "https://api.thecatapi.com/v1/images/search";

        const apiKey = pet.type === "dog" ? DOG_API_KEY : CAT_API_KEY;

        const params = new URLSearchParams({
          limit: "1",
          has_breeds: "1"
        });

        if (breedId) {
          params.append("breed_ids", breedId);
        }

        const response = await fetch(`${apiUrl}?${params}`, {
          headers: { "x-api-key": apiKey }
        });

        const data = await response.json();
        console.log(`API response for ${pet.name}:`, data);

        let imageUrl;
        if (data && data.length > 0 && data[0].url) {
          imageUrl = data[0].url;
        } else {
          // Fallback - try without breed filter
          console.log(`No breed-specific image, trying fallback for ${pet.name}`);
          const fallbackResponse = await fetch(`${apiUrl}?limit=1`, {
            headers: { "x-api-key": apiKey }
          });
          const fallbackData = await fallbackResponse.json();
          imageUrl = fallbackData[0]?.url || "";
        }

        if (imageUrl) {
          this.imageCache.set(cacheKey, imageUrl);
          console.log(`Successfully fetched image for ${pet.name}: ${imageUrl}`);
        }
        
        return imageUrl;

      } catch (error) {
        console.error(`Error fetching image for ${pet.name}:`, error);
        return "";
      }
    },

    async fetchPets() {
      this.loading = true;
      this.error = null;

      try {
        console.log('Fetching pets from backend...');
        const response = await fetch(`${API_BASE_URL}/pets`);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Pets fetched from backend:', data);

        // Process pets with placeholders
        this.pets = data.map(pet => {
          const hasRealImage = pet.image && pet.image.trim() !== '' && pet.image !== 'placeholder';
          
          return {
            ...pet,
            displayImage: hasRealImage ? pet.image : this.getColoredPlaceholder(pet),
            needsApiImage: !hasRealImage,
            showApiBadge: false
          };
        });

        this.filteredPets = [...this.pets];
        console.log('Pets processed:', this.pets);

      } catch (error) {
        console.error('Error fetching pets:', error);
        this.error = `Failed to load pets: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },

    setupLazyLoading() {
      if (this.imageObserver) {
        this.imageObserver.disconnect();
      }

      this.imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            const petId = parseInt(img.dataset.petId);
            const needsApi = img.dataset.needsApi === 'true';

            if (needsApi) {
              const pet = this.pets.find(p => p.id === petId);
              if (pet) {
                this.loadImageForPet(img, pet);
              }
            }

            this.imageObserver.unobserve(img);
          }
        });
      }, {
        rootMargin: '50px'
      });

      // Observe all images that need API loading
      Object.values(this.petImageRefs).forEach(img => {
        if (img && img.dataset.needsApi === 'true') {
          this.imageObserver.observe(img);
        }
      });
    },

    async loadImageForPet(imgElement, pet) {
      console.log(`Loading image for ${pet.name} (${pet.breed})`);
      
      const apiImage = await this.fetchPetImage(pet);
      
      if (apiImage) {
        imgElement.src = apiImage;
        pet.displayImage = apiImage;
        pet.showApiBadge = true;
        pet.needsApiImage = false;
        this.$forceUpdate();
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

    applyFilters() {
      console.log('Applying filters:', {
        searchTerm: this.searchTerm,
        filters: this.filters
      });

      const filtered = this.pets.filter(pet => {
        const matchesSearch = !this.searchTerm ||
          pet.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          pet.breed.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          pet.personality.toLowerCase().includes(this.searchTerm.toLowerCase());

        const matchesSize = !this.filters.size || pet.size === this.filters.size;
        const matchesAge = !this.filters.age || pet.age === this.filters.age;
        const matchesGender = !this.filters.gender || pet.gender === this.filters.gender;

        return matchesSearch && matchesSize && matchesAge && matchesGender;
      });

      this.filteredPets = filtered;
      console.log(`Filtered to ${filtered.length} pets`);
      
      // Re-setup lazy loading for newly visible pets
      this.$nextTick(() => {
        this.setupLazyLoading();
      });
    },

    resetFilters() {
      console.log('Resetting filters');
      this.searchTerm = '';
      this.filters = {
        size: '',
        age: '',
        gender: ''
      };
      this.filteredPets = [...this.pets];
      console.log(`Showing all ${this.pets.length} pets`);
      
      this.$nextTick(() => {
        this.setupLazyLoading();
      });
    }
  }
}
</script>
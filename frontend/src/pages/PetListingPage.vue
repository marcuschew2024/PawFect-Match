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
            placeholder="Name, breed, or personality...">
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

        <!-- Age Filter -->
        <div class="col-lg-2 col-md-4 col-sm-6">
          <label for="ageFilter" class="form-label">AGE</label>
          <select class="form-select" id="ageFilter" v-model="filters.age">
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
          <select class="form-select" id="genderFilter" v-model="filters.gender">
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

      <div v-else class="col-md-6 col-lg-4 mb-4" v-for="pet in filteredPets" :key="pet.id">
        <div class="card h-100 pet-card">
          <div class="position-relative">
            <img :src="pet.displayImage" :alt="pet.name" class="card-img-top"
              :class="{ 'image-loaded': pet.imageLoaded }" @load="onImageLoad(pet)" @error="onImageError(pet)"
              loading="lazy">
            <div v-if="pet.placeholderImage && pet.imageLoaded" class="api-badge">
              Placeholder Image
            </div>
            <div v-if="!pet.imageLoaded" class="image-loading">
              <i class="bi bi-arrow-repeat spinner"></i>
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
      allCatBreeds: []
    }
  },
  async mounted() {
    await this.initializePage();
  },
  methods: {
    async initializePage() {
      // Start loading breeds in background
      this.loadAllBreeds();
      await this.fetchPets();
    },

    async loadAllBreeds() {
      try {
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
        console.log('Breeds loaded successfully');
      } catch (error) {
        console.error("Error fetching breed lists:", error);
      }
    },

    findBreedId(breedName, type) {
      const breeds = type === "dog" ? this.allDogBreeds : this.allCatBreeds;
      if (!breeds.length || !breedName) return null;

      const normalized = breedName.trim().toLowerCase();

      // Try exact match first
      let breed = breeds.find(b => b.name.toLowerCase() === normalized);
      if (breed) return breed.id;

      // Try partial match (only if exact fails)
      breed = breeds.find(b => normalized.includes(b.name.toLowerCase()) || b.name.toLowerCase().includes(normalized));
      if (breed) return breed.id;

      // Try handling common format differences (e.g., "Siberian Husky" vs "Husky, Siberian")
      const simplified = normalized.replace(/[^a-z\s]/g, "").split(" ").sort().join(" ");
      breed = breeds.find(b => {
        const breedSimplified = b.name.toLowerCase().replace(/[^a-z\s]/g, "").split(" ").sort().join(" ");
        return breedSimplified === simplified;
      });
      return breed ? breed.id : null;
    },

    async fetchPetImage(pet) {
      const cacheKey = `${pet.type}-${pet.breed}`;
      if (this.imageCache.has(cacheKey)) {
        console.log(`Using cached image for ${pet.breed}`);
        return this.imageCache.get(cacheKey);
      }

      try {
        console.log(`Fetching image for ${pet.name} (${pet.breed})`);
        const breedId = this.findBreedId(pet.breed, pet.type);
        const apiUrl = pet.type === "dog"
          ? "https://api.thedogapi.com/v1/images/search"
          : "https://api.thecatapi.com/v1/images/search";

        const apiKey = pet.type === "dog" ? DOG_API_KEY : CAT_API_KEY;

        const params = new URLSearchParams({
          limit: "1",
          size: "med"
        });

        if (breedId) {
          params.append("breed_ids", breedId);
        }

        const response = await fetch(`${apiUrl}?${params}`, {
          headers: { "x-api-key": apiKey }
        });

        if (!response.ok) {
          throw new Error(`API responded with status: ${response.status}`);
        }

        const data = await response.json();
        console.log('API response:', data);

        if (data && data.length > 0 && data[0].url) {
          const imageUrl = data[0].url;
          this.imageCache.set(cacheKey, imageUrl);
          console.log(`Successfully fetched image for ${pet.breed}:`, imageUrl);
          return imageUrl;
        } else {
          console.log(`No image found for ${pet.breed}`);
          return "";
        }

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

        // Process all pets immediately with proper image handling
        this.pets = await this.processPetsWithImages(data);
        // Initially show all pets (no filters applied)
        this.filteredPets = [...this.pets];
        console.log('Pets processed:', this.pets);

      } catch (error) {
        console.error('Error fetching pets:', error);
        this.error = `Failed to load pets: ${error.message}`;
      } finally {
        this.loading = false;
      }
    },

    async processPetsWithImages(pets) {
      const processedPets = pets.map(pet => {
        // For pets that already have images from database
        if (pet.image && pet.image.trim() !== '') {
          console.log(`Pet ${pet.name} has existing image:`, pet.image);
          return {
            ...pet,
            displayImage: pet.image,
            imageLoaded: false, // Will be set to true when image loads
            placeholderImage: false
          };
        } else {
          // For pets without images - start with colored placeholder
          console.log(`Pet ${pet.name} needs API image`);
          return {
            ...pet,
            displayImage: this.getColoredPlaceholder(pet),
            imageLoaded: false,
            placeholderImage: true // This pet will get an API image
          };
        }
      });

      // Fetch API images for pets that need them
      this.fetchApiImagesForPets(processedPets);

      return processedPets;
    },

    async fetchApiImagesForPets(pets) {
      const petsNeedingImages = pets.filter(pet => pet.placeholderImage);
      console.log(`Fetching API images for ${petsNeedingImages.length} pets`);

      // Process in small batches to avoid overwhelming the API
      const batchSize = 3;
      for (let i = 0; i < petsNeedingImages.length; i += batchSize) {
        const batch = petsNeedingImages.slice(i, i + batchSize);

        const promises = batch.map(async (pet) => {
          try {
            const apiImage = await this.fetchPetImage(pet);
            if (apiImage) {
              console.log(`Updating ${pet.name} with API image:`, apiImage);
              // Update the pet's display image
              pet.displayImage = apiImage;
              pet.image = apiImage; // Also update the original image field

              // Force Vue reactivity by reassigning the array
              this.pets = [...this.pets];
              this.filteredPets = [...this.filteredPets];
            } else {
              console.log(`No API image found for ${pet.name}, keeping placeholder`);
            }
          } catch (error) {
            console.error(`Failed to fetch API image for ${pet.name}:`, error);
          }
        });

        await Promise.allSettled(promises);

        // Small delay between batches to be nice to the API
        if (i + batchSize < petsNeedingImages.length) {
          await new Promise(resolve => setTimeout(resolve, 500));
        }
      }

      console.log('Finished fetching all API images');
    },

    getColoredPlaceholder(pet) {
      // Create a nice colored placeholder based on pet type
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
      console.log(`Image loaded for ${pet.name}`);
      pet.imageLoaded = true;
    },

    onImageError(pet) {
      console.log(`Image failed to load for ${pet.name}:`, pet.displayImage);
      // If the real image fails, fall back to colored placeholder
      if (pet.displayImage !== this.getColoredPlaceholder(pet)) {
        pet.displayImage = this.getColoredPlaceholder(pet);
        pet.placeholderImage = false;
      }
      pet.imageLoaded = true;
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
    },

    resetFilters() {
      console.log('Resetting filters');
      this.searchTerm = '';
      this.filters = {
        size: '',
        age: '',
        gender: ''
      };
      // Show all pets again
      this.filteredPets = [...this.pets];
      console.log(`Showing all ${this.pets.length} pets`);
    }
  }
}
</script>
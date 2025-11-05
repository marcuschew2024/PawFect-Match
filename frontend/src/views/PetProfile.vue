<template>
  <div class="pet-profile-page">
    <div class="container my-4">
      <!-- Back Button -->
      <div class="mb-4">
        <button @click="$router.back()" class="btn btn-outline-primary btn-back">
          <i class="bi bi-arrow-left me-2"></i>Back to Pets
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2 text-muted">Loading pet details...</p>
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
          <div class="card shadow-lg border-0 profile-card">
            <div class="card-body p-0">
              <!-- Image Display -->
              <div class="pet-image-container position-relative">
                <!-- Multiple Images with Manual Carousel -->
                <div v-if="validImages.length > 1" class="carousel-container">
                  <div class="carousel manual-carousel">
                    <div class="carousel-inner">
                      <div 
                        v-for="(img, index) in validImages" 
                        :key="index" 
                        class="carousel-item"
                        :class="{ active: index === currentImageIndex }"
                      >
                        <img 
                          v-if="imageLoadedStates[getImageUrl(img)]"
                          :src="getImageUrl(img)" 
                          :alt="`${pet.name} - Image ${index + 1}`" 
                          class="pet-image d-block w-100 image-loaded"
                          loading="lazy"
                        >
                        <div v-else class="image-loading-placeholder">
                          <i class="bi bi-arrow-repeat spinner"></i>
                          <span>Loading image...</span>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Manual Controls -->
                    <button class="carousel-control-prev manual-control" @click="prevImage">
                      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                      <span class="visually-hidden">Previous</span>
                    </button>
                    <button class="carousel-control-next manual-control" @click="nextImage">
                      <span class="carousel-control-next-icon" aria-hidden="true"></span>
                      <span class="visually-hidden">Next</span>
                    </button>
                    
                    <!-- Manual Indicators -->
                    <div class="carousel-indicators manual-indicators">
                      <button 
                        v-for="(img, index) in validImages" 
                        :key="index" 
                        type="button"
                        :class="{ active: index === currentImageIndex }" 
                        @click="currentImageIndex = index"
                        :aria-label="`Slide ${index + 1}`"
                      ></button>
                    </div>
                  </div>

                  <!-- Image Counter -->
                  <div class="image-counter">
                    <i class="bi bi-camera me-1"></i>
                    {{ currentImageIndex + 1 }} / {{ validImages.length }}
                  </div>
                </div>

                <!-- Single Image -->
                <div v-else-if="validImages.length === 1" class="single-image-container">
                  <img 
                    v-if="imageLoadedStates[getImageUrl(validImages[0])]"
                    :src="getImageUrl(validImages[0])" 
                    :alt="pet.name" 
                    class="pet-image single-image image-loaded"
                    loading="lazy"
                  >
                  <div v-else class="image-loading-placeholder single">
                    <i class="bi bi-arrow-repeat spinner"></i>
                    <span>Loading image...</span>
                  </div>
                </div>

                <!-- No Valid Images - Show Placeholder -->
                <div v-else class="single-image-container">
                  <img :src="placeholderImage" :alt="pet.name" class="pet-image single-image image-loaded">
                </div>

                <!-- Image Source Badge -->
                <div v-if="hasAnyImageLoaded && pet.imageSource === 'api'" class="api-badge">
                  AI Generated Image
                </div>
                <div v-else-if="hasAnyImageLoaded && pet.imageSource === 'database'" class="api-badge database-badge">
                  Real Image
                </div>
                <div v-else-if="hasAnyImageLoaded && pet.imageSource === 'placeholder'" class="api-badge">
                  Placeholder Image
                </div>

                <!-- Compatibility Badge -->
                <div v-if="hasCompletedQuiz && pet.compatibility_score" class="compatibility-badge">
                  <i class="bi bi-star-fill me-1"></i>
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

              <!-- Pet Basic Info Card -->
              <div class="p-4">
                <div class="pet-basic-info">
                  <h1 class="pet-name">{{ pet.name }}</h1>
                  <div class="pet-meta">
                    <span class="pet-breed">{{ pet.breed }}</span>
                    <span class="pet-type-badge">{{ pet.type }}</span>
                  </div>

                  <!-- Quick Stats -->
                  <div class="quick-stats">
                    <div class="stat-item">
                      <i class="bi bi-calendar3"></i>
                      <span>{{ pet.age }}</span>
                    </div>
                    <div class="stat-item">
                      <i class="bi bi-gender-ambiguous"></i>
                      <span>{{ pet.gender }}</span>
                    </div>
                    <div class="stat-item">
                      <i class="bi bi-rulers"></i>
                      <span>{{ pet.size }}</span>
                    </div>
                  </div>
                </div>

                <!-- Favourite button -->
                <div class="favorite-section">
                  <button v-if="isAuthenticated" class="favourite-btn w-100"
                    :class="isFavorite ? 'btn-favorited' : 'btn-favorite'" @click="toggleFavorite"
                    :disabled="favoriteLoading">
                    <i class="bi me-2" :class="isFavorite ? 'bi-heart-fill' : 'bi-heart'"></i>
                    {{ isFavorite ? 'Remove from Favorites' : 'Add to Favorites' }}
                  </button>
                </div>

                <!-- Action Buttons -->
                <div class="action-buttons mt-4">
                  <div class="d-grid gap-2">
                    <!-- Adopt Button -->
                    <button v-if="isAuthenticated && !pet.is_adopted" class="btn btn-adopt btn-lg py-3"
                      @click="startAdoption" :disabled="adopting">
                      <span v-if="adopting" class="spinner-border spinner-border-sm me-2"></span>
                      <i v-else class="bi bi-heart me-2"></i>
                      {{ adopting ? "Processing..." : `Adopt ${pet.name}` }}
                    </button>

                    <!-- Login to Adopt -->
                    <button v-else-if="!isAuthenticated && !pet.is_adopted" class="btn btn-adopt btn-lg py-3"
                      @click="$router.push('/login')">
                      <i class="bi bi-person me-2"></i>Login to Adopt
                    </button>

                    <!-- Already Adopted -->
                    <div v-else class="adopted-message text-center py-3">
                      <i class="bi bi-check-circle-fill text-success display-6 mb-3"></i>
                      <h5 class="text-success">Congratulations!</h5>
                      <p class="text-muted mb-0">This pet has found a loving home!</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column - Pet Details -->
        <div class="col-xl-7 col-lg-6">
          <!-- Personality & Background Section -->
          <div class="card shadow-lg border-0 profile-card mb-4">
            <div class="card-body p-4">
              <!-- Personality -->
              <div class="section-personality mb-4">
                <h4 class="section-title">
                  <i class="bi bi-chat-heart-fill text-primary me-2"></i>
                  Personality
                </h4>
                <div class="personality-content">
                  <p class="mb-0">"{{ pet.personality }}"</p>
                </div>
              </div>

              <!-- Background Story -->
              <div class="section-background" v-if="pet.background">
                <h4 class="section-title">
                  <i class="bi bi-book-half text-warning me-2"></i>
                  Background Story
                </h4>
                <div class="background-content">
                  <p class="mb-0">{{ pet.background }}</p>
                </div>
              </div>

              <!-- Additional Background Information -->
              <div class="section-background-details" v-if="hasBackgroundDetails">
                <h4 class="section-title">
                  <i class="bi bi-info-circle text-info me-2"></i>
                  Background Details
                </h4>
                <div class="background-details-content">
                  <div class="row g-3">
                    <!-- Previous Home Environment -->
                    <div class="col-md-6" v-if="pet.previous_home_environment">
                      <div class="background-detail-item">
                        <i class="bi bi-house-door text-success"></i>
                        <div>
                          <div class="detail-label">Previous Home</div>
                          <div class="detail-value">{{ pet.previous_home_environment }}</div>
                        </div>
                      </div>
                    </div>

                    <!-- Reason for Surrender -->
                    <div class="col-md-6" v-if="pet.reason_for_surrender">
                      <div class="background-detail-item">
                        <i class="bi bi-heartbreak text-danger"></i>
                        <div>
                          <div class="detail-label">Reason for Surrender</div>
                          <div class="detail-value">{{ pet.reason_for_surrender }}</div>
                        </div>
                      </div>
                    </div>

                    <!-- Time in Shelter -->
                    <div class="col-md-6" v-if="pet.time_in_shelter">
                      <div class="background-detail-item">
                        <i class="bi bi-clock text-warning"></i>
                        <div>
                          <div class="detail-label">Time in Shelter</div>
                          <div class="detail-value">{{ pet.time_in_shelter }}</div>
                        </div>
                      </div>
                    </div>

                    <!-- Special Needs -->
                    <div class="col-md-6" v-if="pet.special_needs">
                      <div class="background-detail-item">
                        <i class="bi bi-heart-pulse text-info"></i>
                        <div>
                          <div class="detail-label">Special Needs</div>
                          <div class="detail-value">{{ pet.special_needs }}</div>
                        </div>
                      </div>
                    </div>

                    <!-- Rescue Story -->
                    <div class="col-12" v-if="pet.rescue_story">
                      <div class="background-detail-item full-width">
                        <i class="bi bi-star text-warning"></i>
                        <div>
                          <div class="detail-label">Rescue Story</div>
                          <div class="detail-value">{{ pet.rescue_story }}</div>
                        </div>
                      </div>
                    </div>

                    <!-- Behavioral Notes -->
                    <div class="col-12" v-if="pet.behavioral_notes">
                      <div class="background-detail-item full-width">
                        <i class="bi bi-clipboard-heart text-primary"></i>
                        <div>
                          <div class="detail-label">Behavioral Notes</div>
                          <div class="detail-value">{{ pet.behavioral_notes }}</div>
                        </div>
                      </div>
                    </div>

                    <!-- Training Status -->
                    <div class="col-md-6" v-if="pet.training_status">
                      <div class="background-detail-item">
                        <i class="bi bi-award text-success"></i>
                        <div>
                          <div class="detail-label">Training Status</div>
                          <div class="detail-value">{{ pet.training_status }}</div>
                        </div>
                      </div>
                    </div>

                    <!-- Favorite Activities -->
                    <div class="col-md-6" v-if="pet.favorite_activities">
                      <div class="background-detail-item">
                        <i class="bi bi-emoji-smile text-warning"></i>
                        <div>
                          <div class="detail-label">Favorite Activities</div>
                          <div class="detail-value">{{ pet.favorite_activities }}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- No Background Message -->
              <div v-else-if="!pet.background" class="no-background-message text-center py-4">
                <i class="bi bi-book text-muted display-4 mb-3"></i>
                <h5 class="text-muted">Background Information</h5>
                <p class="text-muted mb-0">No background information available for {{ pet.name }} yet.</p>
              </div>
            </div>
          </div>

          <!-- Compatibility Section -->
          <div v-if="hasCompletedQuiz && pet.compatibility_score" class="card shadow-lg border-0 profile-card mb-4">
            <div class="card-body p-4">
              <h4 class="section-title mb-3">
                <i class="bi bi-graph-up-arrow text-info me-2"></i>
                Your Compatibility
              </h4>
              <div class="compatibility-section">
                <div class="compatibility-header">
                  <span class="compatibility-label">Match with {{ pet.name }}</span>
                  <span class="compatibility-score">{{ pet.compatibility_score }}%</span>
                </div>
                <div class="progress compatibility-progress">
                  <div class="progress-bar" :class="getCompatibilityClass(pet.compatibility_score)"
                    :style="{ width: pet.compatibility_score + '%' }"></div>
                </div>
                <div class="compatibility-description mt-2">
                  <small class="text-muted">
                    <i class="bi bi-info-circle me-1"></i>
                    {{ getCompatibilityDescription(pet.compatibility_score) }}
                  </small>
                </div>
              </div>
            </div>
          </div>

          <!-- Details Grid -->
          <div class="row g-4">
            <!-- Health & Medical -->
            <div class="col-md-6">
              <div class="card shadow-lg border-0 profile-card h-100">
                <div class="card-body">
                  <h5 class="section-title-sm">
                    <i class="bi bi-heart-pulse text-danger me-2"></i>
                    Health & Medical
                  </h5>
                  <div class="details-list">
                    <div class="detail-item">
                      <span class="detail-label">Vaccination Status</span>
                      <span class="detail-value" :class="getVaccinationStatusClass()">
                        {{ pet.vaccination_status || "Unknown" }}
                      </span>
                    </div>
                    <div class="detail-item">
                      <span class="detail-label">Vaccinated</span>
                      <span class="detail-value" :class="getBooleanStatusClass(pet.vaccinated)">
                        {{ getBooleanDisplay(pet.vaccinated) }}
                      </span>
                    </div>
                    <div class="detail-item">
                      <span class="detail-label">Neutered/Spayed</span>
                      <span class="detail-value" :class="getBooleanStatusClass(pet.neutered)">
                        {{ getBooleanDisplay(pet.neutered) }}
                      </span>
                    </div>
                    <div class="detail-item" v-if="pet.health_info">
                      <span class="detail-label">Health Notes</span>
                      <span class="detail-value text-muted small">{{ pet.health_info }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Home Compatibility -->
            <div class="col-md-6">
              <div class="card shadow-lg border-0 profile-card h-100">
                <div class="card-body">
                  <h5 class="section-title-sm">
                    <i class="bi bi-house-check text-success me-2"></i>
                    Home Compatibility
                  </h5>
                  <div class="details-list">
                    <div class="detail-item">
                      <span class="detail-label">Good with Children</span>
                      <span class="detail-value" :class="getBooleanStatusClass(pet.good_with_children)">
                        {{ getBooleanDisplay(pet.good_with_children) }}
                      </span>
                    </div>
                    <div class="detail-item">
                      <span class="detail-label">Good with Other Pets</span>
                      <span class="detail-value" :class="getBooleanStatusClass(pet.good_with_other_pets)">
                        {{ getBooleanDisplay(pet.good_with_other_pets) }}
                      </span>
                    </div>
                    <div class="detail-item">
                      <span class="detail-label">Activity Level</span>
                      <span class="detail-value">
                        <span class="badge" :class="getActivityClass(pet.activity_level)">
                          {{ formatActivityLevel(pet.activity_level) }}
                        </span>
                      </span>
                    </div>
                    <div class="detail-item">
                      <span class="detail-label">HDB Approved</span>
                      <span class="detail-value" :class="getBooleanStatusClass(pet.hdb_approved)">
                        {{ getBooleanDisplay(pet.hdb_approved) }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Additional Information -->
            <div class="col-12">
              <div class="card shadow-lg border-0 profile-card">
                <div class="card-body">
                  <h5 class="section-title-sm">
                    <i class="bi bi-info-circle text-primary me-2"></i>
                    Additional Information
                  </h5>
                  <div class="row g-3">
                    <div class="col-md-6">
                      <div class="info-item-extended">
                        <i class="bi bi-cash-coin text-warning"></i>
                        <div>
                          <div class="info-label">Adoption Fee</div>
                          <div class="info-value">${{ pet.adoption_fee || 'Free' }}</div>
                        </div>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="info-item-extended">
                        <i class="bi bi-geo-alt text-info"></i>
                        <div>
                          <div class="info-label">Location</div>
                          <div class="info-value">{{ pet.location || 'Singapore' }}</div>
                        </div>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="info-item-extended">
                        <i class="bi bi-palette text-purple"></i>
                        <div>
                          <div class="info-label">Fur Color</div>
                          <div class="info-value">{{ pet.furColor || pet.fur_color || 'Not specified' }}</div>
                        </div>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="info-item-extended">
                        <i class="bi bi-building text-success"></i>
                        <div>
                          <div class="info-label">Living Space</div>
                          <div class="info-value">{{ getLivingSituation(pet.size) }}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- HDB Requirements -->
            <div v-if="pet.hdb_approved" class="col-12">
              <div class="card shadow-lg border-0 profile-card hdb-card">
                <div class="card-body">
                  <h5 class="section-title-sm text-success">
                    <i class="bi bi-building-check me-2"></i>
                    HDB Approved - Requirements
                  </h5>
                  <div class="hdb-requirements">
                    <div v-if="pet.type === 'cat'" class="hdb-item">
                      <i class="bi bi-check-circle-fill text-success"></i>
                      <span>HDB permits up to 2 cats per household</span>
                    </div>
                    <div v-if="pet.type === 'cat'" class="hdb-item">
                      <i class="bi bi-check-circle-fill text-success"></i>
                      <span>Windows and gates must be meshed up for safety</span>
                    </div>
                    <div v-if="pet.type === 'dog'" class="hdb-item">
                      <i class="bi bi-check-circle-fill text-success"></i>
                      <span>HDB regulations permit only one dog per flat</span>
                    </div>
                    <div class="hdb-item">
                      <i class="bi bi-check-circle-fill text-success"></i>
                      <span>This pet meets all HDB requirements for adoption</span>
                    </div>
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
  name: "PetProfile",
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
      imageLoadedStates: {},
      currentImageIndex: 0,
      validImages: [],
      failedImages: new Set(),
      placeholderImage: '',
      imagesLoading: true
    };
  },

  computed: {
    hasAnyImageLoaded() {
      return Object.values(this.imageLoadedStates).some(state => state === true);
    },
    
    hasBackgroundDetails() {
      return this.pet && (
        this.pet.previous_home_environment ||
        this.pet.reason_for_surrender ||
        this.pet.time_in_shelter ||
        this.pet.special_needs ||
        this.pet.rescue_story ||
        this.pet.behavioral_notes ||
        this.pet.training_status ||
        this.pet.favorite_activities
      );
    }
  },

  async mounted() {
    await this.initializePage();
  },

  watch: {
    "$route.params.petId": {
      handler() {
        this.initializePage();
      },
      immediate: false,
    },
  },

  methods: {
    async initializePage() {
      this.checkAuth();

      if (this.isAuthenticated) {
        await this.checkQuizCompletion();
      }

      await this.loadPetDetails();

      if (this.isAuthenticated) {
        await this.checkFavoriteStatus();
      }
    },

    checkAuth() {
      const token = localStorage.getItem("authToken");
      this.isAuthenticated = !!token;
    },

    async loadPetDetails() {
      this.loading = true;
      this.error = null;
      this.imageLoadedStates = {};
      this.currentImageIndex = 0;
      this.validImages = [];
      this.failedImages = new Set();
      this.imagesLoading = true;

      try {
        const petId = this.$route.params.petId;
        console.log("Loading pet details for ID:", petId);

        const token = localStorage.getItem("authToken");
        const headers = {
          "Content-Type": "application/json",
        };

        if (token) {
          headers["Authorization"] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_BASE_URL}/pets/${petId}`, { headers });

        if (response.ok) {
          const petData = await response.json();
          console.log("✅ Pet data loaded:", petData);
          
          this.pet = this.processPetWithImages(petData);
          console.log("✅ Processed pet with images:", this.pet);
          
          // Start with all images as valid, but don't mark them as loaded yet
          this.validImages = [...this.pet.images];
          this.placeholderImage = this.getColoredPlaceholder(this.pet);
          
          // Pre-load images to check which ones are valid
          await this.preloadImages();
        } else if (response.status === 404) {
          this.error = "Pet not found.";
        } else {
          const errorData = await response.json().catch(() => ({}));
          this.error = errorData.error || "Error loading pet details.";
        }
      } catch (error) {
        console.error("❌ Error loading pet:", error);
        this.error = "Network error. Please try again.";
      } finally {
        this.loading = false;
      }
    },

    // Pre-load images to determine which ones are valid
    async preloadImages() {
      if (this.validImages.length === 0) {
        this.imagesLoading = false;
        return;
      }

      const loadPromises = this.validImages.map(async (img, index) => {
        const imageUrl = this.getImageUrl(img);
        return new Promise((resolve) => {
          const image = new Image();
          image.onload = () => {
            console.log('✅ Image pre-loaded successfully:', imageUrl);
            this.imageLoadedStates[imageUrl] = true;
            resolve({ url: imageUrl, success: true });
          };
          image.onerror = () => {
            console.log('❌ Image failed to pre-load:', imageUrl);
            this.failedImages.add(imageUrl);
            this.imageLoadedStates[imageUrl] = false;
            resolve({ url: imageUrl, success: false });
          };
          image.src = imageUrl;
        });
      });

      const results = await Promise.all(loadPromises);
      
      // Filter out failed images
      this.validImages = this.validImages.filter(img => {
        const url = this.getImageUrl(img);
        return !this.failedImages.has(url);
      });
      
      // Reset current image index if needed
      if (this.currentImageIndex >= this.validImages.length) {
        this.currentImageIndex = Math.max(0, this.validImages.length - 1);
      }
      
      this.imagesLoading = false;
      console.log('🔄 Final valid images after pre-loading:', this.validImages);
    },

    processPetWithImages(pet) {
      console.log("🖼 Processing images for pet:", pet.name);
      console.log("📸 Raw pet images data:", pet.images);
      
      let images = [];
      let displayImage = '';
      let imageSource = 'placeholder';

      if (pet.images && Array.isArray(pet.images) && pet.images.length > 0) {
        console.log("📸 Found images array with", pet.images.length, "images");
        
        images = pet.images.map(img => {
          if (typeof img === 'object' && img.image_url) {
            return img.image_url;
          } else if (typeof img === 'string') {
            return img;
          }
          return null;
        }).filter(url => url !== null && url.trim() !== '');

        console.log("📸 Extracted image URLs:", images);
        
        if (images.length > 0) {
          displayImage = images[0];
          imageSource = 'database';
        }
      }
      
      if (!displayImage && pet.main_image && pet.main_image.trim() !== '') {
        console.log("🖼 Using main_image as fallback:", pet.main_image);
        images = [pet.main_image];
        displayImage = pet.main_image;
        imageSource = 'database';
      } else if (!displayImage && pet.image && pet.image.trim() !== '') {
        console.log("🖼 Using image field as fallback:", pet.image);
        images = [pet.image];
        displayImage = pet.image;
        imageSource = 'database';
      }
      
      if (!displayImage || images.length === 0) {
        console.log("🖼 No images found, using placeholder");
        displayImage = this.getColoredPlaceholder(pet);
        imageSource = 'placeholder';
        images = [displayImage];
      }

      console.log("🎯 Final images array:", images);
      console.log("🎯 Display image:", displayImage);
      console.log("🎯 Image source:", imageSource);

      const processedPet = {
        ...pet,
        images: images,
        displayImage: displayImage,
        placeholderImage: imageSource === 'placeholder',
        imageSource: imageSource
      };

      return processedPet;
    },

    // Manual carousel navigation
    nextImage() {
      if (this.validImages && this.validImages.length > 1) {
        this.currentImageIndex = (this.currentImageIndex + 1) % this.validImages.length;
      }
    },

    prevImage() {
      if (this.validImages && this.validImages.length > 1) {
        this.currentImageIndex = (this.currentImageIndex - 1 + this.validImages.length) % this.validImages.length;
      }
    },

    getImageUrl(img) {
      if (typeof img === 'object') {
        if (img.image_url) {
          return img.image_url;
        } else if (img.url) {
          return img.url;
        }
      }
      return img;
    },

    getColoredPlaceholder(pet) {
      const colors = {
        dog: ['#ffb6c1', '#ffd1dc', '#ffecb3', '#c8e6c9'],
        cat: ['#bbdefb', '#c5cae9', '#e1bee7', '#f8bbd0']
      };
      const typeColors = colors[pet.type] || colors.dog;
      const color = typeColors[pet.id % typeColors.length];
      const emoji = pet.type === 'dog' ? '🐕' : '🐱';

      return `data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" viewBox="0 0 400 300"><rect fill="${color}" width="400" height="300"/><text fill="#666" font-size="48" font-family="system-ui" x="200" y="150" text-anchor="middle" dominant-baseline="middle">${emoji}</text><text fill="#333" font-size="24" font-family="system-ui" x="200" y="200" text-anchor="middle">${pet.name}</text></svg>`;
    },

    async checkQuizCompletion() {
      try {
        const token = localStorage.getItem("authToken");
        const response = await fetch(`${API_BASE_URL}/user/quiz`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        this.hasCompletedQuiz = response.ok;
      } catch (error) {
        console.log("No quiz results found");
        this.hasCompletedQuiz = false;
      }
    },

    async checkFavoriteStatus() {
      try {
        const token = localStorage.getItem("authToken");
        const response = await fetch(`${API_BASE_URL}/user/favorites`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const favoriteIds = await response.json();
          this.isFavorite = favoriteIds.includes(parseInt(this.$route.params.petId));
        }
      } catch (error) {
        console.error("Error checking favorite status:", error);
      }
    },

    getBooleanStatusClass(value) {
      if (value === true) return 'status-yes';
      if (value === false) return 'status-no';
      return 'status-unknown';
    },

    getBooleanDisplay(value) {
      if (value === true) return 'Yes';
      if (value === false) return 'No';
      return 'Unknown';
    },

    getVaccinationStatusClass() {
      const status = this.pet.vaccination_status?.toLowerCase();
      if (status?.includes("up to date") || status?.includes("vaccinated")) {
        return "status-yes";
      } else if (status?.includes("not") || status?.includes("unknown")) {
        return "status-no";
      }
      return "status-unknown";
    },

    async toggleFavorite() {
      if (!this.isAuthenticated) {
        this.$router.push("/login");
        return;
      }

      this.favoriteLoading = true;
      try {
        const token = localStorage.getItem("authToken");
        const petId = this.$route.params.petId;

        if (this.isFavorite) {
          await fetch(`${API_BASE_URL}/user/favorites/${petId}`, {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          this.isFavorite = false;
          this.showToast("Removed from favorites", "success");
        } else {
          await fetch(`${API_BASE_URL}/user/favorites`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ pet_id: parseInt(petId) }),
          });
          this.isFavorite = true;
          this.showToast("Added to favorites!", "success");
        }
      } catch (error) {
        console.error("Error toggling favorite:", error);
        this.showToast("Failed to update favorites. Please try again.", "error");
      } finally {
        this.favoriteLoading = false;
      }
    },

    async startAdoption() {
      if (!this.isAuthenticated) {
        this.$router.push("/login");
        return;
      }

      if (this.pet.is_adopted) {
        this.showToast("This pet has already been adopted!", "error");
        return;
      }

      this.$router.push(`/adopt/${this.pet.id}`);
    },

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

    getActivityClass(activity) {
      const activityMap = {
        low: "activity-low",
        medium: "activity-medium",
        high: "activity-high",
      };
      return activityMap[activity] || "activity-medium";
    },

    formatActivityLevel(activity) {
      const activityMap = {
        low: "Low",
        medium: "Medium",
        high: "High",
      };
      return activityMap[activity] || "Medium";
    },

    getCompatibilityClass(score) {
      if (score >= 80) return "bg-success";
      if (score >= 60) return "bg-warning";
      return "bg-danger";
    },

    getCompatibilityDescription(score) {
      if (score >= 80) return "Excellent match! This pet fits perfectly with your lifestyle.";
      if (score >= 60) return "Good match! This pet would be a great companion.";
      if (score >= 40) return "Fair match. Consider if you can accommodate their needs.";
      return "This pet may not be the best fit for your current situation.";
    },

    getLivingSituation(size) {
      const sizeMap = {
        Small: "Apartments and small homes",
        Medium: "Most homes with space",
        Large: "Homes with yards or large spaces",
      };
      return sizeMap[size] || "Various living situations";
    },
  }
};
</script>
<style scoped>
.background-details-content {
  margin-top: 1rem;
}

.background-detail-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 12px;
  margin-bottom: 0.75rem;
  transition: all 0.3s ease;
}

.background-detail-item:hover {
  background: #e9ecef;
  transform: translateX(5px);
}

.background-detail-item.full-width {
  flex-direction: column;
  align-items: flex-start;
}

.background-detail-item i {
  font-size: 1.5rem;
  width: 40px;
  text-align: center;
  flex-shrink: 0;
}

.background-detail-item .detail-label {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
  font-weight: 500;
}

.background-detail-item .detail-value {
  font-weight: 500;
  color: #2c3e50;
  line-height: 1.5;
}

.no-background-message {
  border: 2px dashed #dee2e6;
  border-radius: 15px;
  background: #f8f9fa;
}

/* Rest of the existing styles remain the same */
.image-loading-placeholder {
  width: 100%;
  height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  color: #6c757d;
  border-radius: 20px 20px 0 0;
}

.image-loading-placeholder.single {
  border-radius: 20px 20px 0 0;
}

.image-loading-placeholder .spinner {
  font-size: 2rem;
  margin-bottom: 1rem;
  animation: spin 1s linear infinite;
}

.image-loading-placeholder span {
  font-size: 0.9rem;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.pet-profile-page {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  min-height: 100vh;
  padding: 1rem 0;
}

.pet-profile-page {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  min-height: 100vh;
  padding: 1rem 0;
}

/* Back Button */
.btn-back {
  border-radius: 25px;
  padding: 8px 20px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-back:hover {
  transform: translateX(-5px);
  background-color: #007bff;
  color: white;
}

/* Card Styling */
.profile-card {
  border: none;
  border-radius: 20px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.profile-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15) !important;
}

/* Image Container */
.pet-image-container {
  position: relative;
  background: #f8f9fa;
  overflow: hidden;
}

.carousel-container {
  position: relative;
}

.pet-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.single-image {
  border-radius: 20px 20px 0 0;
}

.pet-image:hover {
  transform: scale(1.02);
}

/* Manual Carousel Styles */
.manual-carousel {
  position: relative;
  overflow: hidden;
  border-radius: 20px 20px 0 0;
}

.manual-carousel .carousel-inner {
  position: relative;
  width: 100%;
}

.manual-carousel .carousel-item {
  display: none;
  transition: opacity 0.5s ease;
}

.manual-carousel .carousel-item.active {
  display: block;
}

.manual-control {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.5);
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin: 0 15px;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 5;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.manual-control:hover {
  background: rgba(0, 0, 0, 0.7);
}

.carousel-container:hover .manual-control {
  opacity: 1;
}

.manual-control.carousel-control-prev {
  left: 0;
}

.manual-control.carousel-control-next {
  right: 0;
}

.manual-control .carousel-control-prev-icon,
.manual-control .carousel-control-next-icon {
  width: 20px;
  height: 20px;
  background-size: 20px 20px;
}

.manual-indicators {
  position: absolute;
  bottom: 15px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  gap: 8px;
  z-index: 5;
  padding: 0;
  margin: 0;
}

.manual-indicators button {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.5);
  border: 2px solid rgba(255, 255, 255, 0.8);
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
}

.manual-indicators button:hover {
  background-color: rgba(255, 255, 255, 0.7);
}

.manual-indicators button.active {
  background-color: white;
  border-color: white;
  transform: scale(1.2);
}

/* Image Counter */
.image-counter {
  position: absolute;
  bottom: 20px;
  right: 20px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  z-index: 10;
  backdrop-filter: blur(10px);
}

/* Badges */
.compatibility-badge {
  position: absolute;
  top: 20px;
  left: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
  z-index: 10;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

/* Status Badge - Move to bottom right */
.status-badge {
  position: absolute;
  bottom: 20px; /* Changed from top to bottom */
  right: 20px;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
  z-index: 10;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.status-badge.available {
  background: linear-gradient(135deg, #4ecdc4, #6ee7e7);
  color: white;
}

.status-badge.adopted {
  background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
  color: white;
}

/* Image Source Badges - Keep at top right */
.api-badge {
  position: absolute;
  top: 20px;
  right: 20px;
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

/* Pet Basic Info */
.pet-basic-info {
  text-align: center;
  padding: 1rem 0;
}

.pet-name {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #2c3e50, #3498db);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.pet-meta {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.pet-breed {
  font-size: 1.2rem;
  color: #6c757d;
  font-weight: 500;
}

.pet-type-badge {
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  color: #1976d2;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: capitalize;
}

.quick-stats {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin: 1.5rem 0;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.stat-item i {
  font-size: 1.5rem;
  color: #4ecdc4;
}

.stat-item span {
  font-size: 0.9rem;
  color: #6c757d;
  font-weight: 500;
}

/* Favorite Button */
.favorite-section {
  margin: 1.5rem 0;
}

.favourite-btn {
  border: none;
  border-radius: 25px;
  padding: 12px 24px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-favorite {
  background: linear-gradient(135deg, #6c757d, #adb5bd);
  color: white;
}

.btn-favorited {
  background: linear-gradient(135deg, #dc3545, #e35d6a);
  color: white;
}

.favourite-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

/* Adopt Button */
.btn-adopt {
  background: linear-gradient(135deg, #28a745, #20c997);
  border: none;
  border-radius: 15px;
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-adopt:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(40, 167, 69, 0.3);
  background: linear-gradient(135deg, #218838, #1e9c7a);
}

.adopted-message {
  padding: 2rem 1rem;
}

/* Section Titles */
.section-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 3px solid #4ecdc4;
}

.section-title-sm {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 1rem;
}

/* Personality & Background */
.section-personality,
.section-background {
  margin-bottom: 2rem;
}

.personality-content,
.background-content {
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  padding: 1.5rem;
  border-radius: 15px;
  border-left: 4px solid #4ecdc4;
  font-size: 1.05rem;
  line-height: 1.6;
}

.background-content {
  border-left-color: #ffc107;
}

/* Compatibility Section */
.compatibility-section {
  text-align: center;
}

.compatibility-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.compatibility-label {
  font-weight: 500;
  color: #6c757d;
}

.compatibility-score {
  font-size: 1.5rem;
  font-weight: 700;
  color: #4ecdc4;
}

.compatibility-progress {
  height: 10px;
  border-radius: 10px;
  background: #e9ecef;
  overflow: hidden;
}

.compatibility-progress .progress-bar {
  border-radius: 10px;
  transition: width 1s ease-in-out;
}

/* Details Lists */
.details-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f8f9fa;
}

.detail-label {
  font-weight: 500;
  color: #6c757d;
}

.detail-value {
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 0.9rem;
}

.status-yes {
  background: #d4edda;
  color: #155724;
}

.status-no {
  background: #f8d7da;
  color: #721c24;
}

.status-unknown {
  background: #fff3cd;
  color: #856404;
}

/* Activity Badges */
.activity-low {
  background: #6c757d;
  color: white;
}

.activity-medium {
  background: #ffc107;
  color: #212529;
}

.activity-high {
  background: #28a745;
  color: white;
}

/* Extended Info Items */
.info-item-extended {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.info-item-extended:hover {
  background: #e9ecef;
  transform: translateX(5px);
}

.info-item-extended i {
  font-size: 1.5rem;
  width: 40px;
  text-align: center;
}

.info-label {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
}

.info-value {
  font-weight: 600;
  color: #2c3e50;
}

.text-purple {
  color: #6f42c1;
}

/* HDB Card */
.hdb-card {
  border: 2px solid #28a745 !important;
}

.hdb-requirements {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.hdb-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 10px;
  border-left: 4px solid #28a745;
}

.hdb-item i {
  color: #28a745;
}

/* Responsive Design */
@media (max-width: 768px) {
  .pet-name {
    font-size: 2rem;
  }

  .quick-stats {
    gap: 1rem;
  }

  .pet-image {
    height: 300px;
  }

  .compatibility-header {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }

  .detail-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}

@media (max-width: 576px) {
  .pet-meta {
    flex-direction: column;
    gap: 0.5rem;
  }

  .quick-stats {
    flex-direction: column;
    gap: 1rem;
  }

  .pet-image {
    height: 250px;
  }
}
</style>
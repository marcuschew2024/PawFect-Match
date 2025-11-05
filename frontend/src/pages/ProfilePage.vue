<template>
  <div class="profile-page">
    <div class="container my-5">
      <div class="row">
        <div class="col-lg-3">
          <!-- Profile Sidebar -->
          <div class="profile-sidebar">
            <div class="profile-header text-center mb-4">
              <div class="profile-avatar">
                <i class="bi bi-person-circle display-1 text-primary"></i>
              </div>
              <h4>{{ user.full_name }}</h4>
              <p class="text-muted">{{ user.email }}</p>
            </div>
            
            <div class="profile-stats mb-4">
              <div class="stat-item text-center p-3">
                <div class="stat-number text-primary">{{ favoritePets.length }}</div>
                <div class="stat-label">Favorites</div>
              </div>
              <div class="stat-item text-center p-3">
                <div class="stat-number text-success">{{ adoptedPets.length }}</div>
                <div class="stat-label">Adoptions</div>
              </div>
            </div>
            
            <nav class="profile-nav">
              <ul class="nav flex-column">
                <li class="nav-item">
                  <a class="nav-link" :class="{ active: activeTab === 'favorites' }" 
                     @click="activeTab = 'favorites'">
                    <i class="bi bi-heart me-2"></i>My Favorites
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" :class="{ active: activeTab === 'adoptions' }" 
                     @click="activeTab = 'adoptions'">
                    <i class="bi bi-house-check me-2"></i>My Adoptions
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" :class="{ active: activeTab === 'quiz' }" 
                     @click="activeTab = 'quiz'">
                    <i class="bi bi-clipboard-check me-2"></i>Lifestyle Quiz
                  </a>
                </li>
              </ul>
            </nav>
          </div>
        </div>
        
        <div class="col-lg-9">
          <!-- Profile Content -->
          <div class="profile-content">
            
            <!-- Favorites Tab -->
            <div v-if="activeTab === 'favorites'" class="tab-content">
              <div class="d-flex justify-content-between align-items-center mb-4">
                <h3>My Favorite Pets</h3>
                <router-link to="/pets" class="btn btn-outline-primary">
                  <i class="bi bi-search me-2"></i>Browse More Pets
                </router-link>
              </div>
              
              <div v-if="favoritesLoading" class="text-center">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </div>
              
              <div v-else-if="favoritePets.length === 0" class="text-center py-5">
                <i class="bi bi-heart display-1 text-muted mb-3"></i>
                <h4 class="text-muted">No favorites yet</h4>
                <p class="text-muted">Start browsing pets and add some to your favorites!</p>
                <router-link to="/pets" class="btn btn-primary">
                  <i class="bi bi-search me-2"></i>Browse Pets
                </router-link>
              </div>
              
              <div v-else class="row">
                <div class="col-md-6 col-lg-4 mb-4" v-for="pet in favoritePets" :key="pet.id">
                  <div class="card h-100 pet-card">
                    <div class="position-relative">
                      <img :src="pet.displayImage" 
                           :alt="pet.name"
                           class="card-img-top"
                           :class="{ 'image-loaded': pet.imageLoaded }"
                           @load="onImageLoad(pet)"
                           @error="onImageError(pet)"
                           loading="lazy">
                      
                      <!-- Compatibility Badge -->
                      <div v-if="pet.compatibility_score" class="compatibility-badge">
                        {{ pet.compatibility_score }}% Match
                      </div>

                      <!-- Favorite Button -->
                      <!-- <button class="favorite-btn favorited" @click="removeFavorite(pet)">
                        <i class="bi bi-heart-fill"></i>
                      </button> -->

                      <!-- Image Source Badge -->
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
                      
                      <!-- Compatibility Meter -->
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
                        <button class="btn view-more-btn" @click="viewPetDetails(pet)">View More</button>
                        <button class="btn btn-outline-danger btn-sm" @click="removeFavorite(pet)">
                          <i class="bi bi-heart-fill me-1"></i>Remove Favorite
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Adoptions Tab -->
            <div v-if="activeTab === 'adoptions'" class="tab-content">
              <div class="d-flex justify-content-between align-items-center mb-4">
                <h3>My Adoptions</h3>
              </div>
              
              <div v-if="adoptionsLoading" class="text-center">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </div>
              
              <div v-else-if="adoptedPets.length === 0" 
                   class="text-center py-5">
                <i class="bi bi-house-check display-1 text-muted mb-3"></i>
                <h4 class="text-muted">No adoptions yet</h4>
                <p class="text-muted">Start browsing pets and submit adoption applications!</p>
                <router-link to="/pets" class="btn btn-primary">
                  <i class="bi bi-search me-2"></i>Browse Pets
                </router-link>
              </div>
              
              <div v-else class="row">
                <div class="col-md-6 col-lg-4 mb-4" v-for="pet in adoptedPets" :key="pet.id">
                  <div class="card h-100 pet-card">
                    <div class="position-relative">
                      <img :src="pet.displayImage" 
                           :alt="pet.name"
                           class="card-img-top"
                           :class="{ 'image-loaded': pet.imageLoaded }"
                           @load="onImageLoad(pet)"
                           @error="onImageError(pet)"
                           loading="lazy">
                      
                      <!-- Image Source Badge -->
                      <div v-if="pet.imageSource === 'api' && pet.imageLoaded" class="api-badge">
                        AI Generated Image
                      </div>
                      <div v-else-if="pet.imageSource === 'database' && pet.imageLoaded" class="api-badge database-badge">
                        Real Image
                      </div>

                      <div v-if="!pet.imageLoaded" class="image-loading">
                        <i class="bi bi-arrow-repeat spinner"></i>
                      </div>
                      
                      <!-- Adopted Badge -->
                      <div class="adoption-badge">
                        <i class="bi bi-check-circle me-1"></i>Adopted
                      </div>
                    </div>
                    
                    <div class="card-body d-flex flex-column">
                      <h5 class="card-title">{{ pet.name }}</h5>
                      
                      <p class="card-text mb-2 flex-grow-1">
                        <strong>Age:</strong> {{ pet.age }}<br>
                        <strong>Breed:</strong> {{ pet.breed }}<br>
                        <strong>Size:</strong> {{ pet.size }}<br>
                        <strong>Gender:</strong> {{ pet.gender }}<br>
                        <strong>Adopted:</strong> {{ formatDate(pet.adoption_date) }}
                      </p>
                      <p class="card-text personality">"{{ pet.personality }}"</p>
                    </div>
                    
                    <div class="card-footer bg-transparent">
                      <div class="d-grid">
                        <button class="btn view-more-btn" @click="viewPetDetails(pet)">View Details</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Quiz Tab -->
            <div v-if="activeTab === 'quiz'" class="tab-content">
              <div class="d-flex justify-content-between align-items-center mb-4">
                <h3>Lifestyle Quiz</h3>
                <button class="btn btn-primary" @click="updateQuiz">
                  <i class="bi bi-arrow-repeat me-2"></i>
                  {{ userQuiz ? 'Update Quiz' : 'Take Quiz' }}
                </button>
              </div>
              
              <div v-if="quizLoading" class="text-center">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </div>
              
              <div v-else class="quiz-section">
                <div v-if="userQuiz" class="current-quiz-results mb-4">
                  <div class="alert alert-success">
                    <h5><i class="bi bi-check-circle me-2"></i>Quiz Completed</h5>
                    <p class="mb-0">Your current preferences are saved. You can update them anytime.</p>
                  </div>
                  
                  <div class="quiz-summary p-4 bg-light rounded">
                    <h6 class="mb-3">Current Preferences</h6>
                    <div class="row">
                      <div class="col-md-6">
                        <p><strong>Home Type:</strong> {{ formatQuizValue(userQuiz.living_space) }}</p>
                        <p><strong>Activity Level:</strong> {{ formatQuizValue(userQuiz.activity_level) }}</p>
                        <p><strong>Pet Type:</strong> {{ formatQuizValue(userQuiz.preferred_pet_type) }}</p>
                        <p><strong>Experience:</strong> {{ formatQuizValue(userQuiz.experience_level) }}</p>
                      </div>
                      <div class="col-md-6">
                        <p><strong>Home Environment:</strong> {{ formatQuizValue(userQuiz.home_environment) }}</p>
                        <p><strong>Time Commitment:</strong> {{ formatQuizValue(userQuiz.time_commitment) }}</p>
                        <p><strong>Allergies:</strong> {{ userQuiz.has_allergies ? 'Yes' : 'No' }}</p>
                        <p><strong>Children:</strong> {{ userQuiz.has_children ? 'Yes' : 'No' }}</p>
                        <p><strong>Other Pets:</strong> {{ userQuiz.has_other_pets ? 'Yes' : 'No' }}</p>
                      </div>
                    </div>
                    <div v-if="userQuiz.allergies" class="row mt-2">
                      <div class="col-12">
                        <p><strong>Allergy Details:</strong> {{ userQuiz.allergies }}</p>
                      </div>
                    </div>
                    <div v-if="userQuiz.children_ages" class="row mt-2">
                      <div class="col-12">
                        <p><strong>Children Ages:</strong> {{ userQuiz.children_ages }}</p>
                      </div>
                    </div>
                    <div v-if="userQuiz.other_pets_details" class="row mt-2">
                      <div class="col-12">
                        <p><strong>Other Pets:</strong> {{ userQuiz.other_pets_details }}</p>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div v-else class="text-center py-5">
                  <i class="bi bi-clipboard-check display-1 text-muted mb-3"></i>
                  <h4 class="text-muted">No Quiz Completed</h4>
                  <p class="text-muted">Complete the lifestyle quiz to get better pet recommendations!</p>
                  <button class="btn btn-primary" @click="updateQuiz">
                    <i class="bi bi-clipboard-check me-2"></i>Take Lifestyle Quiz
                  </button>
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
  name: 'ProfilePage',
  data() {
    return {
      activeTab: 'favorites',
      user: {},
      favoritePets: [],
      favoritesLoading: false,
      adoptedPets: [],
      adoptionsLoading: false,
      userQuiz: null,
      quizLoading: false,
      imageCache: new Map(),
      allDogBreeds: [],
      allCatBreeds: []
    }
  },
  async mounted() {
    await this.loadUserProfile();
    await this.loadAllBreeds();
    
    // Load both favorites and adoptions immediately
    await Promise.all([
      this.loadFavorites(),
      this.loadAdoptions()
    ]);
    
    this.activeTab = this.$route.query.tab || 'favorites';
    
    // Only load quiz results if the active tab is quiz
    if (this.activeTab === 'quiz') {
      await this.loadQuizResults();
    }
    
    // Store reference for external access
    window.profilePage = this;
  },
  watch: {
    activeTab(newTab) {
      if (newTab === 'quiz') {
        this.loadQuizResults();
      }
    }
  },
  methods: {
    async loadUserProfile() {
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/user/profile`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          const profileData = await response.json();
          this.user = profileData.user || {};
        }
      } catch (error) {
        console.error('Error loading user profile:', error);
      }
    },

    async loadFavorites() {
      this.favoritesLoading = true;
      try {
        const token = localStorage.getItem('authToken');
        
        // Get favorite IDs
        const favoritesResponse = await fetch(`${API_BASE_URL}/user/favorites`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (favoritesResponse.ok) {
          const favoriteIds = await favoritesResponse.json();
          console.log('Favorite IDs:', favoriteIds);
          
          if (favoriteIds.length === 0) {
            this.favoritePets = [];
            return;
          }

          // Get ALL pets first (including adopted ones) to ensure we get all favorites
          const petsResponse = await fetch(`${API_BASE_URL}/pets`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });

          if (petsResponse.ok) {
            let allPets = await petsResponse.json();
            console.log('All pets from API:', allPets);
            
            // Filter to only favorited pets
            let favoritedPets = allPets.filter(pet => favoriteIds.includes(pet.id));
            console.log('Raw favorited pets:', favoritedPets);
            
            // Process images using the same method as PetListingPage
            this.favoritePets = await this.processPetsWithImages(favoritedPets);
            console.log('Processed favorited pets with images:', this.favoritePets);
          }
        }
      } catch (error) {
        console.error('Error loading favorites:', error);
      } finally {
        this.favoritesLoading = false;
      }
    },

    async loadAdoptions() {
      this.adoptionsLoading = true;
      try {
        const token = localStorage.getItem('authToken');
        console.log('Loading adoptions...');
        
        // Try both endpoints
        const endpoints = [
          `${API_BASE_URL}/user/adoptions`,
          `${API_BASE_URL}/user/my-adoptions`
        ];
        
        let adoptionsData = [];
        
        for (const endpoint of endpoints) {
          try {
            console.log(`Trying endpoint: ${endpoint}`);
            const response = await fetch(endpoint, {
              headers: {
                'Authorization': `Bearer ${token}`
              }
            });
            
            if (response.ok) {
              adoptionsData = await response.json();
              console.log(`✅ Success from ${endpoint}:`, adoptionsData);
              break; // Use the first successful endpoint
            } else {
              console.log(`❌ ${endpoint} failed:`, response.status);
            }
          } catch (error) {
            console.log(`❌ ${endpoint} error:`, error);
          }
        }

        if (adoptionsData && adoptionsData.length > 0) {
          console.log('Processing adoptions data:', adoptionsData);
          
          // Extract pets from adoption records - handle different formats
          const processedAdoptions = await Promise.all(adoptionsData.map(async (adoption) => {
            // Handle different response formats
            const petData = adoption.pet || adoption.pets || adoption;
            const adoptionDate = adoption.adopted_at || adoption.adoption_date;
            
            console.log('Processing adoption:', adoption, 'Pet data:', petData);
            
            // Process the pet image using the same method as PetListingPage
            const processedPet = await this.processSinglePetWithImages(petData);
            
            return {
              ...processedPet,
              adoption_date: adoptionDate
            };
          }));
          
          this.adoptedPets = processedAdoptions;
          console.log('Final adopted pets:', this.adoptedPets);
        } else {
          this.adoptedPets = [];
          console.log('No adoptions data received');
        }
      } catch (error) {
        console.error('Error loading adoptions:', error);
        this.adoptedPets = [];
      } finally {
        this.adoptionsLoading = false;
      }
    },

    // Image processing methods - EXACTLY like PetListingPage
    async processPetsWithImages(pets) {
      const processedPets = pets.map(pet => {
        let displayImage = null;
        let imageSource = 'placeholder';
        
        // Use the exact same logic as PetListingPage
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

      // Fetch API images for pets that need them (same as PetListingPage)
      this.fetchApiImagesForPets(processedPets);
      return processedPets;
    },

    async processSinglePetWithImages(pet) {
      let displayImage = null;
      let imageSource = 'placeholder';
      
      // Use the exact same logic as PetListingPage
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

      // Fetch API image if needed
      if (processedPet.placeholderImage && processedPet.imageSource === 'placeholder') {
        await this.fetchApiImageForSinglePet(processedPet);
      }

      return processedPet;
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

              // Update the arrays to trigger reactivity
              this.favoritePets = [...this.favoritePets];
              this.adoptedPets = [...this.adoptedPets];
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

    async fetchApiImageForSinglePet(pet) {
      try {
        const apiImage = await this.fetchPetImage(pet);
        if (apiImage) {
          pet.displayImage = apiImage;
          pet.image = apiImage;
          pet.placeholderImage = false;
          pet.imageSource = 'api';

          // Update the arrays to trigger reactivity
          this.favoritePets = [...this.favoritePets];
          this.adoptedPets = [...this.adoptedPets];
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

    getActivityClass(activity) {
      switch (activity) {
        case 'low': return 'bg-secondary';
        case 'medium': return 'bg-warning';
        case 'high': return 'bg-success';
        default: return 'bg-info';
      }
    },

    // Method to refresh all data
    async refreshProfileData() {
      await this.loadFavorites();
      await this.loadAdoptions();
    },

    async debugAdoptions() {
      console.log('=== DEBUG ADOPTIONS ===');
      console.log('Current adoptedPets:', this.adoptedPets);
      console.log('Adopted pets length:', this.adoptedPets.length);
      
      const token = localStorage.getItem('authToken');
      if (!token) {
        console.log('No auth token found');
        return;
      }
      
      // Test all endpoints
      const endpoints = [
        `${API_BASE_URL}/user/adoptions`,
        `${API_BASE_URL}/user/my-adoptions`,
        `${API_BASE_URL}/user/profile`
      ];
      
      for (const endpoint of endpoints) {
        try {
          const response = await fetch(endpoint, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          const data = await response.json();
          console.log(`${endpoint}:`, response.status, data);
        } catch (error) {
          console.log(`${endpoint} error:`, error);
        }
      }
    },

    async loadQuizResults() {
      this.quizLoading = true;
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/user/quiz`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          const quizData = await response.json();
          console.log('Quiz API response:', quizData); // Debug log
          
          if (quizData.has_completed_quiz && quizData.profile) {
            this.userQuiz = quizData.profile;
          } else {
            this.userQuiz = null;
          }
        } else {
          this.userQuiz = null;
        }
      } catch (error) {
        console.error('Error loading quiz results:', error);
        this.userQuiz = null;
      } finally {
        this.quizLoading = false;
      }
    },

    async removeFavorite(pet) {
      try {
        const token = localStorage.getItem('authToken');
        
        // Remove from favorites
        await fetch(`${API_BASE_URL}/user/favorites/${pet.id}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        // Remove from local array - this automatically updates the count
        this.favoritePets = this.favoritePets.filter(p => p.id !== pet.id);
        
      } catch (error) {
        console.error('Error removing favorite:', error);
        alert('Error removing favorite. Please try again.');
      }
    },

    viewPetDetails(pet) {
      this.$router.push(`/pet/${pet.id}`);
    },

    updateQuiz() {
      this.$router.push('/quiz');
    },

    formatDate(dateString) {
      if (!dateString) return 'Unknown date';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },

    formatQuizValue(value) {
      if (!value) return 'Not specified';
      
      const formatMap = {
        // Living Space
        'apartment': 'Apartment/Condo',
        'house': 'House with Yard',
        'farm': 'Farm/Rural Area',
        
        // Activity Level
        'low': 'Low Activity',
        'medium': 'Moderate Activity',
        'high': 'High Activity',
        
        // Pet Type
        'dog': 'Dogs Only',
        'cat': 'Cats Only',
        'both': 'Open to Both',
        
        // Experience Level
        'first_time': 'First-time Owner',
        'some_experience': 'Some Experience',
        'experienced': 'Experienced Owner',
        
        // Home Environment
        'quiet': 'Quiet & Calm',
        'active': 'Moderately Active',
        'very_active': 'Very Active',
        
        // Time Commitment
        'low': '0-4 Hours Alone',
        'medium': '4-8 Hours Alone',
        'high': '8+ Hours Alone'
      };
      
      return formatMap[value] || value.toString().charAt(0).toUpperCase() + value.slice(1);
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
    }
  }
}
</script>

<style scoped>
.profile-sidebar {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(255, 182, 193, 0.15);
  border: 1px solid var(--border-light);
  position: sticky;
  top: 2rem;
}

.profile-header {
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-light);
}

.profile-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-light);
}

.stat-item {
  background: var(--background-light);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.stat-item:hover {
  background: var(--primary-pink-light);
  transform: translateY(-2px);
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-light);
  font-weight: 500;
}

.profile-nav .nav-link {
  color: var(--text-light);
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
  background: none;
  text-align: left;
  width: 100%;
}

.profile-nav .nav-link:hover,
.profile-nav .nav-link.active {
  background: var(--primary-pink);
  color: var(--text-dark);
  font-weight: 600;
}

.profile-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(255, 182, 193, 0.15);
  border: 1px solid var(--border-light);
  min-height: 500px;
}

.pet-card {
  border: 1px solid var(--border-light);
  border-radius: 12px;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-medium);
  overflow: hidden;
  position: relative;
}

.pet-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-heavy);
  border-color: var(--primary-pink);
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
  color: #dc3545;
}

.favorite-btn:hover {
  background: white;
  transform: scale(1.1);
}

.adoption-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  background: rgba(40, 167, 69, 0.95);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  z-index: 3;
  backdrop-filter: blur(10px);
}

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

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.card-img-top {
  height: 200px;
  object-fit: cover;
  transition: opacity 0.3s ease;
}

.card-img-top:not(.image-loaded) {
  opacity: 0;
}

.card-img-top.image-loaded {
  opacity: 1;
}

.compatibility-meter {
  background: var(--background-light);
  padding: 0.75rem;
  border-radius: 8px;
  border-left: 3px solid var(--primary-pink);
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

.quiz-summary {
  border-left: 4px solid var(--primary-pink);
}

.tab-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (max-width: 768px) {
  .profile-sidebar {
    position: static;
    margin-bottom: 2rem;
  }
  
  .profile-stats {
    grid-template-columns: 1fr;
  }
}
</style>
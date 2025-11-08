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

            <!-- Stats: Favorites + Adoptions -->
            <div class="profile-stats mb-4 d-flex">
              <div class="stat-item text-center p-3 flex-fill">
                <div class="stat-number text-primary">{{ favoritePets.length }}</div>
                <div class="stat-label">Favorites</div>
              </div>

              <div class="stat-item text-center p-3 flex-fill">
                <div class="stat-number text-success">{{ adoptedPets.length }}</div>
                <div class="stat-label">Adoptions</div>
              </div>
            </div>

            <nav class="profile-nav">
              <ul class="nav flex-column">
                <li class="nav-item">
                  <a class="nav-link" :class="{ active: activeTab === 'favorites' }" @click="goToTab('favorites')">
                    <i class="bi bi-heart me-2"></i>My Favorites
                  </a>
                </li>

                <li class="nav-item">
                  <a class="nav-link" :class="{ active: activeTab === 'adoptions' }" @click="goToTab('adoptions')">
                    <i class="bi bi-house-check me-2"></i>My Adoptions
                  </a>
                </li>

                <li class="nav-item">
                  <a class="nav-link" :class="{ active: activeTab === 'applications' }"
                    @click="goToTab('applications')">
                    <i class="bi bi-file-text me-2"></i>My Applications
                  </a>
                </li>

                <li class="nav-item">
                  <a class="nav-link" :class="{ active: activeTab === 'quiz' }" @click="goToTab('quiz')">
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

              <div v-if="favoritesLoading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Loading your favorites...</p>
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
                      <img :src="pet.displayImage" :alt="pet.name" class="card-img-top"
                        :class="{ 'image-loaded': pet.imageLoaded }" @load="onImageLoad(pet)" @error="onImageError(pet)"
                        loading="lazy">

                      <!-- Image Source Badge -->
                      <div v-if="pet.imageSource === 'api' && pet.imageLoaded" class="api-badge">
                        AI Generated Image
                      </div>
                      <div v-else-if="pet.imageSource === 'database' && pet.imageLoaded"
                        class="api-badge database-badge">
                        Real Image
                      </div>

                      <!-- Favorite Button -->
                      <button class="favorite-btn favorited" @click="removeFavorite(pet)">
                        <i class="bi bi-heart-fill"></i>
                      </button>

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
                        <strong>Gender:</strong> {{ pet.gender }}<br>
                      </p>
                      <p class="card-text personality">"{{ pet.personality }}"</p>
                    </div>

                    <div class="card-footer bg-transparent">
                      <div class="d-grid gap-2">
                        <button class="btn view-more-btn" @click="viewPetDetails(pet)">
                          <i class="bi bi-eye me-1"></i>View More
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

              <div v-if="adoptionsLoading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Loading your adoptions...</p>
              </div>

              <div v-else-if="adoptedPets.length === 0" class="text-center py-5">
                <i class="bi bi-house-check display-1 text-muted mb-3"></i>
                <h4 class="text-muted">No adoptions yet</h4>
                <p class="text-muted">Your approved adoptions will appear here.</p>
                <router-link to="/pets" class="btn btn-primary">
                  <i class="bi bi-search me-2"></i>Browse Pets
                </router-link>
              </div>

              <div v-else class="row">
                <div class="col-md-6 col-lg-4 mb-4" v-for="adoption in adoptedPets" :key="adoption.id">
                  <div class="card h-100 pet-card">
                    <div class="position-relative">
                      <img :src="getPetImage(adoption)" :alt="getPetName(adoption)" class="card-img-top"
                        :class="{ 'image-loaded': getPetImageLoaded(adoption) }" @load="onAdoptionImageLoad(adoption)"
                        @error="onAdoptionImageError(adoption)" loading="lazy">

                      <div class="adoption-badge">
                        <i class="bi bi-check-circle me-1"></i>Adopted
                      </div>

                      <div v-if="!getPetImageLoaded(adoption)" class="image-loading">
                        <i class="bi bi-arrow-repeat spinner"></i>
                      </div>
                    </div>

                    <div class="card-body d-flex flex-column">
                      <h5 class="card-title">{{ getPetName(adoption) }}</h5>
                      <p class="card-text mb-2 flex-grow-1">
                        <strong>Age:</strong> {{ getPetAge(adoption) }}<br>
                        <strong>Breed:</strong> {{ getPetBreed(adoption) }}<br>
                        <strong>Size:</strong> {{ getPetSize(adoption) }}<br>
                        <strong>Adopted:</strong> {{ formatDate(adoption.adopted_at || adoption.adoption_date) }}<br>
                      </p>
                      <p class="card-text personality">"{{ getPetPersonality(adoption) }}"</p>
                    </div>

                    <div class="card-footer bg-transparent">
                      <div class="d-grid">
                        <button class="btn view-more-btn" @click="viewAdoption(adoption)">
                          View Details
                        </button>
                      </div>
                    </div>

                  </div>
                </div>
              </div>
            </div>

            <!-- Applications Tab -->
            <div v-if="activeTab === 'applications'" class="tab-content">
              <div class="d-flex justify-content-between align-items-center mb-4">
                <h3>My Applications</h3>
              </div>

              <div v-if="applicationsLoading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Loading your applications...</p>
              </div>

              <div v-else-if="allApplications.length === 0" class="text-center py-5">
                <i class="bi bi-file-text display-1 text-muted mb-3"></i>
                <h4 class="text-muted">No applications yet</h4>
                <p class="text-muted">Your adoption applications will appear here.</p>
                <router-link to="/pets" class="btn btn-primary">
                  <i class="bi bi-search me-2"></i>Browse Pets
                </router-link>
              </div>

              <div v-else>
                <!-- Pending Applications Section -->
                <div v-if="pendingApplications.length > 0" class="mb-5">
                  <h4 class="section-header">
                    <i class="bi bi-clock-history text-warning me-2"></i>
                    Pending Applications ({{ pendingApplications.length }})
                  </h4>
                  <div class="row">
                    <div class="col-12 mb-4" v-for="application in pendingApplications" :key="application.id">
                      <div class="card application-card pending-application">
                        <div class="card-body">
                          <div class="row align-items-center">
                            <div class="col-md-3">
                              <div class="position-relative">
                                <img :src="getPetImage(application)" :alt="getPetName(application)"
                                  class="img-fluid rounded" style="height: 120px; width: 100%; object-fit: cover;"
                                  :class="{ 'image-loaded': getPetImageLoaded(application) }"
                                  @load="onApplicationImageLoad(application)"
                                  @error="onApplicationImageError(application)">
                              </div>
                            </div>
                            <div class="col-md-6">
                              <h5>{{ getPetName(application) }}</h5>
                              <p class="mb-1"><strong>Breed:</strong> {{ getPetBreed(application) }}</p>
                              <p class="mb-1"><strong>Age:</strong> {{ getPetAge(application) }}</p>
                              <p class="mb-1"><strong>Applied:</strong> {{ formatDate(application.applied_at) }}</p>
                              <p class="mb-0"><strong>Status:</strong>
                                <span class="badge bg-warning">Pending Review</span>
                              </p>
                            </div>
                            <div class="col-md-3 text-end">
                              <button class="btn btn-outline-primary" @click="viewApplication(application)">
                                View Pet
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Rejected Applications Section -->
                <div v-if="rejectedApplications.length > 0">
                  <h4 class="section-header">
                    <i class="bi bi-x-circle text-danger me-2"></i>
                    Rejected Applications ({{ rejectedApplications.length }})
                  </h4>
                  <div class="row">
                    <div class="col-12 mb-4" v-for="application in rejectedApplications" :key="application.id">
                      <div class="card application-card rejected-application">
                        <div class="card-body">
                          <div class="row">
                            <div class="col-md-3">
                              <div class="position-relative">
                                <img :src="getPetImage(application)" :alt="getPetName(application)"
                                  class="img-fluid rounded" style="height: 120px; width: 100%; object-fit: cover;"
                                  :class="{ 'image-loaded': getPetImageLoaded(application) }"
                                  @load="onApplicationImageLoad(application)"
                                  @error="onApplicationImageError(application)">
                              </div>
                            </div>
                            <div class="col-md-6">
                              <h5>{{ getPetName(application) }}</h5>
                              <p class="mb-1"><strong>Breed:</strong> {{ getPetBreed(application) }}</p>
                              <p class="mb-1"><strong>Age:</strong> {{ getPetAge(application) }}</p>
                              <p class="mb-1"><strong>Applied:</strong> {{ formatDate(application.applied_at) }}</p>
                              <p class="mb-1"><strong>Rejected:</strong> {{ formatDate(application.rejected_at) }}</p>
                              <p class="mb-2"><strong>Status:</strong>
                                <span class="badge bg-danger">Rejected</span>
                              </p>

                              <div v-if="application.rejection_reason" class="alert alert-danger mb-0">
                                <strong><i class="bi bi-exclamation-triangle me-2"></i>Rejection Reason:</strong>
                                <p class="mb-0 mt-2">{{ application.rejection_reason }}</p>
                              </div>
                            </div>
                            <div class="col-md-3 text-end">
                              <button class="btn btn-outline-primary mb-2" @click="viewApplication(application)">
                                View Pet
                              </button>
                            </div>
                          </div>
                        </div>
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

              <div v-if="quizLoading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Loading quiz results...</p>
              </div>

              <div v-else class="quiz-section">
                <div v-if="userQuiz" class="quiz-results">
                  <div class="alert alert-info">
                    <i class="bi bi-info-circle me-2"></i>
                    You've completed the lifestyle quiz! Your preferences are being used to find compatible pets.
                  </div>

                  <div class="row">
                    <div class="col-md-6">
                      <h5>Your Preferences</h5>
                      <ul class="list-group">
                        <li class="list-group-item">
                          <strong>Living Space:</strong> {{ formatQuizValue(userQuiz.living_space) }}
                        </li>
                        <li class="list-group-item">
                          <strong>Activity Level:</strong> {{ formatQuizValue(userQuiz.activity_level) }}
                        </li>
                        <li class="list-group-item">
                          <strong>Preferred Pet:</strong> {{ formatQuizValue(userQuiz.preferred_pet_type) }}
                        </li>
                        <li class="list-group-item">
                          <strong>Experience:</strong> {{ formatQuizValue(userQuiz.experience_level) }}
                        </li>
                      </ul>
                    </div>
                    <div class="col-md-6">
                      <h5>Additional Details</h5>
                      <ul class="list-group">
                        <li class="list-group-item">
                          <strong>Home Environment:</strong> {{ formatQuizValue(userQuiz.home_environment) }}
                        </li>
                        <li class="list-group-item">
                          <strong>Time Commitment:</strong> {{ formatQuizValue(userQuiz.time_commitment) }}
                        </li>
                        <li class="list-group-item" v-if="userQuiz.has_children">
                          <strong>Children:</strong> {{ userQuiz.children_ages || 'Yes' }}
                        </li>
                        <li class="list-group-item" v-if="userQuiz.has_other_pets">
                          <strong>Other Pets:</strong> {{ userQuiz.other_pets_details || 'Yes' }}
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>

                <div v-else class="text-center py-5">
                  <i class="bi bi-clipboard-check display-1 text-muted mb-3"></i>
                  <h4 class="text-muted">No Quiz Results</h4>
                  <p class="text-muted">Complete the lifestyle quiz to get personalized pet recommendations.</p>
                  <button class="btn btn-primary" @click="updateQuiz">
                    <i class="bi bi-clipboard-check me-2"></i>Take Lifestyle Quiz
                  </button>
                </div>
              </div>
            </div>
            <!-- /Quiz Tab -->

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getApiBaseUrl } from '@/utils/config';
const API_BASE_URL = getApiBaseUrl();
//const API_BASE_URL = 'http://localhost:3000/api';

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
      allApplications: [],
      applicationsLoading: false,
      userQuiz: null,
      quizLoading: false,
      imageCache: new Map(),
      allDogBreeds: [],
      allCatBreeds: []
    }
  },
  computed: {
    pendingApplications() {
      return this.allApplications.filter(app => app.status === 'pending');
    },
    rejectedApplications() {
      return this.allApplications.filter(app => app.status === 'rejected');
    }
  },
  async mounted() {
    await this.loadUserProfile();
    await this.loadAllBreeds();

    // Set active tab from URL or default to 'favorites'
    const tabFromUrl = this.$route.query.tab;
    this.activeTab = tabFromUrl || 'favorites';

    // If no tab in URL, set it to favorites and update URL
    if (!tabFromUrl) {
      this.$router.replace({ query: { ...this.$route.query, tab: 'favorites' } });
    }

    await this.loadInitialData();
  },
  watch: {
    activeTab(newTab) {
      // Keep URL in sync with active tab
      this.$router.replace({ query: { ...this.$route.query, tab: newTab } });

      // Load tab-specific data when switching tabs
      if (newTab === 'quiz') {
        this.loadQuizResults();
      } else if (newTab === 'applications') {
        this.loadAllApplications();
      }
    }
  },
  methods: {
    goToTab(tab) {
      this.activeTab = tab;
    },

    async loadInitialData() {
      // Always load favorites and adoptions
      await Promise.all([
        this.loadFavorites(),
        this.loadAdoptions()
      ]);

      // Load additional data based on active tab
      if (this.activeTab === 'quiz') {
        await this.loadQuizResults();
      } else if (this.activeTab === 'applications') {
        await this.loadAllApplications();
      }
    },

    async loadUserProfile() {
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/user/profile`, {
          headers: { 'Authorization': `Bearer ${token}` }
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
          headers: { 'Authorization': `Bearer ${token}` }
        });

        if (favoritesResponse.ok) {
          const favoriteIds = await favoritesResponse.json();

          if (!favoriteIds || favoriteIds.length === 0) {
            this.favoritePets = [];
            return;
          }

          // Get pets data for favorite IDs
          const petsResponse = await fetch(`${API_BASE_URL}/pets`, {
            headers: { 'Authorization': `Bearer ${token}` }
          });

          if (petsResponse.ok) {
            let allPets = await petsResponse.json();
            let favoritedPets = allPets.filter(pet => favoriteIds.includes(pet.id));
            this.favoritePets = await this.processPetsWithImages(favoritedPets);
          }
        }
      } catch (error) {
        console.error('Error loading favorites:', error);
        this.showToast("Error loading favorites", "error");
      } finally {
        this.favoritesLoading = false;
      }
    },

    async loadAdoptions() {
      this.adoptionsLoading = true;
      try {
        const token = localStorage.getItem('authToken');

        const endpoints = [
          `${API_BASE_URL}/profile/my-adoptions`,
          `${API_BASE_URL}/user/adoptions`,
          `${API_BASE_URL}/user/my-applications`
        ];

        let adoptionsData = [];

        for (const endpoint of endpoints) {
          try {
            const response = await fetch(endpoint, {
              headers: { 'Authorization': `Bearer ${token}` }
            });

            if (response.ok) {
              const data = await response.json();
              if (data && data.length > 0) {
                adoptionsData = data.filter(item =>
                  item.status === 'approved' || (item.pet && item.pet.is_adopted)
                );
                if (adoptionsData.length > 0) break;
              }
            }
          } catch (err) {
            console.log(`Error from ${endpoint}:`, err);
          }
        }

        if (adoptionsData.length > 0) {
          const processedAdoptions = await Promise.all(
            adoptionsData.map(async (adoption) => {
              const petData = adoption.pet || adoption;
              if (!petData || !petData.id) return null;

              const processedPet = await this.processSinglePetWithImages(petData);
              return {
                ...adoption,
                pet: processedPet,
                id: adoption.id || adoption.pet_id,
                name: processedPet.name,
                breed: processedPet.breed,
                age: processedPet.age,
                size: processedPet.size,
                personality: processedPet.personality,
                displayImage: processedPet.displayImage,
                imageLoaded: processedPet.imageLoaded,
                pet_id: processedPet.id
              };
            })
          );
          this.adoptedPets = processedAdoptions.filter(a => a !== null);
        } else {
          this.adoptedPets = [];
        }
      } catch (error) {
        console.error('Error loading adoptions:', error);
        this.showToast("Error loading adoptions", "error");
      } finally {
        this.adoptionsLoading = false;
      }
    },

    async loadAllApplications() {
      this.applicationsLoading = true;
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/profile/my-applications`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
          const applications = await response.json();

          if (applications && applications.length > 0) {
            const applicationsWithPetData = await Promise.all(
              applications.map(async (app) => {
                try {
                  const petData = app.pet || app.pets;
                  if (!petData || !petData.id) return null;

                  const processedPet = await this.processSinglePetWithImages(petData);

                  return {
                    ...app,
                    pet: processedPet,
                    name: processedPet.name,
                    breed: processedPet.breed,
                    age: processedPet.age,
                    size: processedPet.size,
                    type: processedPet.type,
                    displayImage: processedPet.displayImage,
                    imageLoaded: processedPet.imageLoaded,
                    pet_id: processedPet.id,
                    status: app.status || 'pending',
                    applied_at: app.applied_at || app.created_at || new Date().toISOString(),
                    rejected_at: app.rejected_at,
                    rejection_reason: app.rejection_reason || null
                  };
                } catch (error) {
                  console.error('Error processing application:', error);
                  return null;
                }
              })
            );

            this.allApplications = applicationsWithPetData.filter(app => app !== null);
          } else {
            this.allApplications = [];
          }
        } else {
          console.error('Failed to load applications');
          this.allApplications = [];
        }
      } catch (error) {
        console.error('Error loading applications:', error);
        this.showToast("Error loading applications", "error");
        this.allApplications = [];
      } finally {
        this.applicationsLoading = false;
      }
    },



    async loadQuizResults() {
      this.quizLoading = true;
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/user/quiz`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
          const quizData = await response.json();
          // FIX: The quiz data is in 'profile', not 'quiz'
          if (quizData.has_completed_quiz && quizData.profile) {
            this.userQuiz = quizData.profile;
            console.log('Quiz data loaded:', this.userQuiz);
          } else {
            this.userQuiz = null;
          }
        } else if (response.status === 404) {
          this.userQuiz = null;
        }
      } catch (error) {
        console.error('Error loading quiz results:', error);
        this.userQuiz = null;
      } finally {
        this.quizLoading = false;
      }
    },

    async loadAllBreeds() {
      try {
        const [dogResponse, catResponse] = await Promise.all([
          fetch(`${API_BASE_URL}/external/dog-breeds`),
          fetch(`${API_BASE_URL}/external/cat-breeds`)
        ]);

        if (dogResponse.ok) {
          this.allDogBreeds = await dogResponse.json();
        }
        if (catResponse.ok) {
          this.allCatBreeds = await catResponse.json();
        }
      } catch (error) {
        console.error('Error loading breeds:', error);
      }
    },

    // -------- Helpers for nested pet data --------
    getPetImage(item) {
      return item.pet?.displayImage || item.displayImage || this.getColoredPlaceholder(item.pet || item);
    },
    getPetName(item) {
      return item.pet?.name || item.name || 'Unknown';
    },
    getPetAge(item) {
      return item.pet?.age || item.age || 'Unknown';
    },
    getPetBreed(item) {
      return item.pet?.breed || item.breed || 'Unknown';
    },
    getPetSize(item) {
      return item.pet?.size || item.size || 'Unknown';
    },
    getPetPersonality(item) {
      return item.pet?.personality || item.personality || 'No description available';
    },
    getPetImageLoaded(item) {
      return item.pet?.imageLoaded || item.imageLoaded || false;
    },
    getPetId(item) {
      return item.pet?.id || item.pet_id || item.id;
    },

    // -------- Image processing --------
    async processPetsWithImages(pets) {
      const processedPets = pets.map(pet => {
        let displayImage = null;
        let imageSource = 'placeholder';

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
          displayImage,
          imageLoaded: false,
          placeholderImage: imageSource === 'placeholder',
          imageSource
        };
      });

      this.fetchApiImagesForPets(processedPets);
      return processedPets;
    },

    async processSinglePetWithImages(pet) {
      if (!pet) {
        return {
          displayImage: this.getColoredPlaceholder({ type: 'dog', name: 'Unknown', id: 0 }),
          imageLoaded: true,
          placeholderImage: true,
          imageSource: 'placeholder'
        };
      }

      let displayImage = null;
      let imageSource = 'placeholder';

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
        displayImage,
        imageLoaded: false,
        placeholderImage: imageSource === 'placeholder',
        imageSource
      };

      if (imageSource === 'placeholder') {
        this.fetchApiImageForSinglePet(processedPet);
      }

      return processedPet;
    },

    async fetchApiImagesForPets(pets) {
      const petsNeedingImages = pets.filter(p => p.placeholderImage && p.imageSource === 'placeholder');
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
              this.$forceUpdate();
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
      if (!pet || !pet.type || !pet.breed) {
        console.warn('Invalid pet object for image fetch:', pet);
        return "";
      }

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

        if (!response.ok) {
          console.warn(`API error for ${pet.name}: ${response.status}`);
          return "";
        }

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

    async fetchApiImageForSinglePet(pet) {
      try {
        const apiImage = await this.fetchPetImage(pet);
        if (apiImage) {
          pet.displayImage = apiImage;
          pet.image = apiImage;
          pet.placeholderImage = false;
          pet.imageSource = 'api';
          this.$forceUpdate();
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

    findBreedId(breedName, type) {
      if (!breedName || !type) return null;
      const breeds = type === "dog" ? this.allDogBreeds : this.allCatBreeds;
      if (!breeds || !breeds.length) return null;

      try {
        const normalizedBreedName = breedName.toString().toLowerCase().trim();
        if (!normalizedBreedName) return null;

        let breed = breeds.find(b =>
          b.name && b.name.toString().toLowerCase().trim() === normalizedBreedName
        );
        if (breed) return breed.id;

        breed = breeds.find(b => {
          if (!b.name) return false;
          const apiName = b.name.toString().toLowerCase().trim();
          return apiName.includes(normalizedBreedName) && normalizedBreedName.length >= 3;
        });
        if (breed) return breed.id;

        breed = breeds.find(b => {
          if (!b.name) return false;
          const apiName = b.name.toString().toLowerCase().trim();
          return normalizedBreedName.includes(apiName) && apiName.length >= 3;
        });
        if (breed) return breed.id;

        const breedWords = normalizedBreedName.split(/\s+/).filter(word => word.length >= 3);
        if (breedWords.length > 0) {
          breed = breeds.find(b => {
            if (!b.name) return false;
            const apiWords = b.name.toString().toLowerCase().trim().split(/\s+/);
            return breedWords.some(word => apiWords.includes(word));
          });
          if (breed) return breed.id;
        }

        return null;
      } catch (error) {
        console.error('Error in findBreedId:', error, { breedName, type });
        return null;
      }
    },

    // -------- Image load handlers --------
    onImageLoad(pet) {
      pet.imageLoaded = true;
      this.$forceUpdate();
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
      this.$forceUpdate();
    },

    onAdoptionImageLoad(adoption) {
      if (adoption.pet) adoption.pet.imageLoaded = true;
      else adoption.imageLoaded = true;
      this.$forceUpdate();
    },
    onAdoptionImageError(adoption) {
      if (adoption.pet) this.onImageError(adoption.pet);
      else this.onImageError(adoption);
    },

    onApplicationImageLoad(application) {
      if (application.pet) application.pet.imageLoaded = true;
      else application.imageLoaded = true;
      this.$forceUpdate();
    },
    onApplicationImageError(application) {
      if (application.pet) this.onImageError(application.pet);
      else this.onImageError(application);
    },

    // -------- Actions --------
    async removeFavorite(pet) {
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/user/favorites/${pet.id}`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
          this.favoritePets = this.favoritePets.filter(p => p.id !== pet.id);
          this.showToast("Removed from favorites", "success");
        } else {
          throw new Error('Failed to remove favorite');
        }
      } catch (error) {
        console.error('Error removing favorite:', error);
        this.showToast("Failed to remove favorite. Please try again.", "error");
      }
    },

    viewAdoption(adoption) {
      const petId = this.getPetId(adoption);
      if (petId) this.$router.push(`/pet/${petId}`);
      else {
        console.error('No pet ID found for adoption:', adoption);
        this.showToast("Could not view pet details", "error");
      }
    },
    viewApplication(application) {
      const petId = this.getPetId(application);
      if (petId) this.$router.push(`/pet/${petId}`);
      else {
        console.error('No pet ID found for application:', application);
        this.showToast("Could not view pet details", "error");
      }
    },
    viewPetDetails(pet) {
      this.$router.push(`/pet/${pet.id}`);
    },
    updateQuiz() {
      this.$router.push('/quiz');
    },

    // -------- Utils --------
    getColoredPlaceholder(pet) {
      if (!pet) pet = { type: 'dog', name: 'Unknown', id: 0 };

      const colors = {
        dog: ['#ffb6c1', '#ffd1dc', '#ffecb3', '#c8e6c9'],
        cat: ['#bbdefb', '#c5cae9', '#e1bee7', '#f8bbd0']
      };

      const typeColors = colors[pet.type] || colors.dog;
      const colorIndex = pet.id ? (typeof pet.id === 'number'
        ? pet.id
        : pet.id.toString().split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)) : 0;
      const color = typeColors[colorIndex % typeColors.length];
      const emoji = pet.type === 'dog' ? '🐕' : '🐱';

      return `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='250' viewBox='0 0 300 250'%3E%3Crect fill='${color}' width='300' height='250'/%3E%3Ctext fill='%23666' font-size='24' font-family='system-ui' x='150' y='125' text-anchor='middle' dominant-baseline='middle'%3E${emoji}%3C/text%3E%3Ctext fill='%23333' font-size='16' font-family='system-ui' x='150' y='160' text-anchor='middle'%3E${pet.name || 'Unknown'}%3C/text%3E%3C/svg%3E`;
    },

    formatDate(dateString) {
      if (!dateString) return 'Unknown date';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric', month: 'short', day: 'numeric',
        hour: '2-digit', minute: '2-digit'
      });
    },

    formatQuizValue(value) {
      if (!value) return 'Not specified';
      const formatMap = {
        'apartment': 'Apartment/Condo',
        'house': 'House with Yard',
        'farm': 'Farm/Rural Area',
        'low': 'Low',
        'medium': 'Medium',
        'high': 'High',
        'dog': 'Dogs',
        'cat': 'Cats',
        'both': 'Dogs & Cats',
        'first_time': 'First Time Owner',
        'some_experience': 'Some Experience',
        'experienced': 'Experienced Owner',
        'quiet': 'Quiet & Calm',
        'active': 'Moderately Active',
        'very_active': 'Very Active'
      };
      return formatMap[value] || value.toString().replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    },

    showToast(message, type = 'info') {
      const toast = document.createElement("div");
      toast.className = `alert alert-${type === "error" ? "danger" : "success"} alert-dismissible fade show position-fixed`;
      toast.style.cssText = "top: 20px; right: 20px; z-index: 9999; min-width: 300px;";
      toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      `;
      document.body.appendChild(toast);

      setTimeout(() => {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, 5000);
    }
  }
}
</script>

<style scoped>
:root {
  --primary-pink: #ffb6c1;
  --primary-pink-dark: #ff91a4;
  --text-dark: #2c3e50;
  --text-light: #6c757d;
  --border-light: #e9ecef;
  --background-light: #f8f9fa;
  --shadow-light: 0 2px 4px rgba(0, 0, 0, 0.05);
  --shadow-medium: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-heavy: 0 10px 20px rgba(0, 0, 0, 0.15);
}

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

/* Make stats flex-based for 2 equal items */
.profile-stats {
  display: flex;
  gap: 0.75rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-light);
}

.stat-item {
  background: var(--background-light);
  border-radius: 8px;
  transition: all 0.3s ease;
  min-width: 0;
  overflow: hidden;
  flex: 1;
  /* equal widths */
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

.stat-number {
  font-size: 1.75rem;
  font-weight: 700;
  line-height: 1.2;
}

.stat-label {
  font-size: 0.75rem;
  color: var(--text-light);
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
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
  display: flex;
  align-items: center;
  justify-content: space-between;
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

.section-header {
  padding-bottom: 0.75rem;
  border-bottom: 2px solid var(--border-light);
  margin-bottom: 1.5rem;
  font-weight: 600;
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
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
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

/* Favorite Button - bottom right */
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
  color: #dc3545;
}

.favorite-btn:hover {
  background: white;
  transform: scale(1.1);
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
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

/* Application Card */
.application-card {
  border: 1px solid var(--border-light);
  border-radius: 12px;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-light);
}

.application-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

.pending-application {
  border-left: 4px solid #ffc107;
}

.pending-application:hover {
  border-left-color: #ff9800;
}

.rejected-application {
  border-left: 4px solid #dc3545;
  background-color: #fff5f5;
}

.rejected-application:hover {
  border-left-color: #c82333;
  background-color: #ffe6e6;
}

/* Quiz Results Styles */
.quiz-results {
  background: #f8f9fa;
  border-radius: 15px;
  padding: 2rem;
}

.list-group-item {
  border: none;
  border-bottom: 1px solid #dee2e6;
  padding: 1rem 1.25rem;
}

.list-group-item:last-child {
  border-bottom: none;
}

@media (max-width: 768px) {
  .profile-sidebar {
    position: static;
    margin-bottom: 2rem;
  }

  .profile-stats {
    gap: 0.5rem;
  }

  .stat-item {
    padding: 0.75rem 0.5rem !important;
  }

  .stat-number {
    font-size: 1.5rem;
  }

  .stat-label {
    font-size: 0.7rem;
  }
}

@media (max-width: 480px) {
  .profile-stats {
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .stat-item {
    flex: 1 1 calc(50% - 0.75rem);
  }
}
</style>
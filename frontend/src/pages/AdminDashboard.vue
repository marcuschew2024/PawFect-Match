<template>
  <div class="admin-dashboard">
    <div class="container my-5">
      <div class="row">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h1 class="mb-0">Admin Dashboard</h1>
            <button class="btn btn-outline-secondary" @click="refreshData">
              <i class="bi bi-arrow-clockwise me-2"></i>Refresh
            </button>
          </div>

          <!-- Stats Overview -->
          <div class="row mb-5">
            <div class="col-md-3 mb-3">
              <div class="card stat-card">
                <div class="card-body text-center">
                  <i class="bi bi-list-check display-4 text-primary mb-3"></i>
                  <h3>{{ stats.pendingListings }}</h3>
                  <p class="text-muted mb-0">Pending Listings</p>
                </div>
              </div>
            </div>
            <div class="col-md-3 mb-3">
              <div class="card stat-card">
                <div class="card-body text-center">
                  <i class="bi bi-heart display-4 text-warning mb-3"></i>
                  <h3>{{ stats.pendingAdoptions }}</h3>
                  <p class="text-muted mb-0">Pending Adoptions</p>
                </div>
              </div>
            </div>
            <div class="col-md-3 mb-3">
              <div class="card stat-card">
                <div class="card-body text-center">
                  <i class="bi bi-house-check display-4 text-success mb-3"></i>
                  <h3>{{ stats.approvedListings }}</h3>
                  <p class="text-muted mb-0">Approved Listings</p>
                </div>
              </div>
            </div>
            <div class="col-md-3 mb-3">
              <div class="card stat-card">
                <div class="card-body text-center">
                  <i class="bi bi-people display-4 text-info mb-3"></i>
                  <h3>{{ stats.totalAdoptions }}</h3>
                  <p class="text-muted mb-0">Total Adoptions</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Tabs -->
          <div class="card">
            <div class="card-header">
              <ul class="nav nav-tabs card-header-tabs">
                <li class="nav-item">
                  <a class="nav-link" :class="{ active: activeTab === 'listings' }" @click="activeTab = 'listings'">
                    <i class="bi bi-list-check me-2"></i>
                    Pending Listings ({{ pendingListings.length }})
                  </a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" :class="{ active: activeTab === 'adoptions' }" @click="activeTab = 'adoptions'">
                    <i class="bi bi-heart me-2"></i>
                    Pending Adoptions ({{ pendingAdoptions.length }})
                  </a>
                </li>
              </ul>
            </div>

            <div class="card-body">
              <!-- Pending Listings Tab -->
              <div v-if="activeTab === 'listings'" class="tab-content">
                <div v-if="loadingListings" class="text-center py-4">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                  <p class="mt-2">Loading pending listings...</p>
                </div>

                <div v-else-if="pendingListings.length === 0" class="text-center py-5">
                  <i class="bi bi-check-circle display-1 text-success mb-3"></i>
                  <h4 class="text-success">All Clear!</h4>
                  <p class="text-muted">No pending pet listings to review.</p>
                </div>

                <div v-else class="row">
                  <div class="col-12" v-for="pet in pendingListings" :key="pet.id">
                    <div class="card listing-card mb-4">
                      <div class="card-body">
                        <div class="row">
                          <div class="col-md-3">
                            <div class="position-relative">
                              <img :src="pet.displayImage" :alt="pet.name" class="img-fluid rounded"
                                style="height: 150px; width: 100%; object-fit: cover;"
                                :class="{ 'image-loaded': pet.imageLoaded }" @load="onImageLoad(pet)"
                                @error="onImageError(pet)" loading="lazy">

                              <!-- Image Source Badge -->
                              <div v-if="pet.imageSource === 'api' && pet.imageLoaded" class="api-badge">
                                AI Generated Image
                              </div>
                              <div v-else-if="pet.imageSource === 'database' && pet.imageLoaded"
                                class="api-badge database-badge">
                                Real Image
                              </div>
                              <div v-else-if="pet.imageSource === 'placeholder' && pet.imageLoaded"
                                class="api-badge placeholder-badge">
                                Placeholder
                              </div>

                              <div v-if="!pet.imageLoaded" class="image-loading">
                                <i class="bi bi-arrow-repeat spinner"></i>
                                <small class="d-block mt-1">Loading image...</small>
                              </div>
                            </div>
                          </div>
                          <div class="col-md-6">
                            <h5>{{ pet.name }}</h5>
                            <div class="pet-details">
                              <p class="mb-1"><strong>Type:</strong> {{ pet.type }}</p>
                              <p class="mb-1"><strong>Breed:</strong> {{ pet.breed }}</p>
                              <p class="mb-1"><strong>Age:</strong> {{ pet.age }}</p>
                              <p class="mb-1"><strong>Size:</strong> {{ pet.size }}</p>
                              <p class="mb-1"><strong>Personality:</strong> {{ pet.personality }}</p>
                              <p class="mb-1" v-if="pet.users"><strong>Listed by:</strong> {{ pet.users.full_name }}</p>
                              <p class="mb-0"><strong>Submitted:</strong> {{ formatDate(pet.created_at) }}</p>
                            </div>
                          </div>
                          <div class="col-md-3">
                            <div class="d-grid gap-2">
                              <button class="btn btn-success" @click="approveListing(pet.id)">
                                <i class="bi bi-check-lg me-2"></i>Approve
                              </button>
                              <button class="btn btn-danger" @click="showListingRejectionModal(pet)">
                                <i class="bi bi-x-lg me-2"></i>Reject
                              </button>
                              <button class="btn btn-outline-primary" @click="viewPetDetails(pet)">
                                <i class="bi bi-eye me-2"></i>View Details
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Pending Adoptions Tab -->
              <div v-if="activeTab === 'adoptions'" class="tab-content">
                <div v-if="loadingAdoptions" class="text-center py-4">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                  <p class="mt-2">Loading pending adoptions...</p>
                </div>

                <div v-else-if="pendingAdoptions.length === 0" class="text-center py-5">
                  <i class="bi bi-check-circle display-1 text-success mb-3"></i>
                  <h4 class="text-success">All Clear!</h4>
                  <p class="text-muted">No pending adoption applications to review.</p>
                </div>

                <div v-else class="row">
                  <div class="col-12" v-for="application in pendingAdoptions" :key="application.id">
                    <div class="card adoption-card mb-4">
                      <div class="card-body">
                        <div class="row">
                          <div class="col-md-3">
                            <div class="position-relative">
                              <img :src="application.petDisplayImage" :alt="application.pets?.name"
                                class="img-fluid rounded" style="height: 150px; width: 100%; object-fit: cover;"
                                :class="{ 'image-loaded': application.petImageLoaded }"
                                @load="onApplicationImageLoad(application)"
                                @error="onApplicationImageError(application)" loading="lazy">

                              <!-- Image Source Badge -->
                              <div v-if="application.petImageSource === 'api' && application.petImageLoaded"
                                class="api-badge">
                                AI Generated Image
                              </div>
                              <div v-else-if="application.petImageSource === 'database' && application.petImageLoaded"
                                class="api-badge database-badge">
                                Real Image
                              </div>
                              <div
                                v-else-if="application.petImageSource === 'placeholder' && application.petImageLoaded"
                                class="api-badge placeholder-badge">
                                Placeholder
                              </div>

                              <div v-if="!application.petImageLoaded" class="image-loading">
                                <i class="bi bi-arrow-repeat spinner"></i>
                                <small class="d-block mt-1">Loading image...</small>
                              </div>
                            </div>
                            <div class="text-center mt-2">
                              <strong>{{ application.pets?.name }}</strong>
                            </div>
                          </div>
                          <div class="col-md-6">
                            <h5>Adoption Application</h5>
                            <div class="application-details">
                              <p class="mb-1"><strong>Applicant:</strong> {{ application.applicant_name }}</p>
                              <p class="mb-1"><strong>Email:</strong> {{ application.applicant_email }}</p>
                              <p class="mb-1"><strong>Phone:</strong> {{ application.applicant_phone }}</p>
                              <p class="mb-1"><strong>Applied:</strong> {{ formatDate(application.applied_at) }}</p>
                              <div class="mt-3">
                                <h6>Application Details:</h6>
                                <p class="mb-1"><strong>Living Situation:</strong> {{ application.living_situation }}
                                </p>
                                <p class="mb-1"><strong>Pet Experience:</strong> {{ application.experience_with_pets }}
                                </p>
                                <p class="mb-0"><strong>Adoption Reason:</strong> {{ application.reason_for_adoption }}
                                </p>
                              </div>
                            </div>
                          </div>
                          <div class="col-md-3">
                            <div class="d-grid gap-2">
                              <button class="btn btn-success" @click="approveAdoption(application.id)">
                                <i class="bi bi-check-lg me-2"></i>Approve
                              </button>
                              <button class="btn btn-danger" @click="showRejectionModal(application)">
                                <i class="bi bi-x-lg me-2"></i>Reject
                              </button>
                              <button class="btn btn-outline-primary" @click="viewApplicationDetails(application)">
                                <i class="bi bi-eye me-2"></i>View Full
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
          </div>
        </div>
      </div>
    </div>

    <!-- Pet Listing Rejection Modal -->
    <div v-if="showListingModal" class="modal-backdrop fade show"></div>
    <div v-if="showListingModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-x-circle-fill text-danger me-2"></i>
              Confirm Listing Rejection
            </h5>
            <button type="button" class="btn-close" @click="hideListingRejectionModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="alert alert-warning mb-3">
              <i class="bi bi-exclamation-triangle-fill me-2"></i>
              <strong>Are you sure you want to reject this pet listing?</strong>
            </div>

            <div class="application-preview mb-3 p-3 border rounded bg-light" v-if="currentRejectionPet">
              <p class="mb-1"><strong>Pet:</strong> {{ currentRejectionPet.name }}</p>
              <p class="mb-1"><strong>Type:</strong> {{ currentRejectionPet.type }}</p>
              <p class="mb-1"><strong>Breed:</strong> {{ currentRejectionPet.breed }}</p>
              <p class="mb-0"><strong>Submitted:</strong> {{ currentRejectionPet ?
                formatDate(currentRejectionPet.created_at) : '' }}</p>
            </div>

            <div class="mb-3">
              <label class="form-label">
                <strong>Reason for rejection (optional):</strong>
              </label>
              <textarea class="form-control" v-model="listingRejectionReason" rows="4"
                placeholder="Enter rejection reason..." maxlength="500"></textarea>
              <div class="form-text text-end">
                {{ listingRejectionReason.length }}/500 characters
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="hideListingRejectionModal">
              <i class="bi bi-arrow-left me-2"></i>Cancel
            </button>
            <button type="button" class="btn btn-danger" @click="confirmRejectListing"
              :disabled="processingListingRejection">
              <i class="bi bi-x-lg me-2"></i>
              <span v-if="processingListingRejection">
                <span class="spinner-border spinner-border-sm me-2"></span>
                Processing...
              </span>
              <span v-else>Confirm Rejection</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Adoption Application Rejection Modal -->
    <div v-if="showAdoptionModal" class="modal-backdrop fade show"></div>
    <div v-if="showAdoptionModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-x-circle-fill text-danger me-2"></i>
              Confirm Rejection
            </h5>
            <button type="button" class="btn-close" @click="hideRejectionModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="alert alert-warning mb-3">
              <i class="bi bi-exclamation-triangle-fill me-2"></i>
              <strong>Are you sure you want to reject this adoption application?</strong>
            </div>

            <div class="application-preview mb-3 p-3 border rounded bg-light">
              <p class="mb-1"><strong>Applicant:</strong> {{ currentRejectionApplication?.applicant_name }}</p>
              <p class="mb-1"><strong>Pet:</strong> {{ currentRejectionApplication?.pets?.name }}</p>
              <p class="mb-0"><strong>Applied:</strong> {{ currentRejectionApplication ?
                formatDate(currentRejectionApplication.applied_at) : '' }}</p>
            </div>

            <div class="mb-3">
              <label class="form-label">
                <strong>Reason for rejection (optional):</strong>
              </label>
              <textarea class="form-control" v-model="rejectionReason" rows="4"
                placeholder="Enter rejection reason (this will be helpful for the applicant)..."
                maxlength="500"></textarea>
              <div class="form-text text-end">
                {{ rejectionReason.length }}/500 characters
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="hideRejectionModal">
              <i class="bi bi-arrow-left me-2"></i>Cancel
            </button>
            <button type="button" class="btn btn-danger" @click="confirmRejectAdoption" :disabled="processingRejection">
              <i class="bi bi-x-lg me-2"></i>
              <span v-if="processingRejection">
                <span class="spinner-border spinner-border-sm me-2"></span>
                Processing...
              </span>
              <span v-else>Confirm Rejection</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Application Details Modal -->
    <div v-if="showApplicationDetailsModal" class="modal-backdrop fade show"></div>
    <div v-if="showApplicationDetailsModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-file-text me-2"></i>
              Adoption Application Details
            </h5>
            <button type="button" class="btn-close" @click="hideApplicationDetailsModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div v-if="currentApplicationDetails" class="application-full-details">
              <!-- Pet Information -->
              <div class="section mb-4">
                <h6 class="section-title bg-light p-2 rounded">
                  <i class="bi bi-heart-fill text-danger me-2"></i>Pet Information
                </h6>
                <div class="row">
                  <!-- In the Application Details Modal - update the image section -->
                  <div class="col-md-4 text-center">
                    <div class="position-relative">
                      <img :src="currentApplicationDetails.petDisplayImage" :alt="currentApplicationDetails.pets?.name"
                        class="img-fluid rounded mb-2" style="max-height: 200px; object-fit: cover; width: 100%;"
                        :class="{ 'image-loaded': currentApplicationDetails.petImageLoaded }"
                        @load="onModalImageLoad(currentApplicationDetails)"
                        @error="onModalImageError(currentApplicationDetails)" loading="lazy">

                      <!-- Image Source Badge for Modal -->
                      <div
                        v-if="currentApplicationDetails.petImageSource === 'api' && currentApplicationDetails.petImageLoaded"
                        class="api-badge">
                        AI Generated Image
                      </div>
                      <div
                        v-else-if="currentApplicationDetails.petImageSource === 'database' && currentApplicationDetails.petImageLoaded"
                        class="api-badge database-badge">
                        Real Image
                      </div>
                      <div
                        v-else-if="currentApplicationDetails.petImageSource === 'placeholder' && currentApplicationDetails.petImageLoaded"
                        class="api-badge placeholder-badge">
                        Placeholder
                      </div>

                      <div v-if="!currentApplicationDetails.petImageLoaded" class="image-loading">
                        <i class="bi bi-arrow-repeat spinner"></i>
                        <small class="d-block mt-1">Loading image...</small>
                      </div>
                    </div>
                    <h5 class="mt-2">{{ currentApplicationDetails.pets?.name }}</h5>
                    <p class="text-muted mb-0">{{ currentApplicationDetails.pets?.type }} • {{
                      currentApplicationDetails.pets?.breed }}</p>
                  </div>
                  <div class="col-md-8">
                    <div class="row">
                      <div class="col-6">
                        <p><strong>Age:</strong> {{ currentApplicationDetails.pets?.age }}</p>
                        <p><strong>Size:</strong> {{ currentApplicationDetails.pets?.size }}</p>
                        <p><strong>Gender:</strong> {{ currentApplicationDetails.pets?.gender || 'Not specified' }}</p>
                      </div>
                      <div class="col-6">
  <p><strong>Personality:</strong> {{ currentApplicationDetails.pets?.personality }}</p>
  <p><strong>Health Status:</strong> {{ currentApplicationDetails.pets?.health_status || 'Not specified' }}</p>
  <p><strong>Location:</strong> {{ currentApplicationDetails.pets?.location || 'Not specified' }}</p>
</div>
                    </div>
                    <div v-if="currentApplicationDetails.pets?.description" class="mt-2">
                      <p><strong>Description:</strong></p>
                      <p class="text-muted">{{ currentApplicationDetails.pets?.description }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Applicant Information -->
              <div class="section mb-4">
                <h6 class="section-title bg-light p-2 rounded">
                  <i class="bi bi-person-fill text-primary me-2"></i>Applicant Information
                </h6>
                <div class="row">
                  <div class="col-md-6">
                    <p><strong>Full Name:</strong> {{ currentApplicationDetails.applicant_name }}</p>
                    <p><strong>Email:</strong> {{ currentApplicationDetails.applicant_email }}</p>
                    <p><strong>Phone:</strong> {{ currentApplicationDetails.applicant_phone }}</p>
                  </div>
                  <div class="col-md-6">
                    <p><strong>Application Date:</strong> {{ formatDate(currentApplicationDetails.applied_at) }}</p>
                    <p><strong>Application ID:</strong> #{{ currentApplicationDetails.id }}</p>
                    <p><strong>Status:</strong> <span class="badge bg-warning">Pending Review</span></p>
                  </div>
                </div>
              </div>

              <!-- Application Details -->
              <div class="section mb-4">
                <h6 class="section-title bg-light p-2 rounded">
                  <i class="bi bi-house-fill text-success me-2"></i>Living Situation & Experience
                </h6>
                <div class="row">
                  <div class="col-12">
                    <p><strong>Living Situation:</strong></p>
                    <p class="text-muted mb-3">{{ currentApplicationDetails.living_situation }}</p>

                    <p><strong>Experience with Pets:</strong></p>
                    <p class="text-muted mb-3">{{ currentApplicationDetails.experience_with_pets }}</p>

                    <p><strong>Reason for Adoption:</strong></p>
                    <p class="text-muted">{{ currentApplicationDetails.reason_for_adoption }}</p>
                  </div>
                </div>
              </div>

              <!-- Additional Information -->
              <div class="section" v-if="currentApplicationDetails.additional_notes">
                <h6 class="section-title bg-light p-2 rounded">
                  <i class="bi bi-chat-text-fill text-info me-2"></i>Additional Notes
                </h6>
                <p class="text-muted">{{ currentApplicationDetails.additional_notes }}</p>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="hideApplicationDetailsModal">
              <i class="bi bi-x me-2"></i>Close
            </button>
            <button type="button" class="btn btn-success" @click="approveAdoption(currentApplicationDetails?.id)">
              <i class="bi bi-check-lg me-2"></i>Approve Application
            </button>
            <button type="button" class="btn btn-danger" @click="showRejectionModal(currentApplicationDetails)">
              <i class="bi bi-x-lg me-2"></i>Reject Application
            </button>
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
  name: 'AdminDashboard',
  data() {
    return {
      activeTab: 'listings',
      pendingListings: [],
      pendingAdoptions: [],
      loadingListings: false,
      loadingAdoptions: false,
      stats: {
        pendingListings: 0,
        pendingAdoptions: 0,
        approvedListings: 0,
        totalAdoptions: 0
      },
      rejectionReason: '',
      listingRejectionReason: '',
      currentRejectionApplication: null,
      currentRejectionPet: null,
      processingRejection: false,
      processingListingRejection: false,
      // Modal visibility states
      showListingModal: false,
      showAdoptionModal: false,
      showApplicationDetailsModal: false,
      currentApplicationDetails: null,
      imageCache: new Map(),
      allDogBreeds: [],
      allCatBreeds: [],
      apiFetchInProgress: new Set() // Track API calls in progress
    }
  },
  async mounted() {
    await this.loadAllBreeds();
    await this.loadAllData();
  },
  methods: {
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

    async loadAllData() {
      await Promise.all([
        this.loadPendingListings(),
        this.loadPendingAdoptions(),
        this.loadStats()
      ]);
    },

    async loadPendingListings() {
      this.loadingListings = true;
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/admin/pending-listings`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          const listings = await response.json();
          this.pendingListings = await this.processPetsWithImages(listings);
        } else {
          console.error('Failed to load pending listings');
          this.pendingListings = [];
        }
      } catch (error) {
        console.error('Error loading pending listings:', error);
        this.pendingListings = [];
      } finally {
        this.loadingListings = false;
      }
    },

    async loadPendingAdoptions() {
      this.loadingAdoptions = true;
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/admin/pending-adoptions`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          const adoptions = await response.json();
          this.pendingAdoptions = await this.processApplicationsWithImages(adoptions);
        } else {
          console.error('Failed to load pending adoptions');
          this.pendingAdoptions = [];
        }
      } catch (error) {
        console.error('Error loading pending adoptions:', error);
        this.pendingAdoptions = [];
      } finally {
        this.loadingAdoptions = false;
      }
    },

    async loadStats() {
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/admin/stats`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          this.stats = await response.json();
        } else {
          console.error('Failed to load stats');
          this.stats.pendingListings = this.pendingListings.length;
          this.stats.pendingAdoptions = this.pendingAdoptions.length;
        }
      } catch (error) {
        console.error('Error loading stats:', error);
        this.stats.pendingListings = this.pendingListings.length;
        this.stats.pendingAdoptions = this.pendingAdoptions.length;
      }
    },

    // Image processing methods
    async processPetsWithImages(pets) {
      const processedPets = await Promise.all(
        pets.map(async (pet) => {
          let displayImage = null;
          let imageSource = 'placeholder';

          // First, check if there are images in the database (same logic as PetProfile)
          if (pet.images && Array.isArray(pet.images) && pet.images.length > 0) {
            const validImages = pet.images.map(img => {
              if (typeof img === 'object' && img.image_url) {
                return img.image_url;
              } else if (typeof img === 'string') {
                return img;
              }
              return null;
            }).filter(url => url !== null && url.trim() !== '');

            if (validImages.length > 0) {
              displayImage = validImages[0];
              imageSource = 'database';
            }
          }

          if (!displayImage && pet.main_image && pet.main_image.trim() !== '') {
            displayImage = pet.main_image;
            imageSource = 'database';
          } else if (!displayImage && pet.image && pet.image.trim() !== '') {
            displayImage = pet.image;
            imageSource = 'database';
          }

          if (!displayImage) {
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

          // If it's a placeholder, try to fetch API image (same as PetProfile)
          if (imageSource === 'placeholder') {
            this.fetchApiImageForPet(processedPet);
          }

          return processedPet;
        })
      );

      return processedPets;
    },

    async processApplicationsWithImages(applications) {
      const processedApplications = await Promise.all(
        applications.map(async (app) => {
          const pet = app.pets;
          let displayImage = null;
          let imageSource = 'placeholder';

          if (pet) {
            // Use the same image processing logic as for pets
            if (pet.images && Array.isArray(pet.images) && pet.images.length > 0) {
              const validImages = pet.images.map(img => {
                if (typeof img === 'object' && img.image_url) {
                  return img.image_url;
                } else if (typeof img === 'string') {
                  return img;
                }
                return null;
              }).filter(url => url !== null && url.trim() !== '');

              if (validImages.length > 0) {
                displayImage = validImages[0];
                imageSource = 'database';
              }
            }

            if (!displayImage && pet.main_image && pet.main_image.trim() !== '') {
              displayImage = pet.main_image;
              imageSource = 'database';
            } else if (!displayImage && pet.image && pet.image.trim() !== '') {
              displayImage = pet.image;
              imageSource = 'database';
            }

            if (!displayImage) {
              displayImage = this.getColoredPlaceholder(pet);
              imageSource = 'placeholder';
            }
          } else {
            displayImage = this.getColoredPlaceholder({ type: 'dog', name: 'Unknown', id: Math.random() });
            imageSource = 'placeholder';
          }

          const processedApp = {
            ...app,
            petDisplayImage: displayImage,
            petImageLoaded: false,
            petPlaceholderImage: imageSource === 'placeholder',
            petImageSource: imageSource
          };

          // If it's a placeholder and we have a pet, try to fetch API image
          if (imageSource === 'placeholder' && pet) {
            this.fetchApiImageForApplication(processedApp, pet);
          }

          return processedApp;
        })
      );

      return processedApplications;
    },

    // Fetch API image for pet (same logic as PetProfile)
    async fetchApiImageForPet(pet) {
      if (!pet || this.apiFetchInProgress.has(pet.id)) {
        return;
      }

      this.apiFetchInProgress.add(pet.id);

      try {
        console.log(`🔄 Fetching API image for ${pet.name}`);
        const apiImage = await this.fetchPetImage(pet);
        if (apiImage) {
          console.log('✅ API image fetched successfully');

          // Update the pet object
          pet.displayImage = apiImage;
          pet.image = apiImage;
          pet.placeholderImage = false;
          pet.imageSource = 'api';

          console.log('🔄 Updated pet with API image');
          this.$forceUpdate();
        } else {
          console.log('❌ No API image available, keeping colored placeholder');
        }
      } catch (error) {
        console.error(`Error fetching API image for ${pet.name}:`, error);
      } finally {
        this.apiFetchInProgress.delete(pet.id);
      }
    },

    // Fetch API image for application
    async fetchApiImageForApplication(application, pet) {
      if (!pet || this.apiFetchInProgress.has(`app-${application.id}`)) {
        return;
      }

      this.apiFetchInProgress.add(`app-${application.id}`);

      try {
        console.log(`🔄 Fetching API image for ${pet.name} in application`);
        const apiImage = await this.fetchPetImage(pet);
        if (apiImage) {
          console.log('✅ API image fetched successfully for application');

          // Update the application object
          application.petDisplayImage = apiImage;
          application.petPlaceholderImage = false;
          application.petImageSource = 'api';

          console.log('🔄 Updated application with API image');
          this.$forceUpdate();
        } else {
          console.log('❌ No API image available for application, keeping colored placeholder');
        }
      } catch (error) {
        console.error(`Error fetching API image for ${pet.name} in application:`, error);
      } finally {
        this.apiFetchInProgress.delete(`app-${application.id}`);
      }
    },

    // Use the same fetchPetImage method as PetProfile
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

        console.log(`📡 Fetching API image from: ${apiUrl}?${params}`);
        const response = await fetch(`${apiUrl}?${params}`, { headers });

        if (!response.ok) {
          console.error(`API error: ${response.status} - ${response.statusText}`);
          throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();
        console.log('📡 API response:', data);

        if (data && data.length > 0 && data[0].url) {
          const imageUrl = data[0].url;
          console.log('✅ Found API image:', imageUrl);
          this.imageCache.set(cacheKey, imageUrl);
          return imageUrl;
        } else {
          console.log('❌ No images found in API response');
          return "";
        }
      } catch (error) {
        console.error(`Error fetching image for ${pet.name}:`, error);
        return "";
      }
    },

    // Breed ID finding method (same as PetProfile)
    findBreedId(breedName, type) {
      const breeds = type === "dog" ? this.allDogBreeds : this.allCatBreeds;

      if (!breeds || !breeds.length) {
        return null;
      }

      try {
        const normalizedBreedName = breedName.toString().toLowerCase().trim();

        // If breed name is empty after normalization, return null
        if (!normalizedBreedName) {
          return null;
        }

        // Exact match
        let breed = breeds.find(b =>
          b.name && b.name.toString().toLowerCase().trim() === normalizedBreedName
        );

        if (breed) {
          return breed.id;
        }

        // Partial match - breed name contains search term
        breed = breeds.find(b => {
          if (!b.name) return false;
          const apiName = b.name.toString().toLowerCase().trim();
          return apiName.includes(normalizedBreedName) && normalizedBreedName.length >= 3;
        });

        if (breed) {
          return breed.id;
        }

        // Partial match - search term contains breed name
        breed = breeds.find(b => {
          if (!b.name) return false;
          const apiName = b.name.toString().toLowerCase().trim();
          return normalizedBreedName.includes(apiName) && apiName.length >= 3;
        });

        if (breed) {
          return breed.id;
        }

        // Word-based matching
        const breedWords = normalizedBreedName.split(/\s+/).filter(word => word.length >= 3);
        if (breedWords.length > 0) {
          breed = breeds.find(b => {
            if (!b.name) return false;
            const apiWords = b.name.toString().toLowerCase().trim().split(/\s+/);
            return breedWords.some(word => apiWords.includes(word));
          });

          if (breed) {
            return breed.id;
          }
        }

        console.log(`No breed match found for: ${breedName} (${type})`);
        return null;
      } catch (error) {
        console.error('Error in findBreedId:', error, { breedName, type });
        return null;
      }
    },

    // Image load/error handlers
    onImageLoad(pet) {
      pet.imageLoaded = true;
      this.$forceUpdate();
    },

    onImageError(pet) {
      console.log(`❌ Image failed to load for ${pet.name}`);

      // If database image fails, try to use API
      if (pet.imageSource === 'database') {
        console.log(`🔄 Database image failed, trying API for ${pet.name}`);
        pet.placeholderImage = true;
        pet.imageSource = 'placeholder';
        this.fetchApiImageForPet(pet);
      } else if (pet.imageSource === 'api') {
        console.log(`🔄 API image failed, using placeholder for ${pet.name}`);
        pet.displayImage = this.getColoredPlaceholder(pet);
        pet.imageSource = 'placeholder';
        pet.placeholderImage = true;
      } else {
        pet.displayImage = this.getColoredPlaceholder(pet);
        pet.imageSource = 'placeholder';
        pet.placeholderImage = true;
      }

      pet.imageLoaded = true;
      this.$forceUpdate();
    },

    onApplicationImageLoad(application) {
      application.petImageLoaded = true;
      this.$forceUpdate();
    },

    onApplicationImageError(application) {
      console.log(`❌ Application image failed to load`);

      // If database image fails, try to use API
      if (application.petImageSource === 'database') {
        console.log(`🔄 Database image failed, trying API for application`);
        application.petPlaceholderImage = true;
        application.petImageSource = 'placeholder';
        if (application.pets) {
          this.fetchApiImageForApplication(application, application.pets);
        }
      } else if (application.petImageSource === 'api') {
        console.log(`🔄 API image failed, using placeholder for application`);
        if (application.pets) {
          application.petDisplayImage = this.getColoredPlaceholder(application.pets);
        }
        application.petImageSource = 'placeholder';
        application.petPlaceholderImage = true;
      } else {
        if (application.pets) {
          application.petDisplayImage = this.getColoredPlaceholder(application.pets);
        }
        application.petImageSource = 'placeholder';
        application.petPlaceholderImage = true;
      }

      application.petImageLoaded = true;
      this.$forceUpdate();
    },
    // Add these methods for modal image handling
    onModalImageLoad(application) {
      application.petImageLoaded = true;
      this.$forceUpdate();
    },

    onModalImageError(application) {
      console.log(`❌ Modal image failed to load for ${application.pets?.name}`);

      // Use the same fallback logic as the main application images
      if (application.petImageSource === 'database') {
        console.log(`🔄 Database image failed in modal, trying API`);
        application.petPlaceholderImage = true;
        application.petImageSource = 'placeholder';
        this.fetchApiImageForApplication(application, application.pets);
      } else if (application.petImageSource === 'api') {
        console.log(`🔄 API image failed in modal, using placeholder`);
        if (application.pets) {
          application.petDisplayImage = this.getColoredPlaceholder(application.pets);
        }
        application.petImageSource = 'placeholder';
        application.petPlaceholderImage = true;
      } else {
        if (application.pets) {
          application.petDisplayImage = this.getColoredPlaceholder(application.pets);
        }
        application.petImageSource = 'placeholder';
        application.petPlaceholderImage = true;
      }

      application.petImageLoaded = true;
      this.$forceUpdate();
    },
    getColoredPlaceholder(pet) {
      const colors = {
        dog: ['#ffb6c1', '#ffd1dc', '#ffecb3', '#c8e6c9'],
        cat: ['#bbdefb', '#c5cae9', '#e1bee7', '#f8bbd0']
      };
      const typeColors = colors[pet.type] || colors.dog;
      const colorIndex = pet.id ? (typeof pet.id === 'number' ? pet.id : pet.id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)) : 0;
      const color = typeColors[colorIndex % typeColors.length];
      const emoji = pet.type === 'dog' ? '🐕' : '🐱';

      return `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='250' viewBox='0 0 300 250'%3E%3Crect fill='${color}' width='300' height='250'/%3E%3Ctext fill='%23666' font-size='24' font-family='system-ui' x='150' y='125' text-anchor='middle' dominant-baseline='middle'%3E${emoji}%3C/text%3E%3Ctext fill='%23333' font-size='16' font-family='system-ui' x='150' y='160' text-anchor='middle'%3E${pet.name || 'Unknown'}%3C/text%3E%3C/svg%3E`;
    },

    async approveListing(petId) {
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/admin/approve-listing/${petId}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          this.showToast('Pet listing approved successfully!', 'success');
          this.pendingListings = this.pendingListings.filter(pet => pet.id !== petId);
          await this.loadStats();
        } else {
          const errorData = await response.json();
          this.showToast(errorData.error || 'Failed to approve listing', 'error');
        }
      } catch (error) {
        console.error('Error approving listing:', error);
        this.showToast('Error approving listing', 'error');
      }
    },

    // Modal methods
    showListingRejectionModal(pet) {
      this.currentRejectionPet = pet;
      this.listingRejectionReason = '';
      this.processingListingRejection = false;
      this.showListingModal = true;
    },

    hideListingRejectionModal() {
      this.showListingModal = false;
      this.currentRejectionPet = null;
      this.listingRejectionReason = '';
    },

    async confirmRejectListing() {
      if (!this.currentRejectionPet) {
        this.showToast('No pet selected for rejection', 'error');
        return;
      }

      this.processingListingRejection = true;

      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/admin/reject-listing/${this.currentRejectionPet.id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            rejection_reason: this.listingRejectionReason.trim() || 'No reason provided'
          })
        });

        if (response.ok) {
          this.showToast('Pet listing rejected successfully!', 'success');
          this.pendingListings = this.pendingListings.filter(pet => pet.id !== this.currentRejectionPet.id);
          await this.loadStats();
          this.hideListingRejectionModal();
        } else {
          const errorData = await response.json();
          this.showToast(errorData.error || 'Failed to reject listing', 'error');
        }
      } catch (error) {
        console.error('Error rejecting listing:', error);
        this.showToast('Error rejecting listing', 'error');
      } finally {
        this.processingListingRejection = false;
      }
    },

    async approveAdoption(applicationId) {
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/admin/approve-adoption/${applicationId}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          this.showToast('Adoption approved successfully!', 'success');
          this.pendingAdoptions = this.pendingAdoptions.filter(app => app.id !== applicationId);
          if (this.showApplicationDetailsModal) {
            this.hideApplicationDetailsModal();
          }
          await this.loadStats();
        } else {
          const errorData = await response.json();
          this.showToast(errorData.error || 'Failed to approve adoption', 'error');
        }
      } catch (error) {
        console.error('Error approving adoption:', error);
        this.showToast('Error approving adoption', 'error');
      }
    },

    showRejectionModal(application) {
      this.currentRejectionApplication = application;
      this.rejectionReason = '';
      this.processingRejection = false;
      this.showAdoptionModal = true;
      // Close the details modal if it's open
      if (this.showApplicationDetailsModal) {
        this.hideApplicationDetailsModal();
      }
    },

    hideRejectionModal() {
      this.showAdoptionModal = false;
      this.currentRejectionApplication = null;
      this.rejectionReason = '';
    },

    async confirmRejectAdoption() {
      if (!this.currentRejectionApplication) {
        this.showToast('No application selected for rejection', 'error');
        return;
      }

      this.processingRejection = true;

      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/admin/reject-adoption/${this.currentRejectionApplication.id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            rejection_reason: this.rejectionReason.trim() || 'No reason provided'
          })
        });

        if (response.ok) {
          this.showToast('Adoption application rejected successfully!', 'success');
          this.pendingAdoptions = this.pendingAdoptions.filter(app => app.id !== this.currentRejectionApplication.id);
          await this.loadStats();
          this.hideRejectionModal();
        } else {
          const errorData = await response.json();
          this.showToast(errorData.error || 'Failed to reject adoption application', 'error');
        }
      } catch (error) {
        console.error('Error rejecting adoption:', error);
        this.showToast('Error rejecting adoption application', 'error');
      } finally {
        this.processingRejection = false;
      }
    },

    viewPetDetails(pet) {
      this.$router.push(`/pet/${pet.id}`);
    },

    viewApplicationDetails(application) {
      // Create a copy of the application to ensure reactivity
      this.currentApplicationDetails = {
        ...application,
        // Ensure image loaded state is properly set
        petImageLoaded: false
      };
      this.showApplicationDetailsModal = true;

      // Force image reload in the modal
      this.$nextTick(() => {
        if (this.currentApplicationDetails && this.currentApplicationDetails.pets) {
          // Re-process the image to ensure proper loading
          this.processApplicationImageForModal(this.currentApplicationDetails);
        }
      });
    },

    // Add this new method to handle modal image processing
    async processApplicationImageForModal(application) {
      if (!application.pets) return;

      let displayImage = application.petDisplayImage;
      let imageSource = application.petImageSource;

      // If we don't have a loaded image, try to reload it
      if (!application.petImageLoaded) {
        // Create a new image element to test loading
        const img = new Image();
        img.onload = () => {
          application.petImageLoaded = true;
          this.$forceUpdate();
        };
        img.onerror = () => {
          // If image fails to load, use placeholder and try API
          console.log('❌ Modal image failed to load, trying fallback');
          if (application.pets) {
            application.petDisplayImage = this.getColoredPlaceholder(application.pets);
            application.petImageSource = 'placeholder';
            application.petPlaceholderImage = true;
            application.petImageLoaded = true;
            this.$forceUpdate();

            // Try to fetch API image as fallback
            if (!this.apiFetchInProgress.has(`modal-app-${application.id}`)) {
              this.fetchApiImageForApplication(application, application.pets);
            }
          }
        };
        img.src = displayImage;
      }
    },

    hideApplicationDetailsModal() {
      this.showApplicationDetailsModal = false;
      this.currentApplicationDetails = null;
    },

    formatDate(dateString) {
      if (!dateString) return 'Unknown date';
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    async refreshData() {
      await this.loadAllData();
      this.showToast('Data refreshed!', 'success');
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
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  min-height: 100vh;
}

.stat-card {
  border: none;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.listing-card,
.adoption-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.listing-card:hover,
.adoption-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.nav-tabs .nav-link {
  color: #6c757d;
  font-weight: 500;
  cursor: pointer;
}

.nav-tabs .nav-link.active {
  color: #495057;
  font-weight: 600;
  border-bottom: 3px solid #007bff;
}

.pet-details,
.application-details {
  font-size: 0.9rem;
}

.btn {
  border-radius: 8px;
  font-weight: 500;
}

.api-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background-color: rgba(255, 255, 255, 0.95);
  color: #666;
  font-size: 0.7rem;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 12px;
  border: 1px solid #ddd;
  z-index: 3;
}

.database-badge {
  background-color: rgba(76, 175, 80, 0.95) !important;
  color: white !important;
}

.placeholder-badge {
  background-color: rgba(255, 193, 7, 0.95) !important;
  color: #000 !important;
}

.image-loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #666;
  font-size: 1.5rem;
  z-index: 2;
  text-align: center;
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

.img-fluid:not(.image-loaded) {
  opacity: 0;
}

.img-fluid.image-loaded {
  opacity: 1;
  transition: opacity 0.3s ease;
}

.modal-header {
  border-bottom: 1px solid #dee2e6;
}

.modal-footer {
  border-top: 1px solid #dee2e6;
}

.application-preview {
  background-color: #f8f9fa;
  border-left: 4px solid #ffc107;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

/* Modal backdrop styling */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1040;
  width: 100vw;
  height: 100vh;
  background-color: #000;
  opacity: 0.5;
}

.modal {
  z-index: 1050;
}

/* Application Details Modal Styles */
.section-title {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.section {
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 1rem;
}

.section:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.application-full-details p {
  margin-bottom: 0.5rem;
}

.badge {
  font-size: 0.75rem;
}
</style>
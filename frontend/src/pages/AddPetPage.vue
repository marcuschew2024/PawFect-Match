<template>
  <div class="add-adoption-page">
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="adoption-header text-center mb-5">
            <h1>Add a Pet for Adoption</h1>
            <p class="lead">Help a furry friend find their forever home by listing them for adoption</p>
          </div>

          <div class="adoption-card">
            <form @submit.prevent="submitPet" class="adoption-form">
              <!-- Basic Information -->
              <div class="form-section mb-4">
                <h4 class="section-title">Basic Information</h4>
                
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="petName" class="form-label">Pet Name *</label>
                    <input type="text" class="form-control" id="petName" 
                           v-model="form.name" required>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label for="petType" class="form-label">Pet Type *</label>
                    <select class="form-select" id="petType" v-model="form.type" required>
                      <option value="">Select Type</option>
                      <option value="dog">Dog</option>
                      <option value="cat">Cat</option>
                    </select>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="petBreed" class="form-label">Breed *</label>
                    <input type="text" class="form-control" id="petBreed" 
                           v-model="form.breed" required>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label for="petAge" class="form-label">Age *</label>
                    <input type="text" class="form-control" id="petAge" 
                           v-model="form.age" required placeholder="e.g., 2 years, 6 months">
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="petSize" class="form-label">Size *</label>
                    <select class="form-select" id="petSize" v-model="form.size" required>
                      <option value="">Select Size</option>
                      <option value="Small">Small</option>
                      <option value="Medium">Medium</option>
                      <option value="Large">Large</option>
                    </select>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label for="petGender" class="form-label">Gender *</label>
                    <select class="form-select" id="petGender" v-model="form.gender" required>
                      <option value="">Select Gender</option>
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- Image Upload -->
              <div class="form-section mb-4">
                <h4 class="section-title">Pet Images</h4>
                <p class="text-muted mb-3">Upload multiple images (up to 5). The first image will be used as the main photo.</p>
                
                <!-- File Upload -->
                <div class="mb-3">
                  <label for="petImages" class="form-label">Upload Images</label>
                  <input 
                    type="file" 
                    class="form-control" 
                    id="petImages" 
                    multiple 
                    accept="image/*"
                    @change="handleFileUpload"
                    ref="fileInput"
                  >
                  <div class="form-text">Select multiple images (PNG, JPG, JPEG). Maximum 5 images, 5MB each.</div>
                </div>

                <!-- URL Upload -->
                <!-- <div class="mb-3">
                  <label for="imageUrls" class="form-label">Or Add Image URLs</label>
                  <div class="input-group mb-2">
                    <input 
                      type="url" 
                      class="form-control" 
                      v-model="newImageUrl" 
                      placeholder="https://example.com/pet-image.jpg"
                    >
                    <button 
                      type="button" 
                      class="btn btn-outline-secondary" 
                      @click="addImageUrl"
                      :disabled="!newImageUrl || uploadedImages.length >= 5"
                    >
                      Add URL
                    </button>
                  </div>
                </div> -->

                <!-- Image Previews -->
                <div v-if="uploadedImages.length > 0" class="image-previews mt-4">
                  <h6>Selected Images ({{ uploadedImages.length }}/5):</h6>
                  <div class="row">
                    <div 
                      v-for="(image, index) in uploadedImages" 
                      :key="index" 
                      class="col-md-4 mb-3"
                    >
                      <div class="image-preview-card position-relative">
                        <img 
                          :src="image.preview || image.url" 
                          alt="Preview" 
                          class="img-thumbnail"
                          style="height: 150px; width: 100%; object-fit: cover;"
                        >
                        <div class="position-absolute top-0 start-0 m-1">
                          <span v-if="index === 0" class="badge bg-primary">Main</span>
                        </div>
                        <button 
                          type="button" 
                          class="btn btn-danger btn-sm position-absolute top-0 end-0 m-1"
                          @click="removeImage(index)"
                        >
                          ×
                        </button>
                        <div class="image-info small text-muted p-1 text-truncate">
                          {{ image.file ? image.file.name : 'URL Image' }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Background Story -->
              <div class="form-section mb-4">
                <h4 class="section-title">Background Story</h4>
                <div class="mb-3">
                  <label for="petBackground" class="form-label">Pet's Background Story</label>
                  <textarea class="form-control" id="petBackground" rows="4" 
                            v-model="form.background"
                            placeholder="Tell us about the pet's history, where they came from, any special circumstances..."></textarea>
                  <div class="form-text">This helps potential adopters understand the pet's journey and special needs.</div>
                </div>
              </div>

              <!-- Additional Details -->
              <div class="form-section mb-4">
                <h4 class="section-title">Additional Details</h4>
                
                <div class="mb-3">
                  <label for="petPersonality" class="form-label">Personality & Description *</label>
                  <textarea class="form-control" id="petPersonality" rows="3" 
                            v-model="form.personality" required
                            placeholder="Describe the pet's personality, temperament, and any special characteristics..."></textarea>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="petActivity" class="form-label">Activity Level</label>
                    <select class="form-select" id="petActivity" v-model="form.activity_level">
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                    </select>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label for="petColor" class="form-label">Fur Color</label>
                    <input type="text" class="form-control" id="petColor" 
                           v-model="form.fur_color" placeholder="e.g., Brown, Black, White">
                  </div>
                </div>
              </div>

              <!-- Health & Adoption Info -->
              <div class="form-section mb-4">
                <h4 class="section-title">Health & Adoption Information</h4>
                
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="vaccinationStatus" class="form-label">Vaccination Status</label>
                    <select class="form-select" id="vaccinationStatus" v-model="form.vaccination_status">
                      <option value="Up to date">Up to date</option>
                      <option value="Partially vaccinated">Partially vaccinated</option>
                      <option value="Not vaccinated">Not vaccinated</option>
                      <option value="Unknown">Unknown</option>
                    </select>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label for="adoptionFee" class="form-label">Adoption Fee ($)</label>
                    <input type="number" class="form-control" id="adoptionFee" 
                           v-model="form.adoption_fee" min="0" step="0.01" placeholder="0.00">
                  </div>
                </div>

                <div class="mb-3">
                  <label for="healthInfo" class="form-label">Health Information</label>
                  <textarea class="form-control" id="healthInfo" rows="2" 
                            v-model="form.health_info"
                            placeholder="Any health conditions, medications, or special care requirements..."></textarea>
                </div>

                <div class="mb-3">
                  <label for="petLocation" class="form-label">Location</label>
                  <input type="text" class="form-control" id="petLocation" 
                         v-model="form.location" placeholder="e.g., Singapore, Central Area">
                </div>
              </div>

              <!-- Behavior & Compatibility -->
              <div class="form-section mb-4">
                <h4 class="section-title">Behavior & Compatibility</h4>
                
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Good with Children</label>
                    <div>
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" id="goodWithChildrenYes" 
                               v-model="form.good_with_children" :value="true">
                        <label class="form-check-label" for="goodWithChildrenYes">Yes</label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" id="goodWithChildrenNo" 
                               v-model="form.good_with_children" :value="false">
                        <label class="form-check-label" for="goodWithChildrenNo">No</label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" id="goodWithChildrenUnknown" 
                               v-model="form.good_with_children" :value="null">
                        <label class="form-check-label" for="goodWithChildrenUnknown">Unknown</label>
                      </div>
                    </div>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Good with Other Pets</label>
                    <div>
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" id="goodWithPetsYes" 
                               v-model="form.good_with_other_pets" :value="true">
                        <label class="form-check-label" for="goodWithPetsYes">Yes</label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" id="goodWithPetsNo" 
                               v-model="form.good_with_other_pets" :value="false">
                        <label class="form-check-label" for="goodWithPetsNo">No</label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" id="goodWithPetsUnknown" 
                               v-model="form.good_with_other_pets" :value="null">
                        <label class="form-check-label" for="goodWithPetsUnknown">Unknown</label>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Vaccinated</label>
                    <div>
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" id="vaccinatedYes" 
                               v-model="form.vaccinated" :value="true">
                        <label class="form-check-label" for="vaccinatedYes">Yes</label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" id="vaccinatedNo" 
                               v-model="form.vaccinated" :value="false">
                        <label class="form-check-label" for="vaccinatedNo">No</label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" id="vaccinatedUnknown" 
                               v-model="form.vaccinated" :value="null">
                        <label class="form-check-label" for="vaccinatedUnknown">Unknown</label>
                      </div>
                    </div>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Neutered/Spayed</label>
                    <div>
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" id="neuteredYes" 
                               v-model="form.neutered" :value="true">
                        <label class="form-check-label" for="neuteredYes">Yes</label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" id="neuteredNo" 
                               v-model="form.neutered" :value="false">
                        <label class="form-check-label" for="neuteredNo">No</label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input class="form-check-input" type="radio" id="neuteredUnknown" 
                               v-model="form.neutered" :value="null">
                        <label class="form-check-label" for="neuteredUnknown">Unknown</label>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="mb-3">
                  <label class="form-label">HDB Approved</label>
                  <div>
                    <div class="form-check form-check-inline">
                      <input class="form-check-input" type="radio" id="hdbApprovedYes" 
                             v-model="form.hdb_approved" :value="true">
                      <label class="form-check-label" for="hdbApprovedYes">Yes</label>
                    </div>
                    <div class="form-check form-check-inline">
                      <input class="form-check-input" type="radio" id="hdbApprovedNo" 
                             v-model="form.hdb_approved" :value="false">
                      <label class="form-check-label" for="hdbApprovedNo">No</label>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Error Message -->
              <div v-if="error" class="alert alert-danger">
                <i class="bi bi-exclamation-triangle me-2"></i>
                {{ error }}
              </div>

              <!-- Success Message -->
              <div v-if="success" class="alert alert-success">
                <i class="bi bi-check-circle me-2"></i>
                {{ success }}
              </div>

              <!-- Submit Button -->
              <div class="d-grid">
                <button type="submit" class="btn btn-primary btn-lg" :disabled="loading || uploadedImages.length === 0">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ loading ? 'Adding Pet...' : `Add Pet for Adoption` }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AddAdoptionPage',
  data() {
    return {
      form: {
        name: '',
        type: '',
        breed: '',
        age: '',
        size: '',
        gender: '',
        personality: '',
        background: '',
        activity_level: 'medium',
        fur_color: '',
        vaccination_status: 'Up to date',
        adoption_fee: 0,
        health_info: '',
        location: 'Singapore',
        good_with_children: null,
        good_with_other_pets: null,
        vaccinated: null,
        neutered: null,
        hdb_approved: false
      },
      uploadedImages: [],
      newImageUrl: '',
      loading: false,
      error: null,
      success: null
    }
  },
  methods: {
    handleFileUpload(event) {
  const files = Array.from(event.target.files);
  
  console.log(`📁 Files selected: ${files.length}`);
  
  if (files.length + this.uploadedImages.length > 5) {
    this.error = 'Maximum 5 images allowed';
    return;
  }

  for (let file of files) {
    console.log(`📄 Processing file: ${file.name}, size: ${file.size}, type: ${file.type}`);
    
    if (file.size > 5 * 1024 * 1024) {
      this.error = `File ${file.name} is too large. Maximum size is 5MB.`;
      continue;
    }

    if (!file.type.startsWith('image/')) {
      this.error = `File ${file.name} is not an image.`;
      continue;
    }

    // Create preview and store file
    const reader = new FileReader();
    reader.onload = (e) => {
      console.log(`🖼️ File loaded as preview: ${file.name}`);
      this.uploadedImages.push({
        file: file,
        preview: e.target.result,
        type: 'file'
      });
      console.log(`📊 Total uploaded images: ${this.uploadedImages.length}`);
    };
    reader.readAsDataURL(file);
  }

  // Reset file input
  this.$refs.fileInput.value = '';
  this.error = null;
},

    addImageUrl() {
      if (this.newImageUrl && this.uploadedImages.length < 5) {
        // Validate URL format
        try {
          new URL(this.newImageUrl);
          this.uploadedImages.push({
            url: this.newImageUrl,
            type: 'url'
          });
          this.newImageUrl = '';
          this.error = null;
        } catch (e) {
          this.error = 'Please enter a valid URL';
        }
      } else if (this.uploadedImages.length >= 5) {
        this.error = 'Maximum 5 images allowed';
      }
    },

    removeImage(index) {
      this.uploadedImages.splice(index, 1);
    },

   async submitPet() {
  if (this.uploadedImages.length === 0) {
    this.error = 'Please add at least one image of the pet';
    return;
  }

  this.loading = true;
  this.error = null;
  this.success = null;
  
  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      this.$router.push('/login');
      return;
    }

    // Convert file images to base64 URLs
    const imageUrls = [];
    
    console.log(`🖼️ Processing ${this.uploadedImages.length} uploaded images:`);
    
    for (const image of this.uploadedImages) {
      if (image.type === 'file') {
        console.log(`📁 Converting file: ${image.file.name}`);
        // Convert file to base64
        const base64Url = await this.fileToBase64(image.file);
        imageUrls.push(base64Url);
        console.log(`✅ Converted to base64, length: ${base64Url.length}`);
      } else {
        // Use URL directly
        console.log(`🌐 Using URL: ${image.url}`);
        imageUrls.push(image.url);
      }
    }

    console.log(`🎯 Final image URLs to send: ${imageUrls.length}`);
    console.log('📤 First image preview:', imageUrls[0]?.substring(0, 100) + '...');

    // Prepare the data - map field names to match database
    const submissionData = {
      name: this.form.name,
      type: this.form.type,
      breed: this.form.breed,
      age: this.form.age,
      size: this.form.size,
      gender: this.form.gender,
      personality: this.form.personality,
      background: this.form.background,
      activity_level: this.form.activity_level,
      fur_color: this.form.fur_color,
      vaccination_status: this.form.vaccination_status,
      adoption_fee: this.form.adoption_fee,
      health_info: this.form.health_info,
      location: this.form.location,
      good_with_children: this.form.good_with_children,
      good_with_other_pets: this.form.good_with_other_pets,
      vaccinated: this.form.vaccinated,
      neutered: this.form.neutered,
      hdb_approved: this.form.hdb_approved,
      images: imageUrls
    };

    console.log('📦 Submission data prepared, sending to backend...');

    const response = await fetch('http://localhost:3000/api/pets', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(submissionData)
    });

    console.log('📨 Response status:', response.status);

    if (response.ok) {
      const newPet = await response.json();
      console.log('✅ Successfully created pet:', newPet);
      console.log('📸 New pet images:', newPet.images);
      console.log('🔢 Number of images in response:', newPet.images ? newPet.images.length : 0);
      
      this.success = `Successfully added ${newPet.name} for adoption with ${this.uploadedImages.length} images!`;
      this.resetForm();
      
      setTimeout(() => {
        this.$router.push('/pets');
      }, 2000);
    } else {
      const error = await response.json();
      console.error('❌ Server error:', error);
      this.error = error.error || `Failed to add pet for adoption (Status: ${response.status})`;
    }
  } catch (error) {
    console.error('Error adding pet:', error);
    this.error = 'Network error. Please try again.';
  } finally {
    this.loading = false;
  }
},

    fileToBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
      });
    },
    
    resetForm() {
      this.form = {
        name: '',
        type: '',
        breed: '',
        age: '',
        size: '',
        gender: '',
        personality: '',
        background: '',
        activity_level: 'medium',
        fur_color: '',
        vaccination_status: 'Up to date',
        adoption_fee: 0,
        health_info: '',
        location: 'Singapore',
        good_with_children: null,
        good_with_other_pets: null,
        vaccinated: null,
        neutered: null,
        hdb_approved: false
      };
      this.uploadedImages = [];
      this.newImageUrl = '';
    }
  }
}
</script>

<style scoped>
.add-adoption-page {
  min-height: 80vh;
}

.adoption-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(255, 182, 193, 0.15);
  border: 1px solid var(--border-light);
}

.adoption-header h1 {
  color: var(--text-dark);
  font-weight: 700;
}

.section-title {
  color: var(--primary-pink-dark);
  border-bottom: 2px solid var(--primary-pink);
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
}

.form-section {
  padding: 1.5rem;
  border: 1px solid var(--border-light);
  border-radius: 8px;
  background: var(--background-light);
}

.form-control:focus,
.form-select:focus {
  border-color: var(--primary-pink);
  box-shadow: 0 0 0 0.2rem rgba(255, 182, 193, 0.25);
}

.btn-primary {
  background: linear-gradient(135deg, #ff868a 0%, #ffa6a6 100%);
  color: white;
  border: none;
  padding: 12px 25px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 154, 158, 0.4);
  background: linear-gradient(135deg, #eb7e7e 0%, #FF9A9E 100%);
  color: white;
}

.image-preview-card {
  border: 1px solid var(--border-light);
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease;
}

.image-preview-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.image-info {
  background: rgba(0,0,0,0.05);
  font-size: 0.75rem;
}

.form-check-input:checked {
  background-color: var(--primary-pink);
  border-color: var(--primary-pink);
}
</style>
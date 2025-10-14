<template>
  <div class="quiz-page">
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="quiz-card">
            <div class="quiz-header text-center mb-5">
              <h1>Find Your Perfect Match</h1>
              <p class="lead" v-if="!hasExistingResults">Complete this quick quiz to help us match you with compatible pets</p>
              <p class="lead" v-else>Update your preferences to improve your matches</p>
              <div class="progress mb-4">
                <div class="progress-bar" :style="{ width: progress + '%' }"></div>
              </div>
            </div>

            <!-- Show current results if redoing quiz -->
            <div v-if="hasExistingResults && !completed" class="alert alert-info mb-4">
              <i class="bi bi-info-circle me-2"></i>
              You've already completed this quiz. You can update your answers below to improve your matches.
            </div>

            <form @submit.prevent="submitQuiz" v-if="!completed">
              <!-- Step 1: Basic Information -->
              <div v-if="currentStep === 1" class="quiz-step">
                <h3 class="mb-4">Your Living Situation</h3>
                
                <div class="form-group mb-4">
                  <label class="form-label">What type of home do you live in?</label>
                  <div class="btn-group-vertical w-100">
                    <button type="button" class="btn btn-outline-primary text-start" 
                            :class="{ 'active': form.living_space === 'apartment' }"
                            @click="form.living_space = 'apartment'">
                      <i class="bi bi-building me-2"></i>
                      <strong>Apartment/Condo</strong>
                      <small class="d-block text-muted">Limited space, shared walls</small>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.living_space === 'house' }"
                            @click="form.living_space = 'house'">
                      <i class="bi bi-house me-2"></i>
                      <strong>House with Yard</strong>
                      <small class="d-block text-muted">Private space with outdoor access</small>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.living_space === 'farm' }"
                            @click="form.living_space = 'farm'">
                      <i class="bi bi-tree me-2"></i>
                      <strong>Farm/Rural Area</strong>
                      <small class="d-block text-muted">Large open spaces</small>
                    </button>
                  </div>
                </div>

                <div class="form-group mb-4">
                  <label class="form-label">Do you have allergies to pets?</label>
                  <div class="btn-group w-100">
                    <button type="button" class="btn btn-outline-primary"
                            :class="{ 'active': form.has_allergies === true }"
                            @click="form.has_allergies = true">
                      Yes
                    </button>
                    <button type="button" class="btn btn-outline-primary"
                            :class="{ 'active': form.has_allergies === false }"
                            @click="form.has_allergies = false; form.allergies = ''">
                      No
                    </button>
                  </div>
                </div>

                <div v-if="form.has_allergies" class="form-group mb-4">
                  <label class="form-label">What are you allergic to?</label>
                  <input type="text" class="form-control" v-model="form.allergies" 
                         placeholder="e.g., cat dander, dog hair...">
                </div>
              </div>

              <!-- Step 2: Lifestyle & Experience -->
              <div v-if="currentStep === 2" class="quiz-step">
                <h3 class="mb-4">Your Lifestyle & Experience</h3>
                
                <div class="form-group mb-4">
                  <label class="form-label">How active is your lifestyle?</label>
                  <div class="btn-group-vertical w-100">
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.activity_level === 'low' }"
                            @click="form.activity_level = 'low'">
                      <i class="bi bi-emoji-sunglasses me-2"></i>
                      <strong>Low Activity</strong>
                      <small class="d-block text-muted">Quiet home, limited outdoor time</small>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.activity_level === 'medium' }"
                            @click="form.activity_level = 'medium'">
                      <i class="bi bi-emoji-smile me-2"></i>
                      <strong>Moderate Activity</strong>
                      <small class="d-block text-muted">Daily walks, some playtime</small>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.activity_level === 'high' }"
                            @click="form.activity_level = 'high'">
                      <i class="bi bi-emoji-laughing me-2"></i>
                      <strong>High Activity</strong>
                      <small class="d-block text-muted">Very active, lots of outdoor time</small>
                    </button>
                  </div>
                </div>

                <div class="form-group mb-4">
                  <label class="form-label">What's your experience with pets?</label>
                  <div class="btn-group-vertical w-100">
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.experience_level === 'first_time' }"
                            @click="form.experience_level = 'first_time'">
                      <strong>First-time Owner</strong>
                      <small class="d-block text-muted">New to pet ownership</small>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.experience_level === 'some_experience' }"
                            @click="form.experience_level = 'some_experience'">
                      <strong>Some Experience</strong>
                      <small class="d-block text-muted">Had pets before</small>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.experience_level === 'experienced' }"
                            @click="form.experience_level = 'experienced'">
                      <strong>Experienced Owner</strong>
                      <small class="d-block text-muted">Very comfortable with pets</small>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Step 3: Family & Preferences -->
              <div v-if="currentStep === 3" class="quiz-step">
                <h3 class="mb-4">Family & Preferences</h3>
                
                <div class="form-group mb-4">
                  <label class="form-label">Do you have children?</label>
                  <div class="btn-group w-100">
                    <button type="button" class="btn btn-outline-primary"
                            :class="{ 'active': form.has_children === true }"
                            @click="form.has_children = true">
                      Yes
                    </button>
                    <button type="button" class="btn btn-outline-primary"
                            :class="{ 'active': form.has_children === false }"
                            @click="form.has_children = false; form.children_ages = ''">
                      No
                    </button>
                  </div>
                </div>

                <div v-if="form.has_children" class="form-group mb-4">
                  <label class="form-label">Ages of children?</label>
                  <input type="text" class="form-control" v-model="form.children_ages" 
                         placeholder="e.g., 5 and 8 years old">
                </div>

                <div class="form-group mb-4">
                  <label class="form-label">Do you have other pets?</label>
                  <div class="btn-group w-100">
                    <button type="button" class="btn btn-outline-primary"
                            :class="{ 'active': form.has_other_pets === true }"
                            @click="form.has_other_pets = true">
                      Yes
                    </button>
                    <button type="button" class="btn btn-outline-primary"
                            :class="{ 'active': form.has_other_pets === false }"
                            @click="form.has_other_pets = false; form.other_pets_details = ''">
                      No
                    </button>
                  </div>
                </div>

                <div v-if="form.has_other_pets" class="form-group mb-4">
                  <label class="form-label">Tell us about your other pets</label>
                  <input type="text" class="form-control" v-model="form.other_pets_details" 
                         placeholder="e.g., 1 cat, 2 dogs...">
                </div>

                <div class="form-group mb-4">
                  <label class="form-label">What type of pet are you looking for?</label>
                  <div class="btn-group-vertical w-100">
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.preferred_pet_type === 'dog' }"
                            @click="form.preferred_pet_type = 'dog'">
                      <i class="bi bi-bootstrap me-2"></i>
                      <strong>Dogs Only</strong>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.preferred_pet_type === 'cat' }"
                            @click="form.preferred_pet_type = 'cat'">
                      <i class="bi bi-bootstrap me-2"></i>
                      <strong>Cats Only</strong>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.preferred_pet_type === 'both' }"
                            @click="form.preferred_pet_type = 'both'">
                      <i class="bi bi-bootstrap me-2"></i>
                      <strong>Open to Both</strong>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Navigation Buttons -->
              <div class="quiz-navigation mt-5">
                <div class="d-flex justify-content-between">
                  <button type="button" class="btn btn-outline-secondary" 
                          @click="previousStep" v-if="currentStep > 1">
                    <i class="bi bi-arrow-left me-2"></i>Back
                  </button>
                  <div v-else></div>

                  <button type="button" class="btn btn-primary" 
                          @click="nextStep" v-if="currentStep < totalSteps">
                    Continue <i class="bi bi-arrow-right ms-2"></i>
                  </button>

                  <button type="submit" class="btn btn-success" v-if="currentStep === totalSteps">
                    <i class="bi bi-check-circle me-2"></i>
                    {{ hasExistingResults ? 'Update Quiz' : 'Complete Quiz' }}
                  </button>
                </div>
              </div>
            </form>

            <!-- Results Page -->
            <div v-if="completed" class="quiz-completed text-center">
              <i class="bi bi-check-circle-fill text-success display-1 mb-4"></i>
              <h2 v-if="hasExistingResults">Quiz Updated!</h2>
              <h2 v-else>Quiz Completed!</h2>
              <p class="lead mb-4">Your preferences have been saved and will be used to find your perfect matches.</p>
              <div class="d-grid gap-2 d-md-block">
                <router-link to="/pets" class="btn btn-primary me-md-2">
                  <i class="bi bi-search me-2"></i>View Updated Matches
                </router-link>
                <button class="btn btn-outline-primary me-md-2" @click="redoQuiz">
                  <i class="bi bi-arrow-repeat me-2"></i>Redo Quiz Again
                </button>
                <router-link to="/" class="btn btn-outline-secondary">
                  <i class="bi bi-house me-2"></i>Back to Home
                </router-link>
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
  name: 'LifestyleQuiz',
  data() {
    return {
      currentStep: 1,
      totalSteps: 3,
      completed: false,
      loading: false,
      hasExistingResults: false,
      form: {
        living_space: '',
        activity_level: '',
        preferred_pet_type: '',
        has_allergies: false,
        allergies: '',
        experience_level: 'first_time',
        home_environment: 'quiet',
        has_children: false,
        children_ages: '',
        has_other_pets: false,
        other_pets_details: '',
        time_commitment: 'medium'
      }
    }
  },
  computed: {
    progress() {
      return (this.currentStep / this.totalSteps) * 100;
    }
  },
  async mounted() {
    // Check if user already has quiz results
    await this.loadExistingResults();
  },
  methods: {
    async loadExistingResults() {
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/user/quiz`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          const existingResults = await response.json();
          this.hasExistingResults = true;
          
          // Pre-fill the form with existing results
          this.form = {
            living_space: existingResults.living_space || '',
            activity_level: existingResults.activity_level || '',
            preferred_pet_type: existingResults.preferred_pet_type || '',
            has_allergies: existingResults.has_allergies || false,
            allergies: existingResults.allergies || '',
            experience_level: existingResults.experience_level || 'first_time',
            home_environment: existingResults.home_environment || 'quiet',
            has_children: existingResults.has_children || false,
            children_ages: existingResults.children_ages || '',
            has_other_pets: existingResults.has_other_pets || false,
            other_pets_details: existingResults.other_pets_details || '',
            time_commitment: existingResults.time_commitment || 'medium'
          };
        }
      } catch (error) {
        console.log('No existing quiz results found');
        this.hasExistingResults = false;
      }
    },

    nextStep() {
      if (this.currentStep < this.totalSteps) {
        this.currentStep++;
      }
    },

    previousStep() {
      if (this.currentStep > 1) {
        this.currentStep--;
      }
    },

    async submitQuiz() {
      this.loading = true;
      
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/user/quiz`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(this.form)
        });

        if (response.ok) {
          this.completed = true;
          this.hasExistingResults = true;
          // Emit event to update parent components
          this.$emit('quiz-completed');
        } else {
          const error = await response.json();
          alert('Error saving quiz: ' + error.error);
        }
      } catch (error) {
        console.error('Quiz submission error:', error);
        alert('Network error. Please try again.');
      } finally {
        this.loading = false;
      }
    },

    redoQuiz() {
      // Reset the quiz to start over
      this.completed = false;
      this.currentStep = 1;
      // Keep the existing form data so they can modify it
    }
  }
}
</script>

<style scoped>
.quiz-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(255, 182, 193, 0.15);
  border: 1px solid var(--border-light);
}

.quiz-header h1 {
  color: var(--text-dark);
  font-weight: 700;
}

.progress {
  height: 8px;
  background-color: var(--border-light);
}

.progress-bar {
  background-color: var(--primary-pink);
  transition: width 0.3s ease;
}

.quiz-step {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.btn-group-vertical .btn {
  margin-bottom: 0.5rem;
  padding: 1rem;
  text-align: left;
  border: 2px solid var(--border-light);
}

.btn-group-vertical .btn.active {
  background-color: var(--primary-pink);
  border-color: var(--primary-pink);
  color: var(--text-dark);
}

.quiz-completed {
  padding: 2rem 0;
}

.quiz-navigation {
  border-top: 1px solid var(--border-light);
  padding-top: 1.5rem;
}
</style>
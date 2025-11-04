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
                  <label class="form-label">Do you have a yard?</label>
                  <div class="btn-group w-100">
                    <button type="button" class="btn btn-outline-primary"
                            :class="{ 'active': form.has_yard === true }"
                            @click="form.has_yard = true">
                      Yes
                    </button>
                    <button type="button" class="btn btn-outline-primary"
                            :class="{ 'active': form.has_yard === false }"
                            @click="form.has_yard = false">
                      No
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
                            :class="{ 'active': form.pet_experience === 'none' }"
                            @click="form.pet_experience = 'none'">
                      <strong>First-time Owner</strong>
                      <small class="d-block text-muted">New to pet ownership</small>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.pet_experience === 'some_experience' }"
                            @click="form.pet_experience = 'some_experience'">
                      <strong>Some Experience</strong>
                      <small class="d-block text-muted">Had pets before</small>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.pet_experience === 'experienced' }"
                            @click="form.pet_experience = 'experienced'">
                      <strong>Experienced Owner</strong>
                      <small class="d-block text-muted">Very comfortable with pets</small>
                    </button>
                  </div>
                </div>

                <div class="form-group mb-4">
                  <label class="form-label">How would you describe your home environment?</label>
                  <div class="btn-group-vertical w-100">
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.home_environment === 'quiet' }"
                            @click="form.home_environment = 'quiet'">
                      <strong>Quiet & Calm</strong>
                      <small class="d-block text-muted">Peaceful, low noise</small>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.home_environment === 'moderate' }"
                            @click="form.home_environment = 'moderate'">
                      <strong>Moderately Active</strong>
                      <small class="d-block text-muted">Some daily activity</small>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.home_environment === 'active' }"
                            @click="form.home_environment = 'active'">
                      <strong>Very Active</strong>
                      <small class="d-block text-muted">Busy, lots of coming and going</small>
                    </button>
                  </div>
                </div>

                <div class="form-group mb-4">
                  <label class="form-label">How many hours will your pet be alone daily?</label>
                  <div class="btn-group-vertical w-100">
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.hours_alone === '0-4' }"
                            @click="form.hours_alone = '0-4'">
                      <strong>0-4 Hours</strong>
                      <small class="d-block text-muted">Someone is usually home</small>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.hours_alone === '4-8' }"
                            @click="form.hours_alone = '4-8'">
                      <strong>4-8 Hours</strong>
                      <small class="d-block text-muted">Typical work day</small>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.hours_alone === '8+' }"
                            @click="form.hours_alone = '8+'">
                      <strong>8+ Hours</strong>
                      <small class="d-block text-muted">Long periods alone</small>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Step 3: Family, Preferences & Comfort -->
              <div v-if="currentStep === 3" class="quiz-step">
                <h3 class="mb-4">Family, Preferences & Comfort</h3>
                
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
                            :class="{ 'active': form.has_pets === true }"
                            @click="form.has_pets = true">
                      Yes
                    </button>
                    <button type="button" class="btn btn-outline-primary"
                            :class="{ 'active': form.has_pets === false }"
                            @click="form.has_pets = false; form.pets_details = ''">
                      No
                    </button>
                  </div>
                </div>

                <div v-if="form.has_pets" class="form-group mb-4">
                  <label class="form-label">Tell us about your other pets</label>
                  <input type="text" class="form-control" v-model="form.pets_details" 
                         placeholder="e.g., 1 cat, 2 dogs...">
                </div>

                <div class="form-group mb-4">
                  <label class="form-label">Your comfort with grooming:</label>
                  <div class="btn-group-vertical w-100">
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.grooming_comfort === 'uncomfortable' }"
                            @click="form.grooming_comfort = 'uncomfortable'">
                      <strong>Uncomfortable</strong>
                      <small class="d-block text-muted">Prefer low-maintenance pets</small>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.grooming_comfort === 'neutral' }"
                            @click="form.grooming_comfort = 'neutral'">
                      <strong>Neutral</strong>
                      <small class="d-block text-muted">Okay with some grooming</small>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.grooming_comfort === 'comfortable' }"
                            @click="form.grooming_comfort = 'comfortable'">
                      <strong>Comfortable</strong>
                      <small class="d-block text-muted">Happy to groom regularly</small>
                    </button>
                  </div>
                </div>

                <div class="form-group mb-4">
                  <label class="form-label">Your comfort with training:</label>
                  <div class="btn-group-vertical w-100">
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.training_comfort === 'uncomfortable' }"
                            @click="form.training_comfort = 'uncomfortable'">
                      <strong>Uncomfortable</strong>
                      <small class="d-block text-muted">Prefer already-trained pets</small>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.training_comfort === 'neutral' }"
                            @click="form.training_comfort = 'neutral'">
                      <strong>Neutral</strong>
                      <small class="d-block text-muted">Can do basic training</small>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.training_comfort === 'comfortable' }"
                            @click="form.training_comfort = 'comfortable'">
                      <strong>Comfortable</strong>
                      <small class="d-block text-muted">Enjoy training challenges</small>
                    </button>
                  </div>
                </div>

                <div class="form-group mb-4">
                  <label class="form-label">Preferred energy level in a pet:</label>
                  <div class="btn-group-vertical w-100">
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.energy_level === 'low' }"
                            @click="form.energy_level = 'low'">
                      <strong>Low Energy</strong>
                      <small class="d-block text-muted">Calm, relaxed companion</small>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.energy_level === 'medium' }"
                            @click="form.energy_level = 'medium'">
                      <strong>Medium Energy</strong>
                      <small class="d-block text-muted">Balanced activity level</small>
                    </button>
                    <button type="button" class="btn btn-outline-primary text-start"
                            :class="{ 'active': form.energy_level === 'high' }"
                            @click="form.energy_level = 'high'">
                      <strong>High Energy</strong>
                      <small class="d-block text-muted">Active, needs lots of exercise</small>
                    </button>
                  </div>
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

                  <button type="submit" class="btn btn-success" v-if="currentStep === totalSteps" :disabled="loading">
                    <i class="bi bi-check-circle me-2"></i>
                    {{ loading ? 'Saving...' : (hasExistingResults ? 'Update Quiz' : 'Complete Quiz') }}
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
        // Step 1: Basic Information
        living_space: '',
        has_yard: false,
        has_allergies: false,
        allergies: '',
        
        // Step 2: Lifestyle & Experience  
        activity_level: '',
        pet_experience: 'some_experience',
        home_environment: 'quiet',
        hours_alone: '4-8',
        
        // Step 3: Family, Preferences & Comfort
        has_children: false,
        children_ages: '',
        has_pets: false,
        pets_details: '',
        grooming_comfort: 'neutral',
        training_comfort: 'neutral',
        energy_level: 'medium',
        preferred_pet_type: ''
      }
    }
  },
  computed: {
    progress() {
      return (this.currentStep / this.totalSteps) * 100;
    }
  },
  async mounted() {
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
          
          // Map existing results to form fields
          this.form = {
            living_space: existingResults.living_space || '',
            has_yard: existingResults.has_yard || false,
            activity_level: existingResults.activity_level || '',
            preferred_pet_type: existingResults.preferred_pet_type || '',
            has_allergies: existingResults.has_allergies || false,
            allergies: existingResults.allergies || '',
            pet_experience: existingResults.pet_experience || 'some_experience',
            home_environment: existingResults.home_environment || 'quiet',
            has_children: existingResults.has_children || false,
            children_ages: existingResults.children_ages || '',
            has_pets: existingResults.has_pets || false,
            pets_details: existingResults.pets_details || '',
            hours_alone: existingResults.hours_alone || '4-8',
            grooming_comfort: existingResults.grooming_comfort || 'neutral',
            training_comfort: existingResults.training_comfort || 'neutral',
            energy_level: existingResults.energy_level || 'medium'
          };
        }
      } catch (error) {
        console.log('No existing quiz results found');
        this.hasExistingResults = false;
      }
    },

    nextStep() {
      // Validate current step before proceeding
      if (this.validateStep()) {
        this.currentStep++;
      }
    },

    validateStep() {
      switch (this.currentStep) {
        case 1:
          if (!this.form.living_space) {
            alert('Please select your living space');
            return false;
          }
          break;
        case 2:
          if (!this.form.activity_level) {
            alert('Please select your activity level');
            return false;
          }
          if (!this.form.pet_experience) {
            alert('Please select your experience level');
            return false;
          }
          if (!this.form.home_environment) {
            alert('Please select your home environment');
            return false;
          }
          if (!this.form.hours_alone) {
            alert('Please select hours alone');
            return false;
          }
          break;
        case 3:
          if (!this.form.preferred_pet_type) {
            alert('Please select your preferred pet type');
            return false;
          }
          if (!this.form.grooming_comfort) {
            alert('Please select your grooming comfort level');
            return false;
          }
          if (!this.form.training_comfort) {
            alert('Please select your training comfort level');
            return false;
          }
          if (!this.form.energy_level) {
            alert('Please select preferred energy level');
            return false;
          }
          break;
      }
      return true;
    },

    previousStep() {
      if (this.currentStep > 1) {
        this.currentStep--;
      }
    },

    async submitQuiz() {
      if (!this.validateStep()) {
        return;
      }

      this.loading = true;
      
      try {
        // Ensure all required fields have values
        const submissionData = {
          living_space: this.form.living_space,
          has_yard: this.form.has_yard,
          activity_level: this.form.activity_level,
          preferred_pet_type: this.form.preferred_pet_type,
          has_allergies: this.form.has_allergies,
          allergies: this.form.allergies || '',
          pet_experience: this.form.pet_experience,
          home_environment: this.form.home_environment,
          has_children: this.form.has_children,
          children_ages: this.form.children_ages || '',
          has_pets: this.form.has_pets,
          pets_details: this.form.pets_details || '',
          hours_alone: this.form.hours_alone,
          grooming_comfort: this.form.grooming_comfort,
          training_comfort: this.form.training_comfort,
          energy_level: this.form.energy_level
        };

        console.log('Submitting quiz data:', submissionData);

        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/user/quiz`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(submissionData)
        });

        if (response.ok) {
          this.completed = true;
          this.hasExistingResults = true;
          this.$emit('quiz-completed');
        } else {
          const error = await response.json();
          console.error('Backend error:', error);
          alert('Error saving quiz: ' + (error.message || error.error || 'Unknown error'));
        }
      } catch (error) {
        console.error('Quiz submission error:', error);
        alert('Network error. Please try again.');
      } finally {
        this.loading = false;
      }
    },

    redoQuiz() {
      this.completed = false;
      this.currentStep = 1;
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

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text-dark);
}

.btn-group .btn {
  padding: 0.75rem 1.5rem;
}

.btn-group .btn.active {
  background-color: var(--primary-pink);
  border-color: var(--primary-pink);
  color: white;
}
</style>
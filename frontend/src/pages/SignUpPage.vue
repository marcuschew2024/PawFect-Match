<template>
  <div class="auth-page">
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-lg-6 col-md-8">
          <div class="auth-card">
            <h1 class="text-center mb-4">Create Your Account</h1>
            
            <form @submit.prevent="handleSignUp" class="auth-form">
              <div class="row">
                <div class="col-12">
                  <div class="form-group mb-3">
                    <label for="fullName" class="form-label">Full Name *</label>
                    <input
                      type="text"
                      class="form-control"
                      id="fullName"
                      v-model="form.full_name"
                      required
                      placeholder="Enter your full name"
                    >
                  </div>
                </div>
                
                <div class="col-12">
                  <div class="form-group mb-3">
                    <label for="email" class="form-label">Email Address *</label>
                    <input
                      type="email"
                      class="form-control"
                      id="email"
                      v-model="form.email"
                      required
                      placeholder="Enter your email"
                    >
                  </div>
                </div>
                
                <div class="col-12">
                  <div class="form-group mb-3">
                    <label for="password" class="form-label">Password *</label>
                    <input
                      type="password"
                      class="form-control"
                      id="password"
                      v-model="form.password"
                      required
                      placeholder="Create a password"
                      minlength="6"
                    >
                    <div class="form-text">Password must be at least 6 characters long.</div>
                  </div>
                </div>
                
                <div class="col-12">
                  <div class="form-group mb-3">
                    <label for="phone" class="form-label">Phone Number</label>
                    <input
                      type="tel"
                      class="form-control"
                      id="phone"
                      v-model="form.phone"
                      placeholder="Enter your phone number"
                    >
                  </div>
                </div>
                
                <div class="col-12">
                  <div class="form-group mb-4">
                    <label for="address" class="form-label">Address</label>
                    <textarea
                      class="form-control"
                      id="address"
                      v-model="form.address"
                      rows="3"
                      placeholder="Enter your address"
                    ></textarea>
                  </div>
                </div>
              </div>

              <div v-if="error" class="alert alert-danger" role="alert">
                {{ error }}
              </div>

              <button 
                type="submit" 
                class="btn btn-primary w-100 mb-3"
                :disabled="loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ loading ? 'Creating Account...' : 'Create Account' }}
              </button>

              <div class="text-center">
                <p class="mb-0">
                  Already have an account? 
                  <router-link to="/login" class="auth-link">Sign In</router-link>
                </p>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const API_BASE_URL = 'http://localhost:3000/api';

export default {
  name: 'SignUpPage',
  data() {
    return {
      form: {
        email: '',
        password: '',
        full_name: '',
        phone: '',
        address: ''
      },
      loading: false,
      error: ''
    }
  },
  methods: {
    async handleSignUp() {
      this.loading = true;
      this.error = '';

      try {
        const response = await fetch(`${API_BASE_URL}/auth/signup`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.form)
        });

        const data = await response.json();

        if (response.ok) {
          // Store token and user data
          localStorage.setItem('authToken', data.token);
          localStorage.setItem('user', JSON.stringify(data.user));
          
          // Emit auth change event to parent
          this.$emit('auth-change');
          
          this.$router.push('/pets');
        } else {
          this.error = data.error || 'Sign up failed. Please try again.';
        }
      } catch (error) {
        this.error = 'Network error. Please try again.';
        console.error('Sign up error:', error);
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.auth-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(255, 182, 193, 0.15);
  border: 1px solid var(--border-light);
}
</style>
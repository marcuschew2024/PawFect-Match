<template>
  <div class="auth-page">
    <div class="container my-5">
      <div class="row justify-content-center">
        <div class="col-lg-6 col-md-8">
          <div class="auth-card">
            <h1 class="text-center mb-4">Welcome Back</h1>
            
            <form @submit.prevent="handleLogin" class="auth-form">
              <div class="form-group mb-3">
                <label for="email" class="form-label">Email Address</label>
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  v-model="form.email"
                  required
                  placeholder="Enter your email"
                >
              </div>

              <div class="form-group mb-4">
                <label for="password" class="form-label">Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  v-model="form.password"
                  required
                  placeholder="Enter your password"
                >
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
                {{ loading ? 'Signing In...' : 'Sign In' }}
              </button>

              <div class="text-center">
                <p class="mb-0">
                  Don't have an account? 
                  <router-link to="/signup" class="auth-link">Create Account</router-link>
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
import { getApiBaseUrl } from '@/utils/config';
const API_BASE_URL = getApiBaseUrl();
//const API_BASE_URL = 'http://localhost:3000/api';

export default {
  name: 'LoginPage',
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      loading: false,
      error: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = '';

      try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
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
          this.error = data.error || 'Invalid email or password.';
        }
      } catch (error) {
        this.error = 'Network error. Please try again.';
        console.error('Login error:', error);
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

.auth-form .form-label {
  color: var(--text-dark);
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.auth-form .form-control {
  border: 2px solid var(--border-light);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
}

.auth-form .form-control:focus {
  border-color: var(--primary-pink);
  box-shadow: 0 0 0 3px rgba(255, 182, 193, 0.2);
}

.auth-link {
  color: var(--primary-pink-dark);
  text-decoration: none;
  font-weight: 600;
}

.auth-link:hover {
  color: var(--primary-pink);
  text-decoration: underline;
}
</style>
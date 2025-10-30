<template>
  <div id="app">
    <!-- Header -->
    <nav class="navbar navbar-expand-lg">
      <div class="container">
        <div class="d-flex align-items-center">
          <img src="https://cdn-icons-png.flaticon.com/512/616/616430.png" alt="Cat Logo" height="40">
          <router-link to="/" class="navbar-brand">PawFect Match</router-link>
        </div>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/" class="nav-link">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/about" class="nav-link">About Us</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/pets" class="nav-link">Pet Listing</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <router-link to="/add-pet" class="nav-link">List a Pet</router-link>
            </li>
<<<<<<< Updated upstream
            
            
=======
            <li class="nav-item">
              <router-link to="/community" class="nav-link">
                Community
              </router-link>
            </li>


>>>>>>> Stashed changes
            <!-- Authentication Section -->
            <li class="nav-item dropdown" v-if="!isAuthenticated">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                <i class="bi bi-person me-1"></i>Account
              </a>
              <ul class="dropdown-menu">
                <li><router-link to="/login" class="dropdown-item">Login</router-link></li>
                <li><router-link to="/signup" class="dropdown-item">Sign Up</router-link></li>
              </ul>
            </li>
            
            <li class="nav-item dropdown" v-else>
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                <i class="bi bi-person-circle me-1"></i>{{ user?.full_name || 'User' }}
              </a>
              <ul class="dropdown-menu">
                <li><router-link to="/profile" class="dropdown-item">
                  <i class="bi bi-person me-2"></i>My Profile
                </router-link></li>
                <li><router-link to="/favorites" class="dropdown-item">
                  <i class="bi bi-heart me-2"></i>My Favorites
                </router-link></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item" href="#" @click="handleLogout"><i class="bi bi-box-arrow-right me-2"></i>Logout</a></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main>
      <router-view @auth-change="checkAuth"/>
    </main>

    <!-- Footer -->
    <footer>
      <div class="container">
        <div class="row">
          <!-- Explore Column -->
          <div class="col-md-4 mb-4">
            <h6 class="footer-heading">Explore</h6>
            <ul class="footer-links">
              <li><router-link to="/">Home</router-link></li>
              <li><router-link to="/about">About Us</router-link></li>
              <li><router-link to="/pets">Pet Listing</router-link></li>
              <li><router-link to="/add-pet">List a Pet</router-link></li>
            </ul>
          </div>

          <!-- Contact Column -->
          <div class="col-md-4 mb-4">
            <h6 class="footer-heading">Contact</h6>
            <ul class="footer-links">
              <li><a href="#">Contact Us</a></li>
              <li><a href="mailto:pawfectmatch@gmail.com">pawfectmatch@gmail.com</a></li>
              <li><a href="tel:+6588398193">Tel: 8839 8193</a></li>
            </ul>
          </div>

          <!-- Follow Us Column -->
          <div class="col-md-4 mb-4">
            <h6 class="footer-heading">Follow Us</h6>
            <div class="social-icons">
              <a href="#"><i class="bi bi-facebook"></i></a>
              <a href="#"><i class="bi bi-instagram"></i></a>
              <a href="#"><i class="bi bi-tiktok"></i></a>
            </div>
            <div class="brand-section mt-4">
              <div class="d-flex align-items-center">
                <img src="https://cdn-icons-png.flaticon.com/512/616/616430.png" alt="PawFect Match Logo" height="40" class="me-2">
                <h5 class="brand-name">PawFect Match</h5>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isAuthenticated: false,
      user: null
    }
  },
  mounted() {
    this.checkAuth();
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem('authToken');
      const userData = localStorage.getItem('user');
      
      this.isAuthenticated = !!token;
      if (userData) {
        try {
          this.user = JSON.parse(userData);
        } catch (e) {
          console.error('Error parsing user data:', e);
          this.user = null;
        }
      } else {
        this.user = null;
      }
      
      console.log('Auth check:', { isAuthenticated: this.isAuthenticated, user: this.user });
    },
    handleLogout() {
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      this.isAuthenticated = false;
      this.user = null;
      this.$router.push('/');
    }
  }
}

</script>

<style>
/* No inline CSS - all styles are in the external file */
</style>
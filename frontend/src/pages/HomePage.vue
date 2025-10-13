<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <div class="row align-items-center min-vh-75">
          <div class="col-lg-6">
            <h1 class="hero-title">Find Your Perfect Furry Friend</h1>
            <p class="hero-subtitle">
              Welcome to PawFect Match, where we help you find the perfect pet companion. 
              Browse through our adorable pets waiting for their forever homes.
            </p>
            <div class="hero-buttons">
              <router-link to="/pets" class="btn btn-primary me-3">
                Browse Pets
              </router-link>
              <router-link to="/about" class="btn btn-outline-secondary">
                Learn More
              </router-link>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="hero-image">
              <img src="https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=600&h=500&fit=crop" 
                   alt="Happy pets" class="img-fluid rounded">
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section py-5">
      <div class="container">
        <div class="row text-center">
          <div class="col-lg-4 mb-4">
            <div class="feature-card p-4">
              <i class="bi bi-heart feature-icon"></i>
              <h4>Loving Companions</h4>
              <p>Find pets that match your lifestyle and become lifelong friends.</p>
            </div>
          </div>
          <div class="col-lg-4 mb-4">
            <div class="feature-card p-4">
              <i class="bi bi-house-check feature-icon"></i>
              <h4>Forever Homes</h4>
              <p>Help provide loving forever homes for pets in need of adoption.</p>
            </div>
          </div>
          <div class="col-lg-4 mb-4">
            <div class="feature-card p-4">
              <i class="bi bi-shield-check feature-icon"></i>
              <h4>Safe Adoption</h4>
              <p>All our pets are health-checked and ready for their new families.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
}
</script>


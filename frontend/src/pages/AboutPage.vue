<template>
  <div class="about-page">
    <!-- 1. Hero Section -->
    <section class="hero-section text-center">
      <div class="container">
        <h1 class="hero-title">Giving Every Pet a Second Chance</h1>
        <p class="hero-subtitle lead">
          We are dedicated to connecting loving families with pets in need of their forever homes.
        </p>
        <router-link to="/pets" class="btn btn-primary btn-lg mt-3">
          Meet Our Pets <i class="bi bi-arrow-right-short"></i>
        </router-link>
      </div>
    </section>

    <!-- 2. About Us Section -->
    <section class="about-us-section py-5">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6 mb-4 mb-lg-0">
            <img src="https://images.unsplash.com/photo-1623387641168-d9803ddd3f35?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=2070"
              alt="A variety of happy pets including a dog, cat, and rabbit" class="img-fluid rounded shadow-heavy">
          </div>
          <div class="col-lg-6">
            <div class="about-us-content">
              <h2 class="section-title">About PawFect Match</h2>
              <p>
                PawFect Match was founded with the mission to reduce the number of homeless pets
                and help every animal find their perfect family. We believe that every pet deserves
                a loving home and every family deserves the joy of a furry companion.
              </p>
              <p>
                Our platform makes it easy to browse available pets, learn about their personalities,
                and start the adoption process. We work with trusted shelters and foster families
                to ensure all our pets are healthy, vaccinated, and ready for their new homes.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 3. Our Impact Section -->
    <section class="impact-section py-5">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="section-title">Our Impact, By the Numbers</h2>
          <p class="lead text-muted">We're proud of the community we've built and the lives we've changed.</p>
        </div>
        <div class="row text-center">
          <div class="col-md-4 mb-4">
            <div class="impact-card h-100">
              <i class="bi bi-heart-fill impact-icon"></i>
              <h3>500+</h3>
              <p>Pets Rehomed</p>
            </div>
          </div>
          <div class="col-md-4 mb-4">
            <div class="impact-card h-100">
              <i class="bi bi-house-heart-fill impact-icon"></i>
              <h3>15</h3>
              <p>Shelter Partners</p>
            </div>
          </div>
          <div class="col-md-4 mb-4">
            <div class="impact-card h-100">
              <i class="bi bi-people-fill impact-icon"></i>
              <h3>100%</h3>
              <p>Volunteer Run</p>
            </div>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script>
export default {
  name: 'AboutPage'
}
</script>

<style scoped>

/* Hero Section */
.hero-section {
  padding: 4rem 0;
  background-color: var(--background-light);
  border-bottom: 1px solid var(--border-light);
}

.hero-title {
  font-size: 2.8rem;
  font-weight: 700;
  color: var(--text-dark);
  animation: fadeInUp 0.5s ease-out;
}

.hero-subtitle {
  font-size: 1.15rem;
  max-width: 600px;
  margin: 1rem auto 0;
  color: var(--text-medium);
  animation: fadeInUp 0.7s ease-out;
}

.hero-section .btn {
  animation: fadeInUp 0.9s ease-out;
}

/* About Us Section */
.about-us-section .img-fluid {
  box-shadow: var(--shadow-heavy);
}

.about-us-content p {
  line-height: 1.8;
  color: var(--text-medium);
}

.section-title {
  color: var(--text-dark);
  font-weight: 700;
  margin-bottom: 1.5rem;
}

/* Impact Section */
.impact-section {
  background-color: var(--background-white);
}

.impact-card {
  background: var(--background-light);
  padding: 2.5rem 1.5rem;
  border-radius: 12px;
  border: 1px solid var(--border-light);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.impact-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-heavy);
}

.impact-icon {
  font-size: 2.5rem;
  color: var(--primary-pink);
  margin-bottom: 1rem;
}

.impact-card h3 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-dark);
}

.impact-card p {
  color: var(--text-medium);
  font-size: 1.1rem;
  margin-bottom: 0;
}

/* Meet Our Pets Button */
.btn-primary {
  background-color: var(--primary-pink);
  border-color: var(--primary-pink);
  color: var(--text-dark);
}

.btn-primary:hover {
  background-color: var(--primary-pink-dark);
  border-color: var(--primary-pink-dark);
}
</style>
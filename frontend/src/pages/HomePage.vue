<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section d-flex align-items-center">
      <div class="container">
        <!-- align image to center -->
        <div class="row align-items-center">

          <div class="col-lg-6 text-start">
            <div class="badge-pill mb-3">
              <i class="bi bi-heart-fill me-2"></i>Find Your Perfect Companion
            </div>
            <h1 class="hero-title mb-3">
              Your <span class="highlight">Pawfect Match</span> Awaits
            </h1>
            <p class="hero-subtitle mb-4">
              Discover your ideal furry friend through our lifestyle quiz.
              Every pet deserves a loving home, and every person deserves the perfect companion.
            </p>
            <div class="hero-buttons mb-5">
              <router-link to="/pets" class="btn btn-hero-primary me-3 mb-2">
                Browse Pets <i class="bi bi-arrow-right ms-2"></i>
              </router-link>
            </div>

            <!-- Stats for how many adoptions so far and success rate in matching -->
            <div class="row stats-row">
              <div class="col-6">
                <div class="stat-item">
                  <h3 class="stat-number">500+</h3>
                  <p class="stat-label">Happy Adoptions</p>
                </div>
              </div>
              <div class="col-6">
                <div class="stat-item">
                  <h3 class="stat-number">95%</h3>
                  <p class="stat-label">Match Success Rate</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Hero Image -->
          <div class="col-lg-6">
            <div class="hero-image position-relative">
              <img
                src="https://plus.unsplash.com/premium_photo-1664908327473-9323161a566b?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=1170"
                alt="happy cat owner image" class="img-fluid rounded-4 hero-main-img">
              <div class="match-card">
                <i class="bi bi-heart-fill text-danger me-2"></i>
                <div>
                  <strong>98% Match!</strong>
                  <p class="mb-0 small">Sarah & Max</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- About Us -->
    <section class="About-section py-5">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6 mb-4 mb-lg-0">
            <div class="about-images">
              <img
                src="https://images.unsplash.com/photo-1548199973-03cce0bbc87b?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=1169"
                alt="Happy dogs" class="img-fluid rounded-4 shadow">
            </div>
          </div>
          <div class="col-lg-6">
            <div class="badge-pill mb-3">
              <i class="bi bi-people-fill me-2"></i>Our Mission
            </div>
            <h2 class="section-title mb-4">About Pawfect Match </h2>
            <p class="section-text mb-4">
              We are more than an adoption site — we are matchmakers for people and pets. Using our smart compatibility
              quiz, we connect loving families with pets that feel just right. Get to know how PawFect Match started and
              what drives us every day.
            </p>
            <router-link to="/About" class="btn btn-coral">
              Learn More About Us <i class="bi bi-arrow-right ms-2"></i>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- steps to have a successful pet adoption experiencee -->
    <section class="step-section py-5">
      <div class="container">
        <div class="text-center mb-5">
          <div class="badge-pill mb-3 d-inline-block">
            <i class="bi bi-lightbulb-fill me-2"></i>4 Easy Steps
          </div>
          <h2 class="section-title">How Pawfect Match Works</h2>
          <p class="section-subtitle">Follow these four simple steps to find the pet that is meant for you</p>
        </div>

        <div class="row">
          <div class="col-lg-3 col-md-6 mb-4">
            <div class="step-card text-center h-100">
              <div class="step-number">1</div>
              <div class="step-icon">
                <i class="bi bi-person-plus"></i>
              </div>
              <h4 class="process-title">Create an Account</h4>
              <p class="process-text">Sign up in minutes so as to access features such as the lifestyle quiz</p>
            </div>
          </div>

          <div class="col-lg-3 col-md-6 mb-4">
            <div class="step-card text-center h-100">
              <div class="step-number">2</div>
              <div class="step-icon">
                <i class="bi bi-clipboard-check"></i>
              </div>
              <h4 class="process-title">Lifestyle Quiz</h4>
              <p class="process-text">Answer questions about your lifestyle and daily routine to help
                us understand you better.</p>
            </div>
          </div>

          <div class="col-lg-3 col-md-6 mb-4">
            <div class="step-card text-center h-100">
              <div class="step-number">3</div>
              <div class="step-icon">
                <i class="bi bi-heart"></i>
              </div>
              <h4 class="process-title">Get Compatibility Scores</h4>
              <p class="process-text">Browse pets with a higher compatibility scores. See which furry friends match
                your lifestyle best.</p>
            </div>
          </div>

          <div class="col-lg-3 col-md-6 mb-4">
            <div class="step-card text-center h-100">
              <div class="step-number">4</div>
              <div class="step-icon">
                <i class="bi bi-check-circle"></i>
              </div>
              <h4 class="process-title">Submit Adoption Form</h4>
              <p class="process-text">Choose your pawfect pet and complete the adoption form. We will review and update your adoption status.</p>
            </div>
          </div>
        </div>

        <!-- <div class="text-center mt-4">
          <router-link to="/pets" class="btn btn-coral btn-lg">
            Start Your Journey <i class="bi bi-arrow-right ms-2"></i>
          </router-link>
        </div> -->
      </div>
    </section>

    <!-- adoption success stories Section -->
    <section class="success-section py-5">
      <div class="container">
        <div class="text-center mb-5">
          <div class="badge-pill mb-3 d-inline-block">
            <i class="bi bi-heart-fill me-2"></i>Happy Tails
          </div>
          <h2 class="section-title">Pawfect Success Stories</h2>
          <p class="section-subtitle">Don't take our word for it, hear from individuals with successful adoption stories!</p>
        </div>

        <div class="row">
          <div class="col-lg-4 mb-4">
            <div class="story-card h-100">
              <div class="match-badge">98% Match</div>
              <img
                src="https://plus.unsplash.com/premium_photo-1664371675043-a0a8e5173d9c?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=688"
                alt="fluffy cat" class="img-fluid story-img">
              <div class="story-content">
                <div class="d-flex align-items-center mb-3">
                  <img src="https://i.pravatar.cc/50?img=1" alt="Sarah" class="rounded-circle me-2" width="40"
                    height="40">
                  <div>
                    <h5 class="mb-0">Sarah & Fluffy</h5>
                    <small class="text-muted">Adopted 5 months ago</small>
                  </div>
                </div>
                <p class="story-text">"Fluffy is my calm companion after long work days. She loves lounging on the couch
                  as much as I do. The matching system really understood what I needed."</p>
              </div>
            </div>
          </div>

          <div class="col-lg-4 mb-4">
            <div class="story-card h-100">
              <div class="match-badge">96% Match</div>
              <img
                src="https://plus.unsplash.com/premium_photo-1718358631714-05d459d32ab8?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=1170"
                alt="Orange cat with bow tie" class="img-fluid story-img">
              <div class="story-content">
                <div class="d-flex align-items-center mb-3">
                  <img src="https://i.pravatar.cc/50?img=5" alt="Roffy" class="rounded-circle me-2" width="40"
                    height="40">
                  <div>
                    <h5 class="mb-0">Lina & Roffy</h5>
                    <small class="text-muted">Adopted 1 year ago</small>
                  </div>
                </div>
                <p class="story-text">"Roffy is the perfect running buddy I always dreamed of! The compatibility quiz
                  nailed it - our energy levels match perfectly. Every morning run is pure joy!"</p>
              </div>
            </div>
          </div>

          <div class="col-lg-4 mb-4">
            <div class="story-card h-100">
              <div class="match-badge">99% Match</div>
              <img
                src="https://plus.unsplash.com/premium_photo-1694819488591-a43907d1c5cc?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=714"
                alt="Buddy" class="img-fluid story-img">
              <div class="story-content">
                <div class="d-flex align-items-center mb-3">
                  <img src="https://i.pravatar.cc/50?img=9" alt="Emily" class="rounded-circle me-2" width="40"
                    height="40">
                  <div>
                    <h5 class="mb-0">Emily & Buddy</h5>
                    <small class="text-muted">Adopted 3 months ago</small>
                  </div>
                </div>
                <p class="story-text">"Buddy fits into our family like she's always been here. The kids adore her gentle
                  nature. Pawfect Match truly found us our pawfect match!"</p>
              </div>
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

<style scoped>

/* Hero Section */
.hero-section {
  min-height: 100vh;
  background: linear-gradient(135deg, #FFF5F5 0%, #FFF0F0 100%);
  padding: 100px 0 60px;
}

.badge-pill {
  display: inline-block;
  background: #FFE5E5;
  color: #eb7e7e;
  padding: 8px 20px;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 500;
}

.hero-title {
  text-align: left;
  /* font-weight: 800; */
  font-size: 2.5 rem;
  line-height: 1.2;
  /* color: #1a1a1a; */
  color: var(--text-dark);

}

.highlight {
  color: #FF9A9E;
}

.hero-subtitle {
  color: #666;
  font-size: 1.15rem;
  line-height: 1.7;
}

.btn-hero-primary {
  background: linear-gradient(135deg, #ff8488 0%, #fc9d9d 100%);
  color: white;
  border: none;
  padding: 14px 32px;
  border-radius: 50px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 154, 158, 0.3);
}

.btn-hero-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 154, 158, 0.4);
  background: linear-gradient(135deg, #eb7e7e 0%, #FF9A9E 100%);
  color: white;
}

.btn-hero-outline {
  background: white;
  color: #666;
  border: 2px solid #e0e0e0;
  padding: 14px 32px;
  border-radius: 50px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-hero-outline:hover {
  border-color: #FF9A9E;
  color: #FF9A9E;
  background: #FFF5F5;
}

.stats-row {
  margin-top: 40px;
}

.stat-item {
  border-left: 3px solid #FF9A9E;
  padding-left: 20px;
}

.stat-number {
  font-size: 2.7rem;
  font-weight: 700;
  color: var(--text-dark);
  /* color: #1a1a1a; */
  margin-bottom: 5px;
}

.stat-label {
  color: #666;
  font-size: 0.95rem;
  margin: 0;
}

.hero-image {
  position: relative;
  padding: 20px;
}

.hero-main-img {
  border-radius: 30px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  width: 100%;
  height: auto;
}

.match-card {
  position: absolute;
  bottom: 40px;
  left: 40px;
  background: white;
  padding: 16px 24px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  gap: 10px;
}

.match-card strong {
  display: block;
  color: #1a1a1a;
  font-size: 1rem;
}

.match-card p {
  color: #666;
  font-size: 0.85rem;
}

/* About Section */
.About-section {
  padding: 100px 0;
  background: white;
}

.about-images {
  position: relative;
  max-width: 90%;
  margin: auto;
}

.mission-img-1 {
  position: absolute;
  width: 65%;
  top: 0;
  left: 0;
  z-index: 2;
  border-radius: 25px;
}

.mission-img-2 {
  position: absolute;
  width: 55%;
  bottom: 0;
  right: 0;
  z-index: 1;
  border-radius: 25px;
}

.experience-badge {
  position: absolute;
  bottom: 60px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #FF9A9E 0%, #FFB5B5 100%);
  color: white;
  padding: 20px 30px;
  border-radius: 20px;
  text-align: center;
  z-index: 3;
  box-shadow: 0 10px 30px rgba(255, 154, 158, 0.4);
}

.experience-badge h4 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 0;
}

.experience-badge p {
  font-size: 0.9rem;
  margin-bottom: 0;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 20px;
}

.section-text {
  color: #666;
  font-size: 1.05rem;
  line-height: 1.8;
}

.section-subtitle {
  color: #666;
  font-size: 1.1rem;
  max-width: 700px;
  margin: 0 auto;
}

.btn-coral {
  background: linear-gradient(135deg, #ff8488 0%, #fc9d9d 100%);
  color: white;
  border: none;
  padding: 12px 25px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-coral:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 154, 158, 0.4);
  background: linear-gradient(135deg, #eb7e7e 0%, #FF9A9E 100%);
  color: white;
}

/* step section */
.step-section {
  padding: 100px 0;
  background: linear-gradient(135deg, #FFF5F5 0%, #FFF0F0 100%);
}

.step-card {
  background: white;
  padding: 40px 30px;
  border-radius: 25px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  position: relative;
}

.step-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
}

.step-number {
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #FF9A9E 0%, #FFB5B5 100%);
  color: white;
  width: 45px;
  height: 45px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.2rem;
}

.step-icon {
  background: #FFE5E5;
  width: 80px;
  height: 80px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 30px auto 20px;
  font-size: 2rem;
  color: #FF9A9E;
}

.process-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-dark);
  margin-bottom: 15px;
}

.process-text {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0;
}

/* Success Stories Section */
.success-section {
  padding: 100px 0;
  background: white;
}

.story-card {
  background: white;
  border-radius: 25px;
  overflow: hidden;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  position: relative;
}

.story-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
}

.match-badge {
  position: absolute;
  top: 20px;
  right: 20px;
  background: white;
  color: #FF9A9E;
  padding: 8px 16px;
  border-radius: 50px;
  font-weight: 600;
  font-size: 0.85rem;
  z-index: 2;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.story-img {
  width: 100%;
  height: 280px;
  object-fit: cover;
}

.story-content {
  padding: 30px;
}

.story-text {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.7;
  margin: 0;
}

.btn-outline-coral {
  background: transparent;
  color: #FF9A9E;
  border: 2px solid #FF9A9E;
  padding: 12px 28px;
  border-radius: 50px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-outline-coral:hover {
  background: linear-gradient(135deg, #FF9A9E 0%, #FFB5B5 100%);
  color: white;
  border-color: transparent;
  transform: translateY(-2px);
}

/* Responsive Design */
@media (max-width: 991px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-section {
    min-height: auto;
    padding: 80px 0 40px;
  }

  .about-images {
    height: 400px;
    margin-bottom: 40px;
  }

  .section-title {
    font-size: 2rem;
  }

  .cta-title {
    font-size: 2rem;
  }
}

@media (max-width: 767px) {
  .hero-title {
    font-size: 2rem;
  }

  .stat-number {
    font-size: 2rem;
  }

  .match-card {
    bottom: 20px;
    left: 20px;
    padding: 12px 16px;
  }

  .about-images {
    height: 350px;
  }

  .experience-badge {
    padding: 15px 20px;
  }

  .experience-badge h4 {
    font-size: 2rem;
  }

  .step-section,
  .About-section,
  .success-section {
    padding: 60px 0;
  }

  .cta-section {
    padding: 60px 20px;
  }
}
</style>
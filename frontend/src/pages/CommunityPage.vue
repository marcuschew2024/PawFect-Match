<template>
  <div class="container my-5">
    <!-- Toast Notifications -->
    <div class="toast-container">
      <transition-group name="toast">
        <div
          v-for="toast in toastNotifications"
          :key="toast.id"
          :class="['toast-notification', `toast-${toast.type}`]"
          @click="removeToastNotification(toast.id)"
        >
          <div class="toast-icon">
            <i
              :class="[
                'bi',
                toast.type === 'warning' ? 'bi-exclamation-triangle-fill' :
                toast.type === 'success' ? 'bi-check-circle-fill' :
                toast.type === 'error' ? 'bi-x-circle-fill' :
                'bi-info-circle-fill'
              ]"
            ></i>
          </div>
          <div class="toast-content">
            <p class="toast-message">{{ toast.message }}</p>
          </div>
          <button class="toast-close" @click.stop="removeToastNotification(toast.id)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </transition-group>
    </div>

    <!-- Auth Modal Notification -->
    <transition name="fade">
      <div v-if="showNotification" class="auth-modal-overlay" @click="closeNotification">
        <div class="auth-modal-content" @click.stop>
          <button class="auth-modal-close" @click="closeNotification">&times;</button>
          <div class="auth-modal-icon">
            <i class="bi bi-lock-fill"></i>
          </div>
          <h3 class="auth-modal-title">{{ notificationTitle }}</h3>
          <p class="auth-modal-message">{{ notificationMessage }}</p>
          <div class="auth-modal-actions">
            <button class="btn btn-auth-primary" @click="goToLogin">Sign In</button>
            <button class="btn btn-auth-secondary" @click="closeNotification">Maybe Later</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-3">
      <h1 class="fw-bold mb-0">Community Forum</h1>
      <div v-if="isAuthenticated">
        <button class="btn btn-pink" @click="openQuestionModal">
          <i class="bi bi-pencil-square me-2"></i>Ask a Question
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="filter-section mb-5">
      <div class="row g-3 align-items-end">
        <div class="col-md-6">
          <label for="searchInput" class="form-label">Search Questions</label>
          <input
            type="text"
            id="searchInput"
            class="form-control"
            v-model="searchTerm"
            placeholder="Search by title or content..."
          />
        </div>
        <div class="col-md-3">
          <label for="categoryFilter" class="form-label">Category</label>
          <select id="categoryFilter" class="form-select" v-model="filters.category">
            <option value="all">All Categories</option>
            <option v-for="cat in categories" :key="cat.value" :value="cat.value">{{ cat.label }}</option>
          </select>
        </div>
        <div class="col-md-3">
          <div class="d-flex gap-2">
            <button class="btn btn-box flex-fill" @click="applyFilters">
              <i class="bi bi-funnel me-2"></i>Apply
            </button>
            <button class="btn btn-outline-secondary" @click="resetFilters">
              <i class="bi bi-arrow-clockwise"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading / Empty -->
    <div v-if="loading" class="text-center py-5">
      <i class="bi bi-arrow-repeat spinner me-2"></i>Loading...
    </div>
    <div v-else-if="error" class="text-center text-danger py-5">{{ error }}</div>
    <div v-else-if="filteredQuestions.length === 0" class="text-center text-muted py-5">
      <i class="bi bi-chat-left-text display-5"></i>
      <p>No discussions found.</p>
    </div>

    <!-- Questions -->
    <div v-else class="questions-grid">
      <div v-for="question in filteredQuestions" :key="question.id" class="question-card">
        <div class="card-body">
          <h5 class="fw-semibold mb-2">{{ question.title }}</h5>
          <p class="text-muted mb-3">{{ truncateContent(question.content) }}</p>

          <div class="d-flex justify-content-between align-items-center flex-wrap small text-muted mb-3">
            <div>
              <i class="bi bi-person-circle me-1"></i>{{ question.author }} •
              <i class="bi bi-calendar3 ms-1 me-1"></i>{{ formatDate(question.createdAt) }}
            </div>
            <div>
              <span class="badge bg-light text-dark me-2">{{ question.category }}</span>
              <span class="badge bg-primary">{{ question.answers.length }} Answers</span>
            </div>
          </div>

          <!-- Reply input -->
          <div v-if="isAuthenticated" class="reply-box mb-3">
            <textarea
              class="form-control"
              v-model="question.newAnswer"
              rows="2"
              placeholder="Write your reply..."
            ></textarea>
          </div>

          <!-- Buttons row -->
          <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mt-2">
            <div class="d-flex gap-2">
              <button
                class="btn btn-pink-outline btn-sm"
                @click="handleReplyClick(question)"
              >
                <i class="bi bi-send me-1"></i>Reply
              </button>
              <button class="btn btn-pink-outline btn-sm" @click="toggleDiscussion(question.id)">
                <i
                  class="bi me-1"
                  :class="expandedQuestion === question.id ? 'bi-chevron-up' : 'bi-chevron-down'"
                ></i>
                {{ expandedQuestion === question.id ? 'Hide Discussion' : 'View Discussion' }}
              </button>
            </div>

            <div>
              <button 
                :class="['btn btn-sm', question.liked ? 'btn-danger' : 'btn-outline-danger']"
                @click="toggleQuestionLike(question)"
              >
                <i :class="question.liked ? 'bi bi-hand-thumbs-up-fill' : 'bi bi-hand-thumbs-up'"></i>
                {{ question.likes }}
              </button>
            </div>
          </div>

          <!-- Dropdown replies -->
          <transition name="fade">
            <div v-if="expandedQuestion === question.id" class="discussion-dropdown mt-3">
              <div v-if="question.answers.length === 0" class="text-muted small text-center py-3">
                No replies yet. Be the first to respond!
              </div>

              <div v-for="answer in sortedAnswers(question.answers)" :key="answer.id" class="answer-item">
                <div class="d-flex justify-content-between align-items-start">
                  <small class="text-muted">
                    <i class="bi bi-person-circle me-1"></i>{{ answer.author }} •
                    {{ formatDate(answer.createdAt) }}
                  </small>
                  <div class="d-flex gap-2">
                    <button
                      v-if="answer.author_id === currentUserId"
                      class="btn btn-outline-danger btn-sm"
                      @click="deleteAnswer(answer.id)"
                    >
                      Delete
                    </button>
                    <button 
                      :class="['btn btn-sm', answer.liked ? 'btn-primary' : 'btn-outline-primary']"
                      @click="toggleAnswerLike(answer)"
                    >
                      <i :class="answer.liked ? 'bi bi-hand-thumbs-up-fill' : 'bi bi-hand-thumbs-up'"></i>
                      {{ answer.likes }}
                    </button>
                  </div>
                </div>
                <p class="mt-2 mb-0">{{ answer.content }}</p>
              </div>
            </div>
          </transition>
        </div>
      </div>
    </div>

    <!-- Ask Question Modal -->
    <div v-if="showQuestionModal" class="modal-overlay" @click="closeQuestionModal">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h3>Ask a Question</h3>
          <button class="btn-close" @click="closeQuestionModal">&times;</button>
        </div>

        <div class="modal-body">
          <div class="mb-3">
            <label class="form-label">Title</label>
            <input type="text" class="form-control" v-model="newQuestion.title" />
          </div>

          <div class="mb-3">
            <label class="form-label">Category</label>
            <select class="form-select" v-model="newQuestion.category" required>
              <option disabled value="">Select a category</option>
              <option v-for="cat in categories" :key="cat.value" :value="cat.value">{{ cat.label }}</option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Content</label>
            <textarea class="form-control" v-model="newQuestion.content" rows="5"></textarea>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn btn-secondary" @click="closeQuestionModal">Cancel</button>
          <button class="btn btn-pink" @click="submitQuestion">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const API_BASE_URL = "http://localhost:3000/api";

export default {
  name: "CommunityPage",
  data() {
    return {
      questions: [],
      filteredQuestions: [],
      filters: { category: "all" },
      categories: [
        { label: "General", value: "general" },
        { label: "Health", value: "health" },
        { label: "Training", value: "training" },
        { label: "Adoption", value: "adoption" },
        { label: "Nutrition", value: "nutrition" },
      ],
      searchTerm: "",
      loading: true,
      error: null,
      isAuthenticated: false,
      currentUserId: null,
      expandedQuestion: null,

      // Ask question modal
      showQuestionModal: false,
      newQuestion: { title: "", content: "", category: "general" },

      // Notification system
      showNotification: false,
      notificationMessage: "",
      notificationTitle: "",
      notificationType: "info", // success, error, warning, info
      notificationTimeout: null,

      // Toast notification system
      toastNotifications: [],
      toastIdCounter: 0,
    };
  },
  computed: {
    notificationIcon() {
      const icons = {
        success: "bi-check-circle-fill",
        error: "bi-x-circle-fill",
        warning: "bi-exclamation-triangle-fill",
        info: "bi-info-circle-fill",
      };
      return icons[this.notificationType] || "bi-info-circle-fill";
    },
  },
  async mounted() {
    this.checkAuth();
    await this.fetchQuestions();
  },
  methods: {
    // Notification methods
    showAuthModal(title, message) {
      this.notificationTitle = title;
      this.notificationMessage = message;
      this.showNotification = true;
    },
    closeNotification() {
      this.showNotification = false;
    },
    goToLogin() {
      // Redirect to login page - adjust this route as needed
      this.$router.push('/login');
      // OR if you don't have router:
      // window.location.href = '/login';
    },
    showToastNotification(message, type = "info") {
      const id = this.toastIdCounter++;
      const toast = { id, message, type };
      this.toastNotifications.push(toast);
      
      setTimeout(() => {
        this.removeToastNotification(id);
      }, 4000);
    },
    removeToastNotification(id) {
      const index = this.toastNotifications.findIndex(t => t.id === id);
      if (index > -1) {
        this.toastNotifications.splice(index, 1);
      }
    },

    checkAuth() {
      const token = localStorage.getItem("authToken");
      this.isAuthenticated = !!token;
      this.currentUserId = token ? parseInt(localStorage.getItem("userId")) : null;
      
    },
    async fetchQuestions() {
      this.loading = true;
      try {
        const res = await fetch(`${API_BASE_URL}/forum/questions`);
        const data = await res.json();
        this.questions = data.map((q) => ({ ...q, newAnswer: "", liked: false }));
        // Sort questions by likes in descending order (most liked first)
        this.questions.sort((a, b) => b.likes - a.likes);
        this.filteredQuestions = [...this.questions];
      } catch (err) {
        this.error = "Failed to load questions.";
      } finally {
        this.loading = false;
      }
    },
    applyFilters() {
      this.filteredQuestions = this.questions.filter((q) => {
        const matchSearch =
          !this.searchTerm ||
          q.title.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          q.content.toLowerCase().includes(this.searchTerm.toLowerCase());
        const matchCategory =
          this.filters.category === "all" || q.category === this.filters.category;
        return matchSearch && matchCategory;
      });
    },
    resetFilters() {
      this.searchTerm = "";
      this.filters.category = "all";
      this.filteredQuestions = [...this.questions];
    },
    formatDate(iso) {
      const d = new Date(iso);
      return d.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
    },
    truncateContent(txt, len = 160) {
      return txt.length > len ? txt.slice(0, len) + "..." : txt;
    },
    toggleDiscussion(id) {
      this.expandedQuestion = this.expandedQuestion === id ? null : id;
    },
    handleReplyClick(question) {
      if (!this.isAuthenticated) {
        this.showAuthModal(
          "Reply to this post?",
          "Sign in to join the conversation and share your thoughts."
        );
        return;
      }
      // If logged in, submit the answer
      this.submitAnswerToCard(question);
    },
    async submitAnswerToCard(question) {
      if (!question.newAnswer.trim()) {
        this.showToastNotification(
          "Please write something before submitting your reply.",
          "warning"
        );
        return;
      }
      try {
        const token = localStorage.getItem("authToken");
        const res = await fetch(`${API_BASE_URL}/forum/questions/${question.id}/answers`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ content: question.newAnswer }),
        });
        if (!res.ok) throw new Error("Failed to submit reply");
        const newAnswer = await res.json();
        question.answers.push(newAnswer);
        question.newAnswer = "";
        this.showToastNotification("Reply submitted successfully!", "success");
      } catch (err) {
        this.showToastNotification(
          "Failed to submit reply. Please try again.",
          "error"
        );
      }
    },
    async deleteAnswer(id) {
      if (!confirm("Delete this answer?")) return;
      const token = localStorage.getItem("authToken");
      await fetch(`${API_BASE_URL}/forum/answers/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      this.questions.forEach((q) => {
        q.answers = q.answers.filter((a) => a.id !== id);
      });
      this.showToastNotification("Answer deleted successfully.", "success");
    },
    async toggleQuestionLike(q) {
      // Check if user is authenticated
      if (!this.isAuthenticated) {
        this.showAuthModal(
          "Like this post?",
          "Sign in to show your support and engage with the community."
        );
        return;
      }

      const token = localStorage.getItem("authToken");
      const res = await fetch(`${API_BASE_URL}/forum/questions/${q.id}/like`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const data = await res.json();
        q.liked = data.liked;
        q.likes = data.likes;
        
        // Re-sort questions after like update
        this.questions.sort((a, b) => b.likes - a.likes);
        this.filteredQuestions = [...this.questions];
      }
    },
    async toggleAnswerLike(a) {
      // Check if user is authenticated
      if (!this.isAuthenticated) {
        this.showAuthModal(
          "Like this reply?",
          "Sign in to show your appreciation and interact with others."
        );
        return;
      }

      const token = localStorage.getItem("authToken");
      const res = await fetch(`${API_BASE_URL}/forum/answers/${a.id}/like`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const data = await res.json();
        a.liked = data.liked;
        a.likes = data.likes;
        // Force re-render to update the sorted order
        this.$forceUpdate();
      }
    },
    
    // Helper method to sort answers by likes
    sortedAnswers(answers) {
      return [...answers].sort((a, b) => b.likes - a.likes);
    },

    // Ask Question Modal
    openQuestionModal() {
      this.showQuestionModal = true;
    },
    closeQuestionModal() {
      this.showQuestionModal = false;
      this.newQuestion = { title: "", content: "", category: "general" };
    },
    async submitQuestion() {
      if (!this.newQuestion.title.trim() || !this.newQuestion.content.trim()) {
        this.showToastNotification(
          "Please fill in all fields before submitting your question.",
          "warning"
        );
        return;
      }
      try {
        const token = localStorage.getItem("authToken");
        const res = await fetch(`${API_BASE_URL}/forum/questions`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(this.newQuestion),
        });
        if (!res.ok) throw new Error("Failed to submit question");
        const createdQuestion = await res.json();
        this.questions.unshift(createdQuestion);
        this.filteredQuestions.unshift(createdQuestion);
        this.closeQuestionModal();
        this.showToastNotification("Question posted successfully!", "success");
      } catch (err) {
        this.showToastNotification(
          "Failed to submit question. Please try again.",
          "error"
        );
      }
    },
  },
};
</script>

<style scoped>
/* Toast Notification Styles */
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 10001;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 400px;
}

.toast-notification {
  display: flex;
  align-items: center;
  gap: 12px;
  background: white;
  border-radius: 12px;
  padding: 16px 18px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  border-left: 4px solid;
  min-width: 320px;
  transition: all 0.3s ease;
}

.toast-notification:hover {
  transform: translateX(-4px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.toast-warning {
  border-left-color: #f59e0b;
  background: linear-gradient(to right, #fffbeb, white);
}

.toast-success {
  border-left-color: #10b981;
  background: linear-gradient(to right, #f0fdf4, white);
}

.toast-error {
  border-left-color: #ef4444;
  background: linear-gradient(to right, #fef2f2, white);
}

.toast-info {
  border-left-color: #3b82f6;
  background: linear-gradient(to right, #eff6ff, white);
}

.toast-icon {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.toast-warning .toast-icon {
  color: #f59e0b;
}

.toast-success .toast-icon {
  color: #10b981;
}

.toast-error .toast-icon {
  color: #ef4444;
}

.toast-info .toast-icon {
  color: #3b82f6;
}

.toast-content {
  flex: 1;
}

.toast-message {
  margin: 0;
  font-size: 14px;
  color: #374151;
  line-height: 1.5;
  font-weight: 500;
}

.toast-close {
  flex-shrink: 0;
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  font-size: 20px;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.toast-close:hover {
  background: #f3f4f6;
  color: #6b7280;
}

/* Toast animations */
.toast-enter-active {
  animation: toastSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.toast-leave-active {
  animation: toastSlideOut 0.3s ease;
}

@keyframes toastSlideIn {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes toastSlideOut {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(100%);
  }
}

/* Auth Modal Styles */
.auth-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.65);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 20px;
  backdrop-filter: blur(4px);
}

.auth-modal-content {
  background: white;
  border-radius: 20px;
  padding: 40px 35px;
  max-width: 420px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  position: relative;
  text-align: center;
  animation: modalSlideUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.auth-modal-close {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  font-size: 28px;
  color: #999;
  cursor: pointer;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.auth-modal-close:hover {
  background: #f3f4f6;
  color: #666;
}

.auth-modal-icon {
  width: 70px;
  height: 70px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #ffd4d8 0%, #ffc1cc 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 4px solid #ff6b9a;
}

.auth-modal-icon i {
  font-size: 32px;
  color: #ff6b9a;
}

.auth-modal-title {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 12px;
}

.auth-modal-message {
  font-size: 15px;
  color: #6b7280;
  line-height: 1.6;
  margin-bottom: 30px;
}

.auth-modal-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.btn-auth-primary {
  background: linear-gradient(135deg, #ff7d82 0%, #fa9696 100%);
  color: white;
  border: none;
  padding: 14px 24px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
}

.btn-auth-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 107, 154, 0.35);
  background: linear-gradient(135deg, #eb7e7e 0%, #ff9a9e 100%);
}

.btn-auth-secondary {
  background: white;
  color: #6b7280;
  border: 2px solid #e5e7eb;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
}

.btn-auth-secondary:hover {
  background: #f9fafb;
  border-color: #d1d5db;
  color: #4b5563;
}

@keyframes modalSlideUp {
  from {
    opacity: 0;
    transform: translateY(50px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.fade-enter-active {
  animation: fadeIn 0.3s ease;
}

.fade-leave-active {
  animation: fadeOut 0.25s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fadeOut {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}

@media (max-width: 576px) {
  .auth-modal-content {
    padding: 35px 25px;
    max-width: 90%;
  }
  
  .auth-modal-title {
    font-size: 21px;
  }
  
  .auth-modal-message {
    font-size: 14px;
  }

  .toast-container {
    top: 10px;
    right: 10px;
    left: 10px;
    max-width: none;
  }
  
  .toast-notification {
    min-width: auto;
  }
}

/* Original Styles */
.btn-box {
  background: linear-gradient(135deg, #ff868a 0%, #fa9696 100%);
  color: white;
  border: none !important;
  padding: 12px 25px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-box:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 154, 158, 0.4);
  background: linear-gradient(135deg, #eb7e7e 0%, #ff9a9e 100%);
  color: white;
}

.questions-grid {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.question-card {
  background: #fff;
  border-radius: 14px;
  padding: 1.5rem;
  border: 1px solid #ffe3eb;
  box-shadow: 0 3px 10px rgba(255, 182, 193, 0.15);
  transition: all 0.3s ease;
}

.question-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(255, 182, 193, 0.25);
}

.btn-pink {
  /* background: linear-gradient(135deg, #ff7d82 0%, #fa9696 100%); */
  background-origin: white;
  color: #ff6b9a;
  border:  #ff6b9a solid 1px !important;
  padding: 12px 25px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-pink:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 154, 158, 0.4);
  background: linear-gradient(135deg, #eb7e7e 0%, #ff9a9e 100%);
  color: white;
}

.btn-pink-outline {
  border: 1px solid #ff6b9a;
  color: #ff6b9a;
  background: transparent;
  transition: all 0.2s ease;
}

.btn-pink-outline:hover {
  background: #ff6b9a;
  color: #fff;
}

.discussion-dropdown {
  background: linear-gradient(135deg, #fff8fa, #fff);
  border-radius: 10px;
  padding: 1rem;
  border: 1px solid #ffe1ec;
}

.answer-item {
  background: white;
  border-left: 3px solid #ff6b9a;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.reply-box textarea {
  resize: none;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
}

.modal-container {
  background: white;
  border-radius: 16px;
  max-width: 600px;
  width: 100%;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.3s ease;
}

.modal-header,
.modal-footer {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #dee2e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-body {
  padding: 1.5rem;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #777;
  cursor: pointer;
}

@media (max-width: 768px) {
  .question-card {
    padding: 1rem;
  }
}
</style>
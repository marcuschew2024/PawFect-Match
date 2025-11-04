<template>
  <div class="container my-5">
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
                v-if="isAuthenticated"
                class="btn btn-pink-outline btn-sm"
                @click="submitAnswerToCard(question)"
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

            <button class="btn btn-outline-danger btn-sm" @click="toggleQuestionLike(question)">
              <i :class="question.liked ? 'bi bi-hand-thumbs-up-fill' : 'bi bi-hand-thumbs-up'"></i>
              {{ question.likes }}
            </button>
          </div>

          <!-- Dropdown replies -->
          <transition name="fade">
            <div v-if="expandedQuestion === question.id" class="discussion-dropdown mt-3">
              <div v-if="question.answers.length === 0" class="text-muted small text-center py-3">
                No replies yet. Be the first to respond!
              </div>

              <div v-for="answer in question.answers" :key="answer.id" class="answer-item">
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
                    <button class="btn btn-outline-primary btn-sm" @click="toggleAnswerLike(answer)">
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
    };
  },
  async mounted() {
    this.checkAuth();
    await this.fetchQuestions();
  },
  methods: {
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
    async submitAnswerToCard(question) {
      if (!question.newAnswer.trim()) return alert("Reply cannot be empty.");
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
      } catch (err) {
        alert(err.message);
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
    },
    async toggleQuestionLike(q) {
      const token = localStorage.getItem("authToken");
      const res = await fetch(`${API_BASE_URL}/forum/questions/${q.id}/like`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const data = await res.json();
        q.liked = data.liked;
        q.likes = data.likes;
      }
    },
    async toggleAnswerLike(a) {
      const token = localStorage.getItem("authToken");
      const res = await fetch(`${API_BASE_URL}/forum/answers/${a.id}/like`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const data = await res.json();
        a.liked = data.liked;
        a.likes = data.likes;
      }
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
        alert("All fields are required.");
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
      } catch (err) {
        alert(err.message);
      }
    },
  },
};
</script>

<style scoped>

.btn-box{
    background: linear-gradient(135deg, #ff868a 0%, #fa9696 100%);
  color: white;
  border: none !important;
  padding: 12px 25px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-box:hover{
    transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 154, 158, 0.4);
  background: linear-gradient(135deg, #eb7e7e 0%, #FF9A9E 100%);
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
  background: linear-gradient(135deg, #ff7d82 0%, #fa9696 100%);
  color: white;
  border: none !important;
  padding: 12px 25px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-pink:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 154, 158, 0.4);
  background: linear-gradient(135deg, #eb7e7e 0%, #FF9A9E 100%);
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .question-card {
    padding: 1rem;
  }
}
</style>

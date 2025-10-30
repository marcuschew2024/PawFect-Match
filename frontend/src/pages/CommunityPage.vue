<template>
  <div class="container my-5">
    <h2 class="text-center mb-4">Community Forum</h2>

    <!-- New Question Form -->
    <div v-if="user" class="card mb-4 shadow-sm">
      <div class="card-body">
        <h5 class="card-title">Ask a New Question</h5>
        <div class="mb-3">
          <input
            v-model="newQuestion.title"
            type="text"
            class="form-control"
            placeholder="Enter your question title"
          />
        </div>
        <div class="mb-3">
          <textarea
            v-model="newQuestion.content"
            class="form-control"
            placeholder="Describe your question in detail..."
            rows="4"
          ></textarea>
        </div>
        <div class="mb-3">
          <select v-model="newQuestion.category" class="form-select">
            <option disabled value="">Select Category</option>
            <option value="general">General</option>
            <option value="health">Health</option>
            <option value="training">Training</option>
            <option value="adoption">Adoption</option>
            <option value="nutrition">Nutrition</option>
          </select>
        </div>
        <button @click="createQuestion" class="btn btn-primary" :disabled="posting">
          <span v-if="posting" class="spinner-border spinner-border-sm me-2"></span>
          {{ posting ? 'Posting...' : 'Post Question' }}
        </button>
      </div>
    </div>

    <!-- Login message for non-authenticated users -->
    <div v-else class="alert alert-info text-center">
      Please <router-link to="/login">login</router-link> to ask questions and post answers.
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Loading questions...</p>
    </div>

    <!-- Forum Questions -->
    <div v-else-if="questions.length" class="accordion" id="forumAccordion">
      <div
        class="accordion-item"
        v-for="question in questions"
        :key="question.id"
      >
        <h2 class="accordion-header" :id="'heading' + question.id">
          <button
            class="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            :data-bs-target="'#collapse' + question.id"
            aria-expanded="false"
            :aria-controls="'collapse' + question.id"
          >
            <div class="w-100 d-flex justify-content-between align-items-center">
              <div>
                <strong>{{ question.title }}</strong>
                <span class="badge bg-secondary ms-2">{{ question.category }}</span>
              </div>
              <div>
                <span class="text-muted small">{{ formatDate(question.createdAt || question.created_at) }}</span>
              </div>
            </div>
          </button>
        </h2>

        <div
          :id="'collapse' + question.id"
          class="accordion-collapse collapse"
          :aria-labelledby="'heading' + question.id"
          data-bs-parent="#forumAccordion"
        >
          <div class="accordion-body">
            <p>{{ question.content }}</p>
            <div class="d-flex justify-content-between align-items-center mb-3">
              <button
                class="btn btn-outline-primary btn-sm"
                @click="toggleLikeQuestion(question)"
                :disabled="!user"
              >
                👍 {{ question.likes }}
              </button>
              <span class="text-muted small">
                Asked by {{ question.author || 'Anonymous' }}
              </span>
            </div>

            <!-- Answers Section -->
            <div class="answers">
              <h6>Answers ({{ question.answers ? question.answers.length : 0 }}):</h6>
              <div v-if="question.answers && question.answers.length">
                <div
                  v-for="answer in question.answers"
                  :key="answer.id"
                  class="border rounded p-2 mb-2 bg-light"
                >
                  <p class="mb-1">{{ answer.content }}</p>
                  <div class="d-flex justify-content-between">
                    <button
                      class="btn btn-sm btn-outline-success"
                      @click="likeAnswer(answer)"
                      :disabled="!user"
                    >
                      👍 {{ answer.likes }}
                    </button>
                    <span class="text-muted small">
                      by {{ answer.author || 'Anonymous' }}
                    </span>
                  </div>
                </div>
              </div>
              <p v-else class="text-muted">No answers yet. Be the first to answer!</p>

              <!-- Add Answer Form -->
              <div v-if="user" class="mt-3">
                <textarea
                  v-model="newAnswers[question.id]"
                  class="form-control mb-2"
                  placeholder="Write your answer..."
                  rows="3"
                ></textarea>
                <button
                  @click="addAnswer(question.id)"
                  class="btn btn-sm btn-primary"
                  :disabled="!newAnswers[question.id] || postingAnswer"
                >
                  <span v-if="postingAnswer" class="spinner-border spinner-border-sm me-2"></span>
                  {{ postingAnswer ? 'Posting...' : 'Post Answer' }}
                </button>
              </div>
              <div v-else class="mt-3 text-muted small">
                Please login to answer this question.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <p v-else class="text-center text-muted mt-5">
      No questions yet. Be the first to post!
    </p>
  </div>
</template>

<script>
const API_BASE_URL = 'http://localhost:3000/api';

export default {
  name: "CommunityPage",
  data() {
    return {
      user: null,
      questions: [],
      newQuestion: {
        title: "",
        content: "",
        category: "",
      },
      newAnswers: {},
      loading: false,
      posting: false,
      postingAnswer: false,
    };
  },
  mounted() {
    this.checkAuth();
    this.fetchQuestions();
  },
  methods: {
    checkAuth() {
      // Check if user is logged in
      const token = localStorage.getItem("authToken");
      const userData = localStorage.getItem("user");
      
      if (token && userData) {
        try {
          this.user = JSON.parse(userData);
        } catch (e) {
          console.error("Error parsing user data:", e);
          this.user = null;
        }
      } else {
        this.user = null;
      }
    },

    async fetchQuestions() {
      this.loading = true;
      try {
        const response = await fetch(`${API_BASE_URL}/forum/questions`);
        
        if (response.ok) {
          this.questions = await response.json();
          console.log("Questions loaded:", this.questions);
        } else {
          console.error("Failed to fetch questions:", response.status);
          this.showToast("Failed to load questions", "error");
        }
      } catch (err) {
        console.error("Error fetching questions:", err);
        this.showToast("Network error loading questions", "error");
      } finally {
        this.loading = false;
      }
    },

    async createQuestion() {
      // Validate inputs
      if (!this.newQuestion.title.trim()) {
        this.showToast("Please enter a question title", "error");
        return;
      }
      if (!this.newQuestion.content.trim()) {
        this.showToast("Please enter question details", "error");
        return;
      }
      if (!this.newQuestion.category) {
        this.showToast("Please select a category", "error");
        return;
      }

      this.posting = true;
      try {
        const token = localStorage.getItem("authToken");
        const response = await fetch(`${API_BASE_URL}/forum/questions`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(this.newQuestion)
        });

        if (response.ok) {
          this.newQuestion = { title: "", content: "", category: "" };
          this.showToast("Question posted successfully!", "success");
          await this.fetchQuestions();
        } else {
          const error = await response.json();
          this.showToast(error.error || "Failed to post question", "error");
        }
      } catch (err) {
        console.error("Error creating question:", err);
        this.showToast("Network error posting question", "error");
      } finally {
        this.posting = false;
      }
    },

    async addAnswer(questionId) {
      const content = this.newAnswers[questionId];
      if (!content || !content.trim()) {
        this.showToast("Please enter an answer", "error");
        return;
      }

      this.postingAnswer = true;
      try {
        const token = localStorage.getItem("authToken");
        const response = await fetch(`${API_BASE_URL}/forum/questions/${questionId}/answers`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ content })
        });

        if (response.ok) {
          this.newAnswers[questionId] = "";
          this.showToast("Answer posted successfully!", "success");
          await this.fetchQuestions();
        } else {
          const error = await response.json();
          this.showToast(error.error || "Failed to post answer", "error");
        }
      } catch (err) {
        console.error("Error adding answer:", err);
        this.showToast("Network error posting answer", "error");
      } finally {
        this.postingAnswer = false;
      }
    },

    async toggleLikeQuestion(question) {
      if (!this.user) {
        this.showToast("Please login to like questions", "error");
        return;
      }

      try {
        const token = localStorage.getItem("authToken");
        const response = await fetch(`${API_BASE_URL}/forum/questions/${question.id}/like`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          await this.fetchQuestions();
        } else {
          this.showToast("Failed to like question", "error");
        }
      } catch (err) {
        console.error("Error liking question:", err);
        this.showToast("Network error", "error");
      }
    },

    async likeAnswer(answer) {
      if (!this.user) {
        this.showToast("Please login to like answers", "error");
        return;
      }

      try {
        const token = localStorage.getItem("authToken");
        const response = await fetch(`${API_BASE_URL}/forum/answers/${answer.id}/like`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (response.ok) {
          await this.fetchQuestions();
        } else {
          this.showToast("Failed to like answer", "error");
        }
      } catch (err) {
        console.error("Error liking answer:", err);
        this.showToast("Network error", "error");
      }
    },

    formatDate(date) {
      if (!date) return 'Unknown date';
      const dateObj = new Date(date);
      const now = new Date();
      const diff = now - dateObj;
      
      // Less than 1 hour
      if (diff < 3600000) {
        const minutes = Math.floor(diff / 60000);
        return minutes <= 1 ? 'Just now' : `${minutes} minutes ago`;
      }
      // Less than 24 hours
      if (diff < 86400000) {
        const hours = Math.floor(diff / 3600000);
        return `${hours} hour${hours > 1 ? 's' : ''} ago`;
      }
      // Less than 7 days
      if (diff < 604800000) {
        const days = Math.floor(diff / 86400000);
        return `${days} day${days > 1 ? 's' : ''} ago`;
      }
      // Default to date string
      return dateObj.toLocaleDateString();
    },

    showToast(message, type = 'info') {
      const toast = document.createElement('div');
      toast.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show position-fixed`;
      toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
      toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      `;
      document.body.appendChild(toast);

      setTimeout(() => {
        if (toast.parentNode) {
          toast.parentNode.removeChild(toast);
        }
      }, 5000);
    }
  },
};
</script>

<style scoped>
textarea {
  resize: vertical;
  min-height: 80px;
}

.accordion-button {
  background-color: #f8f9fa;
}

.accordion-button:not(.collapsed) {
  background-color: #e7f1ff;
  color: #0c63e4;
}

.accordion-item {
  border-radius: 10px;
  margin-bottom: 10px;
  border: 1px solid #dee2e6;
}

.card {
  border-radius: 10px;
  border: 1px solid #dee2e6;
}

.btn {
  border-radius: 20px;
}

.btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.answers {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.bg-light {
  background-color: #ffffff !important;
}

.badge {
  font-size: 0.75rem;
  padding: 0.35em 0.65em;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
  border-width: 0.15em;
}
</style>
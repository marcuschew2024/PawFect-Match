<template>
  <div class="container my-5">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="mb-0">Community Forum</h1>
      <div v-if="isAuthenticated" class="d-flex gap-2">
        <button class="btn btn-primary" @click="openQuestionModal">
          <i class="bi bi-pencil-square me-2"></i>Ask a Question
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="filter-section mb-4">
      <div class="row g-3 align-items-end">
        <div class="col-md-6">
          <label for="searchInput" class="form-label">SEARCH QUESTIONS</label>
          <input type="text" class="form-control" id="searchInput" v-model="searchTerm"
                 placeholder="Search by title or content..." autocomplete="off">
        </div>
        <div class="col-md-3">
          <label for="categoryFilter" class="form-label">CATEGORY</label>
          <select class="form-select" id="categoryFilter" v-model="filters.category">
            <option value="all">All Categories</option>
            <option v-for="cat in categories" :key="cat.value" :value="cat.value">
                {{ cat.label }}
            </option>
         </select>
        </div>
        <div class="col-md-3">
          <div class="d-flex gap-2">
            <button class="btn btn-primary flex-fill" @click="applyFilters">
              <i class="bi bi-funnel me-2"></i>APPLY FILTERS
            </button>
            <button class="btn btn-outline-secondary" @click="resetFilters">
              <i class="bi bi-arrow-clockwise"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Questions Grid -->
    <div v-if="loading" class="text-center py-5">
      <i class="bi bi-arrow-repeat spinner me-2"></i>Loading community posts...
    </div>

    <div v-else-if="error" class="text-center text-danger py-5">
      <i class="bi bi-exclamation-triangle display-5"></i>
      <p class="mt-3">{{ error }}</p>
      <button class="btn btn-primary" @click="fetchQuestions">
        Try Again
      </button>
    </div>

    <div v-else-if="filteredQuestions.length === 0" class="text-center py-5 text-muted">
      <i class="bi bi-chat-left-text display-5"></i>
      <p class="mt-3">No discussions found matching your filters.</p>
    </div>

    <div v-else class="row mt-4">
      <div v-for="question in filteredQuestions" :key="question.id" class="col-12 mb-4">
        <div class="card question-card">
          <div class="card-body">
            <h5 class="card-title">{{ question.title }}</h5>
            <p class="card-text text-muted mb-3">{{ truncateContent(question.content) }}</p>

            <div class="d-flex justify-content-between align-items-center">
              <div>
                <small class="text-muted">
                  <i class="bi bi-person-circle me-1"></i>{{ getAuthorName(question) }} • 
                  <i class="bi bi-calendar3 me-1"></i>{{ formatDate(question.createdAt) }}
                </small>
              </div>
              <div>
                <span class="badge bg-light text-dark me-2">{{ getCategoryLabel(question.category) }}</span>
                <span class="badge bg-primary">{{ question.answers?.length || 0 }} Answers</span>
              </div>
            </div>
          </div>
          <div class="card-footer bg-transparent d-flex justify-content-between">
            <div class="d-flex gap-2">
              <button class="btn btn-outline-primary btn-sm" @click="openQuestionDetail(question.id)">
                <i class="bi bi-eye me-1"></i>View Discussion
              </button>
              <button v-if="isAuthenticated" class="btn btn-outline-success btn-sm" 
                      @click="openQuestionDetail(question.id, true)">
                <i class="bi bi-reply me-1"></i>Answer
              </button>
            </div>
            <button class="btn btn-outline-danger btn-sm" @click="toggleQuestionLike(question)">
              <i :class="question.liked ? 'bi bi-hand-thumbs-up-fill' : 'bi bi-hand-thumbs-up'"></i>
              {{ question.likes || 0 }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Question Detail Modal -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h3>{{ selectedQuestion?.title }}</h3>
          <button class="btn-close" @click="closeModal">&times;</button>
        </div>

        <div class="modal-body" v-if="selectedQuestion">
          <div class="mb-3">
            <small class="text-muted">
              <i class="bi bi-person-circle me-1"></i>{{ getAuthorName(selectedQuestion) }} • 
              {{ formatDate(selectedQuestion.createdAt) }}
            </small>
            <span class="badge bg-light text-dark ms-2">{{ getCategoryLabel(selectedQuestion.category) }}</span>
          </div>
          <p class="question-content">{{ selectedQuestion.content }}</p>

          <div class="mt-3">
            <button v-if="isAuthenticated" class="btn btn-success mb-3" @click="showAnswerForm = !showAnswerForm">
              <i class="bi bi-reply me-2"></i>{{ showAnswerForm ? 'Cancel' : 'Answer this Question' }}
            </button>

            <div v-if="showAnswerForm" class="mb-4">
              <textarea class="form-control mb-2" v-model="newAnswerContent" rows="3" placeholder="Write your answer..."></textarea>
              <button class="btn btn-primary" @click="submitAnswer">Submit Answer</button>
            </div>
          </div>

          <hr>

          <h5 class="mb-3">
            <i class="bi bi-chat-left-text me-2"></i>
            Answers ({{ selectedQuestion.answers?.length || 0 }})
          </h5>

          <div v-if="!selectedQuestion.answers || selectedQuestion.answers.length === 0" class="text-muted text-center py-4">
            <i class="bi bi-inbox display-6"></i>
            <p class="mt-2">No answers yet. Be the first to help!</p>
          </div>

          <div class="answers-list" v-else>
            <div v-for="answer in selectedQuestion.answers" :key="answer.id" class="answer-card">
              <div class="d-flex justify-content-between align-items-start">
                <div>
                  <small class="text-muted">
                    <i class="bi bi-person-circle me-1"></i>{{ getAuthorName(answer) }} • 
                    {{ formatDate(answer.createdAt) }}
                  </small>
                </div>
                <div class="d-flex gap-2">
                  <button class="btn btn-outline-danger btn-sm" v-if="answer.author_id === currentUserId"
                          @click="deleteAnswer(answer.id)">
                    Delete
                  </button>
                  <button class="btn btn-outline-primary btn-sm" @click="toggleAnswerLike(answer)">
                    <i :class="answer.liked ? 'bi bi-hand-thumbs-up-fill' : 'bi bi-hand-thumbs-up'"></i>
                    {{ answer.likes || 0 }}
                  </button>
                </div>
              </div>
              <p class="answer-content mt-2">{{ answer.content }}</p>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn btn-secondary" @click="closeModal">Close</button>
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
            <input type="text" class="form-control" v-model="newQuestion.title">
          </div>

          <div class="mb-3">
            <label class="form-label">Category</label>
           <select class="form-select" v-model="newQuestion.category" required>
                <option disabled value="">Select a category</option>
                <option v-for="cat in categories" :key="cat.value" :value="cat.value">
                    {{ cat.label }}
                </option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Content</label>
            <textarea class="form-control" v-model="newQuestion.content" rows="5"></textarea>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn btn-secondary" @click="closeQuestionModal">Cancel</button>
          <button class="btn btn-primary" @click="submitQuestion">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const API_BASE_URL = 'http://localhost:3000/api';

export default {
  name: 'CommunityPage',
  data() {
    return {
      questions: [],
      filteredQuestions: [],
      filters: { category: 'all' },
      categories: [
        { label: 'General', value: 'general' },
        { label: 'Health', value: 'health' },
        { label: 'Training', value: 'training' },
        { label: 'Adoption', value: 'adoption' },
        { label: 'Nutrition', value: 'nutrition' }
      ],
      searchTerm: '',
      loading: true,
      error: null,
      isAuthenticated: false,
      currentUserId: null,
      currentUserName: '',

      // Question detail modal
      showModal: false,
      selectedQuestion: null,
      showAnswerForm: false,
      newAnswerContent: '',

      // Ask question modal
      showQuestionModal: false,
      newQuestion: { title: '', content: '', category: '' }
    };
  },
  async mounted() {
    console.log('=== Forum Page Debug Info ===');
    console.log('LocalStorage keys:', Object.keys(localStorage));
    console.log('authToken:', localStorage.getItem('authToken') ? 'exists' : 'missing');
    console.log('userId:', localStorage.getItem('userId'));
    console.log('Checking for user name in localStorage...');
    ['full_name', 'fullName', 'username', 'userName', 'name', 'email'].forEach(key => {
      const value = localStorage.getItem(key);
      if (value) console.log(`  - ${key}: ${value}`);
    });
    console.log('=============================');
    
    this.checkAuth();
    await this.fetchQuestions();
  },
  methods: {
    async checkAuth() {
      const token = localStorage.getItem('authToken');
      this.isAuthenticated = !!token;
      this.currentUserId = token ? parseInt(localStorage.getItem('userId')) : null;
      
      // Try to get full_name from localStorage
      this.currentUserName = localStorage.getItem('full_name') || 
                            localStorage.getItem('fullName') ||
                            localStorage.getItem('username') || 
                            localStorage.getItem('userName') || 
                            localStorage.getItem('name');
      
      // If no name found in localStorage, fetch from API
      if (!this.currentUserName && this.isAuthenticated) {
        try {
          const response = await fetch(`${API_BASE_URL}/auth/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          
          if (response.ok) {
            const userData = await response.json();
            this.currentUserName = userData.full_name || 'User';
            // Store it for next time
            localStorage.setItem('full_name', userData.full_name);
            console.log('Fetched and stored user name:', this.currentUserName);
          }
        } catch (err) {
          console.error('Failed to fetch user data:', err);
          this.currentUserName = 'You';
        }
      }
      
      if (!this.currentUserName) {
        this.currentUserName = 'You';
      }
      
      console.log('Auth check - User:', this.currentUserName, 'ID:', this.currentUserId);
    },

    // Get author name - your backend returns 'author' field from full_name
    getAuthorName(item) {
      // Your backend already provides 'author' field from users.full_name
      if (item.author && item.author !== 'Anonymous' && item.author !== 'undefined' && item.author !== null) {
        return item.author;
      }
      
      // Check if this is current user (for newly created items before page refresh)
      if (item.author_id === this.currentUserId && this.currentUserName) {
        return this.currentUserName;
      }
      
      return 'Anonymous';
    },

    // Get category label from value
    getCategoryLabel(value) {
      const cat = this.categories.find(c => c.value === value);
      return cat ? cat.label : value;
    },

    // -------------------------------
    // Fetch questions
    // -------------------------------
    async fetchQuestions() {
      this.loading = true;
      this.error = null;

      try {
        const params = new URLSearchParams();
        if (this.filters.category !== 'all') params.append('category', this.filters.category);
        if (this.searchTerm) params.append('search', this.searchTerm);

        const response = await fetch(`${API_BASE_URL}/forum/questions?${params.toString()}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();
        console.log('Fetched questions:', data);
        
        // Log first question structure
        if (data.length > 0) {
          console.log('First question fields:', Object.keys(data[0]));
          console.log('First question:', data[0]);
        }
        
        this.questions = data.map(q => ({ 
          ...q, 
          liked: false,
          answers: q.answers || []
        }));
        this.filteredQuestions = [...this.questions];
      } catch (err) {
        console.error('Error fetching forum questions:', err);
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    },

    applyFilters() {
      this.filteredQuestions = this.questions.filter(q => {
        const matchesSearch = !this.searchTerm ||
          q.title.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
          q.content.toLowerCase().includes(this.searchTerm.toLowerCase());

        const matchesCategory = this.filters.category === 'all' || q.category === this.filters.category;
        return matchesSearch && matchesCategory;
      });
    },

    resetFilters() {
      this.searchTerm = '';
      this.filters.category = 'all';
      this.filteredQuestions = [...this.questions];
    },

    truncateContent(text, length = 120) {
      if (!text) return '';
      return text.length > length ? text.substring(0, length) + '...' : text;
    },

    formatDate(isoString) {
      if (!isoString) return 'Unknown date';
      const date = new Date(isoString);
      return date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
    },

    // -------------------------------
    // Question Detail Modal
    // -------------------------------
    async openQuestionDetail(id, autoOpenAnswer = false) {
      try {
        const question = this.questions.find(q => q.id === id);
        if (question) {
          this.selectedQuestion = { ...question };
        } else {
          const res = await fetch(`${API_BASE_URL}/forum/questions/${id}`);
          if (!res.ok) throw new Error('Failed to fetch question detail');
          this.selectedQuestion = await res.json();
        }
        
        // Ensure answers array exists
        if (!this.selectedQuestion.answers) {
          this.selectedQuestion.answers = [];
        }
        
        this.showModal = true;
        this.showAnswerForm = autoOpenAnswer;
        this.newAnswerContent = '';
      } catch (err) {
        console.error(err);
        alert('Unable to open question.');
      }
    },

    closeModal() {
      this.showModal = false;
      this.selectedQuestion = null;
      this.showAnswerForm = false;
      this.newAnswerContent = '';
    },

    // -------------------------------
    // Answer
    // -------------------------------
    async submitAnswer() {
      if (!this.newAnswerContent.trim()) {
        alert('Answer cannot be empty.');
        return;
      }

      try {
        const token = localStorage.getItem('authToken');
        const res = await fetch(`${API_BASE_URL}/forum/questions/${this.selectedQuestion.id}/answers`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ content: this.newAnswerContent })
        });

        if (!res.ok) {
          const errData = await res.json();
          throw new Error(errData.error || 'Failed to submit answer');
        }

        const newAnswer = await res.json();
        
        // Add current user's name to the answer
        newAnswer.author = this.currentUserName;
        newAnswer.author_id = this.currentUserId;
        
        this.selectedQuestion.answers.push(newAnswer);
        console.log("Answer submitted successfully");

        // Update the question in the main list
        const questionIndex = this.questions.findIndex(q => q.id === this.selectedQuestion.id);
        if (questionIndex >= 0) {
          this.questions[questionIndex].answers = [...this.selectedQuestion.answers];
        }

        this.newAnswerContent = '';
        this.showAnswerForm = false;

      } catch (err) {
        console.error(err);
        alert(err.message);
      }
    },

    async deleteAnswer(answerId) {
      if (!confirm('Are you sure you want to delete this answer?')) return;

      try {
        const token = localStorage.getItem('authToken');
        const res = await fetch(`${API_BASE_URL}/forum/answers/${answerId}`, {
          method: 'DELETE',
          headers: { Authorization: `Bearer ${token}` }
        });

        if (!res.ok) throw new Error('Failed to delete answer');

        // Remove locally
        this.selectedQuestion.answers = this.selectedQuestion.answers.filter(a => a.id !== answerId);
        const questionIndex = this.questions.findIndex(q => q.id === this.selectedQuestion.id);
        if (questionIndex >= 0) {
          this.questions[questionIndex].answers = this.questions[questionIndex].answers.filter(a => a.id !== answerId);
        }
      } catch (err) {
        console.error(err);
        alert(err.message);
      }
    },

    // -------------------------------
    // Like/Unlike Question
    // -------------------------------
    async toggleQuestionLike(question) {
      if (!this.isAuthenticated) {
        alert('Please log in to like questions.');
        return;
      }

      try {
        const token = localStorage.getItem('authToken');
        const res = await fetch(`${API_BASE_URL}/forum/questions/${question.id}/like`, {
          method: 'POST',
          headers: { Authorization: `Bearer ${token}` }
        });

        if (!res.ok) throw new Error('Failed to like/unlike question');

        const data = await res.json();
        question.liked = data.liked;
        question.likes = data.likes;
      } catch (err) {
        console.error(err);
        alert(err.message);
      }
    },

    async toggleAnswerLike(answer) {
      if (!this.isAuthenticated) {
        alert('Please log in to like answers.');
        return;
      }

      try {
        const token = localStorage.getItem('authToken');
        const res = await fetch(`${API_BASE_URL}/forum/answers/${answer.id}/like`, {
          method: 'POST',
          headers: { Authorization: `Bearer ${token}` }
        });

        if (!res.ok) throw new Error('Failed to like/unlike answer');

        const data = await res.json();
        answer.liked = data.liked;
        answer.likes = data.likes;
      } catch (err) {
        console.error(err);
        alert(err.message);
      }
    },

    // -------------------------------
    // Ask Question Modal
    // -------------------------------
    openQuestionModal() { 
      this.showQuestionModal = true;
      this.newQuestion = { title: '', content: '', category: '' };
    },
    
    closeQuestionModal() {
      this.showQuestionModal = false;
      this.newQuestion = { title: '', content: '', category: '' };
    },

    async submitQuestion() {
      if (!this.newQuestion.title.trim() || !this.newQuestion.content.trim() || !this.newQuestion.category) {
        alert('All fields are required.');
        return;
      }

      try {
        const token = localStorage.getItem('authToken');
        const res = await fetch(`${API_BASE_URL}/forum/questions`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(this.newQuestion)
        });

        if (!res.ok) {
          const errData = await res.json();
          throw new Error(errData.error || 'Failed to submit question');
        }

        const createdQuestion = await res.json();
        
        // Add current user's name
        createdQuestion.author = this.currentUserName;
        createdQuestion.author_id = this.currentUserId;
        createdQuestion.answers = [];
        createdQuestion.likes = 0;
        createdQuestion.liked = false;
        
        this.questions.unshift(createdQuestion);
        this.filteredQuestions.unshift(createdQuestion);
        this.closeQuestionModal();
      } catch (err) {
        console.error(err);
        alert(err.message);
      }
    }
  }
};
</script>

<style scoped>
.question-card {
  border: 1px solid var(--border-light);
  border-radius: 12px;
  box-shadow: var(--shadow-medium);
  transition: all 0.3s ease;
  background: var(--background-white);
}
.question-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-heavy);
  border-color: var(--primary-pink);
}
.filter-section {
  background: linear-gradient(135deg, #e6f2ff 0%, #f0f9ff 100%);
  border: 2px solid var(--border-light);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-medium);
}
.spinner {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
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
  animation: fadeIn 0.2s ease;
}
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
.modal-container {
  background: white;
  border-radius: 16px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease;
}
@keyframes slideUp {
  from {
    transform: translateY(30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #dee2e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
}
.btn-close {
  background: none;
  border: none;
  font-size: 2rem;
  line-height: 1;
  color: #999;
  cursor: pointer;
  padding: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.2s;
}
.btn-close:hover {
  background: #f8f9fa;
  color: #333;
}
.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}
.question-detail {
  margin-bottom: 1rem;
}
.question-content {
  font-size: 1.05rem;
  line-height: 1.6;
  color: #555;
  white-space: pre-wrap;
}
.answers-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.answer-card {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  border-left: 3px solid #007bff;
}
.answer-header {
  margin-bottom: 0.5rem;
}
.answer-content {
  margin: 0;
  line-height: 1.5;
  color: #333;
  white-space: pre-wrap;
}
.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #dee2e6;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
@media (max-width: 768px) {
  .modal-container {
    max-height: 95vh;
    margin: 10px;
  }
  .modal-header h3 {
    font-size: 1.25rem;
  }
}
</style>
<!-- <template>
  <div class="question-detail-modal" v-if="visible">
    <div class="modal-backdrop" @click="close"></div>
    <div class="modal-content">
      <h4>{{ question.title }}</h4>
      <p>{{ question.content }}</p>
      <p class="text-muted">Category: {{ question.category }} | Likes: {{ question.likes }}</p>

      <hr />

      <div>
        <h5>Answers</h5>
        <div v-if="answers.length === 0">No answers yet.</div>
        <div v-for="answer in answers" :key="answer.id" class="answer">
          <p>{{ answer.content }}</p>
          <small>By {{ answer.author }} | Likes: {{ answer.likes }}</small>
        </div>
      </div>

      <div v-if="isAuthenticated" class="mt-3">
        <textarea v-model="newAnswer" class="form-control" placeholder="Write your answer..."></textarea>
        <button class="btn btn-primary mt-2" @click="postAnswer">Post Answer</button>
      </div>

      <button class="btn btn-outline-secondary mt-3" @click="close">Close</button>
    </div>
  </div>
</template>

<script>
const API_BASE_URL = 'http://localhost:3000/api';

export default {
  props: {
    questionId: Number,
    isAuthenticated: Boolean
  },
  data() {
    return {
      visible: false,
      question: {},
      answers: [],
      newAnswer: ''
    }
  },
  methods: {
    async open() {
      this.visible = true;
      await this.fetchQuestion();
    },
    close() {
      this.visible = false;
      this.newAnswer = '';
    },
    async fetchQuestion() {
      try {
        const response = await fetch(`${API_BASE_URL}/forum/questions/${this.questionId}`);
        if (!response.ok) throw new Error('Failed to fetch question');
        const data = await response.json();
        this.question = data;
        this.answers = data.answers || [];
      } catch (error) {
        console.error(error);
      }
    },
    async postAnswer() {
      if (!this.newAnswer.trim()) return;
      try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE_URL}/forum/questions/${this.questionId}/answers`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ content: this.newAnswer })
        });
        if (!response.ok) throw new Error('Failed to post answer');
        const answer = await response.json();
        this.answers.push(answer);
        this.newAnswer = '';
      } catch (error) {
        console.error(error);
      }
    }
  }
}
</script>

<style scoped>
.question-detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;
}

.modal-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
}

.modal-content {
  position: relative;
  background: white;
  max-width: 600px;
  margin: 5% auto;
  padding: 2rem;
  border-radius: 12px;
  z-index: 10;
}
.answer {
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}
</style>
 -->

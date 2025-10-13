import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Import Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'

// Import Bootstrap JavaScript
import 'bootstrap'

// Import your custom CSS
import './assets/styling.css'

createApp(App).use(router).mount('#app')
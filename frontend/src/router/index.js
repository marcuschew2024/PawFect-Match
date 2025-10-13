import { createRouter, createWebHistory } from 'vue-router'

// Import all your page components
import HomePage from '../pages/HomePage.vue'
import PetListingPage from '../pages/PetListingPage.vue'
import AboutPage from '../pages/AboutPage.vue'
import AddAdoptionPage from '../pages/AddAdoptionPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/pets',
    name: 'Pets',
    component: PetListingPage
  },
  {
    path: '/about',
    name: 'About',
    component: AboutPage
  },
  {
    path: '/add-adoption',
    name: 'AddAdoption',
    component: AddAdoptionPage
  },
  // Redirect any unknown routes to home
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
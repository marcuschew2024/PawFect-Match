import { createRouter, createWebHistory } from 'vue-router'

// Import all your page components
import HomePage from '../pages/HomePage.vue'
import PetListingPage from '../pages/PetListingPage.vue'
import AboutPage from '../pages/AboutPage.vue'
import AddPetPage from '../pages/AddPetPage.vue'  // Changed from AddAdoptionPage
import LoginPage from '../pages/LoginPage.vue'
import SignUpPage from '../pages/SignUpPage.vue'
import LifestyleQuiz from '../pages/LifestyleQuiz.vue'
import FavoritesPage from '../pages/FavoritesPage.vue'
import ProfilePage from '../pages/ProfilePage.vue'
import AdoptionFormPage from '../pages/AdoptionFormPage.vue'
import CommunityPage from '../pages/CommunityPage.vue' 

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
    // No meta - public access
  },
  {
    path: '/about',
    name: 'About',
    component: AboutPage
    // No meta - public access
  },
   {
    path: '/community', 
    name: 'Community',
    component: CommunityPage
    // No meta - public access

  },
  {
    path: '/community', 
    name: 'Community',
    component: CommunityPage
    // No meta - public access

  },
  {
    path: '/add-pet',  // Changed from /add-adoption
    name: 'AddPet',    // Changed from AddAdoption
    component: AddPetPage,
    meta: { requiresAuth: true } // 🔒 PROTECTED
  },
  {
    path: '/quiz',
    name: 'Quiz',
    component: LifestyleQuiz,
    meta: { requiresAuth: true } // 🔒 PROTECTED
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: FavoritesPage,
    meta: { requiresAuth: true } // 🔒 PROTECTED
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfilePage,
    meta: { requiresAuth: true } // 🔒 PROTECTED
  },
  {
    path: '/adopt/:petId',
    name: 'AdoptionForm',
    component: AdoptionFormPage,
    meta: { requiresAuth: true } // 🔒 PROTECTED
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
    meta: { requiresGuest: true } // Redirects if already logged in
  },
  {
    path: '/signup',
    name: 'SignUp',
    component: SignUpPage,
    meta: { requiresGuest: true } // Redirects if already logged in
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  },
  {
    path: '/pet/:petId',
    name: 'PetProfile',
    component: () => import('@/views/PetProfile.vue'),
    props: true
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard - enforces authentication
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('authToken');
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Redirect to login if trying to access protected routes without auth
    next('/login');
  } else if (to.meta.requiresGuest && isAuthenticated) {
    // Redirect to pets if trying to access login/signup while already logged in
    next('/pets');
  } else {
    // Allow access
    next();
  }
})

export default router
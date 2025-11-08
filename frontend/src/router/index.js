import { createRouter, createWebHistory } from 'vue-router'

// Import all your page components
import HomePage from '../pages/HomePage.vue'
import PetListingPage from '../pages/PetListingPage.vue'
import AboutPage from '../pages/AboutPage.vue'
import AddPetPage from '../pages/AddPetPage.vue'
import LoginPage from '../pages/LoginPage.vue'
import SignUpPage from '../pages/SignUpPage.vue'
import LifestyleQuiz from '../pages/LifestyleQuiz.vue'
import FavoritesPage from '../pages/FavoritesPage.vue'
import ProfilePage from '../pages/ProfilePage.vue'
import AdoptionFormPage from '../pages/AdoptionFormPage.vue'
import CommunityPage from '../pages/CommunityPage.vue'
import AdminDashboard from '../pages/AdminDashboard.vue'

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
    path: '/community', 
    name: 'Community',
    component: CommunityPage
  },
  {
    path: '/add-pet',
    name: 'AddPet',
    component: AddPetPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/quiz',
    name: 'Quiz',
    component: LifestyleQuiz,
    meta: { requiresAuth: true }
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: FavoritesPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfilePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/adopt/:petId',
    name: 'AdoptionForm',
    component: AdoptionFormPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
    meta: { requiresGuest: true }
  },
  {
    path: '/signup',
    name: 'SignUp',
    component: SignUpPage,
    meta: { requiresGuest: true }
  },
  {
    path: '/pet/:petId',
    name: 'PetProfile',
    component: () => import('@/views/PetProfile.vue'),
    props: true
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Enhanced navigation guard with admin check
router.beforeEach(async (to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('authToken');
  
  // Check if user is admin
  let isAdmin = false;
  let user = null;
  
  if (isAuthenticated) {
    try {
      user = JSON.parse(localStorage.getItem('user') || '{}');
      isAdmin = user.is_admin === true;
      console.log('User admin status:', { isAdmin, user });
    } catch (error) {
      console.error('Error checking admin status:', error);
    }
  }
  
  // Route protection logic
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Redirect to login if trying to access protected routes without auth
    next('/login');
  } else if (to.meta.requiresGuest && isAuthenticated) {
    // Redirect to home if trying to access login/signup while already logged in
    next('/');
  } else if (to.meta.requiresAdmin) {
    if (!isAuthenticated) {
      // Redirect to login if not authenticated
      next('/login');
    } else if (!isAdmin) {
      // Show access denied for non-admin users
      console.warn('Non-admin user attempted to access admin route:', user);
      alert('Access denied. Admin privileges required.');
      next('/');
    } else {
      // Allow admin access
      next();
    }
  } else {
    // Allow access to public routes
    next();
  }
})

export default router
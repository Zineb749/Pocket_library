// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'

// Importer les composants/pages
import Home from '../components/Home.vue'
import BooksList from '../components/BooksList.vue'
import GoogleBooksSearch from '../components/GoogleBooksSearch.vue' // ✅ ajout

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/books',
    name: 'BooksList',
    component: BooksList,
  },
  {
    path: '/google-books',
    name: 'GoogleBooksSearch',
    component: GoogleBooksSearch, // ✅ nouvelle route
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

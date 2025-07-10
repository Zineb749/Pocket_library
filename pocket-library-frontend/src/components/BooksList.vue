<template>
  <div>
    <h1>Liste des livres</h1>

    <!-- Filtres -->
    <div style="margin-bottom: 20px;">
      <input
        type="text"
        v-model="searchTitle"
        placeholder="Rechercher par titre"
      />
      <input
        type="text"
        v-model="searchAuthor"
        placeholder="Rechercher par auteur"
      />
      <select v-model="filterStatus" @change="fetchBooksDebounced">
        <option value="">Tous</option>
        <option value="a_lire">À lire</option>
        <option value="en_cours">En cours</option>
        <option value="lu">Lu</option>
      </select>
      <button @click="resetSearch">Réinitialiser</button>
    </div>

    <!-- Liste des livres -->
    <ul>
      <li v-for="book in books" :key="book.id" style="margin-bottom: 20px;">
        <h3>{{ book.title }}</h3>
        <p>Auteur : {{ book.author }}</p>
        <p>Status : <strong>{{ statusLabel(book.status) }}</strong></p>
        <img
          v-if="book.cover_url"
          :src="book.cover_url"
          alt="Couverture"
          style="max-width: 100px;"
        />
        <div>
          <label for="statusSelect">Changer le statut:</label>
          <select
            :id="'statusSelect-' + book.id"
            v-model="book.status"
            @change="updateBookStatus(book)"
          >
            <option value="a_lire">À lire</option>
            <option value="en_cours">En cours</option>
            <option value="lu">Lu</option>
          </select>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import api from '../services/api.js'

export default {
  data() {
    return {
      books: [],
      searchTitle: '',
      searchAuthor: '',
      filterStatus: '',
      searchTimeout: null,
    }
  },
  methods: {
    async fetchBooks(params = {}) {
      try {
        const response = await api.get('/books', { params })
        this.books = response.data
      } catch (error) {
        console.error('Erreur lors de la récupération des livres:', error)
      }
    },
    fetchBooksDebounced() {
      if (this.searchTimeout) clearTimeout(this.searchTimeout)
      this.searchTimeout = setTimeout(() => {
        const params = {}
        if (this.searchTitle) params.title = this.searchTitle
        if (this.searchAuthor) params.author = this.searchAuthor
        if (this.filterStatus) params.status = this.filterStatus
        this.fetchBooks(params)
      }, 300)
    },
    resetSearch() {
      this.searchTitle = ''
      this.searchAuthor = ''
      this.filterStatus = ''
      this.fetchBooks()
    },
    statusLabel(status) {
      const labels = {
        a_lire: "À lire",
        en_cours: "En cours",
        lu: "Lu"
      }
      return labels[status] || status
    },
    async updateBookStatus(book) {
      try {
        // Appel PATCH ou PUT pour mettre à jour uniquement le statut
        // Ici on fait un PUT complet (à adapter selon ton API)
        await api.put(`/books/${book.id}`, {
          ...book,
        })
        // Tu peux afficher un message de succès si tu veux
      } catch (error) {
        console.error("Erreur lors de la mise à jour du statut :", error)
      }
    }
  },
  watch: {
    searchTitle() {
      this.fetchBooksDebounced()
    },
    searchAuthor() {
      this.fetchBooksDebounced()
    },
    filterStatus() {
      this.fetchBooksDebounced()
    }
  },
  mounted() {
    this.fetchBooks()
  }
}
</script>

<template>
  <div>
    <input 
      v-model="query" 
      placeholder="Recherche"
      @input="onSearch"
      type="text" 
    />

    <!-- Affichage si pas de résultat -->
    <div v-if="query && !searchResults.length && !isLoading">
      <p>Aucun résultat trouvé pour "{{ query }}"</p>
    </div>

    <!-- Affichage de la liste -->
    <ul v-if="searchResults.length">
      <li v-for="book in searchResults" :key="book.title + book.author">
        <h4>{{ book.title }}</h4>
        <p>Auteur : {{ book.author }}</p>
        <img 
          v-if="book.cover_url" 
          :src="book.cover_url" 
          alt="Couverture" 
          style="max-width: 80px;"
        >
        
        <select v-model="book.status">
          <option value="a_lire">À lire</option>
          <option value="en_cours">En cours</option>
          <option value="lu">Lu</option>
        </select>

        <button @click="addBook(book)">Ajouter à Mes livres</button>
      </li>
    </ul>

    <!-- Décommenter pour voir le JSON brut -->
    <!-- <pre>{{ searchResults }}</pre> -->
  </div>
</template>

<script>
import api from '../services/api.js'
import debounce from 'lodash.debounce'

export default {
  data() {
    return {
      query: '',
      searchResults: [],
      isLoading: false
    }
  },
  methods: {
    onSearch: debounce(async function () {
      if (!this.query) {
        this.searchResults = []
        return
      }

      this.isLoading = true

      try {
        const res = await api.get('/books/import-google-books/', {
          params: { query: this.query }
        })

        console.log('Résultats API:', res.data) // 🔍 Pour debug

        this.searchResults = res.data.map(book => ({
          ...book,
          status: 'a_lire'
        }))
      } catch (e) {
        console.error('Erreur recherche :', e)
      } finally {
        this.isLoading = false
      }
    }, 500),

    async addBook(book) {
      try {
        const payload = {
          title: book.title,
          author: book.author,
          description: book.description,
          purchase_date: book.purchase_date,
          cover_url: book.cover_url,
          status: book.status,
          source: 'google_books'
        }

        await api.post('/books/', payload)
        alert('Livre ajouté à Mes livres !')
      } catch (e) {
        console.error('Erreur ajout livre :', e)
      }
    }
  }
}
</script>

<style scoped>
input {
  padding: 8px;
  margin-bottom: 16px;
  width: 100%;
  max-width: 400px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin-bottom: 20px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 16px;
}
</style>

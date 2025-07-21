<template>
  <div class="books-container">
    <h2 class="title">📚 Ma bibliothèque</h2>

    <div class="filters">
      <input v-model="searchTitle" placeholder="🔍 Titre…" />
      <input v-model="searchAuthor" placeholder="✍️ Auteur…" />
      <select v-model="filterStatus">
        <option value="">Tous</option>
        <option value="a_lire">À lire</option>
        <option value="en_cours">En cours</option>
        <option value="lu">Lu</option>
      </select>
      <button @click="resetSearch">Réinitialiser</button>
    </div>

    <div v-if="filteredBooks.length" class="book-grid">
      <div v-for="book in filteredBooks" :key="book.userbook_id" class="book-card">
        <img v-if="book.cover_url" :src="book.cover_url" alt="Couverture" />
        <div class="book-info">
          <h3>{{ book.title }}</h3>
          <p><strong>Auteur :</strong> {{ book.author }}</p>
          <select v-model="book.status" @change="updateBookStatus(book)">
            <option value="a_lire">À lire</option>
            <option value="en_cours">En cours</option>
            <option value="lu">Lu</option>
          </select>
        </div>

        <div v-if="book.reviews?.length" class="review-block">
          <h4 class="review-title">💬 Avis des lecteurs :</h4>
          <ul>
            <li v-for="(review, index) in book.reviews" :key="index">
              <strong>{{ review.user_name }}</strong> : {{ review.comment || '—' }} ({{ review.rating }}⭐)
            </li>
          </ul>
        </div>
      </div>
    </div>

    <p v-else class="no-result">Aucun livre trouvé dans ta bibliothèque 📭</p>
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
      filterStatus: ''
    }
  },
  computed: {
    filteredBooks() {
      return this.books.filter(book => {
        const matchTitle = book.title.toLowerCase().includes(this.searchTitle.toLowerCase())
        const matchAuthor = book.author.toLowerCase().includes(this.searchAuthor.toLowerCase())
        const matchStatus = this.filterStatus ? book.status === this.filterStatus : true
        return matchTitle && matchAuthor && matchStatus
      })
    }
  },
  methods: {
    async fetchBooks() {
      try {
        const response = await api.get('/userbooks/me')

        const enrichedBooks = await Promise.all(
          response.data.map(async (item) => {
            const bookId = item.book.id
            let reviews = []

            try {
              const r = await api.get(`/reviews/book/${bookId}`)
              reviews = r.data
            } catch {
              reviews = []
            }

            return {
              userbook_id: item.id,
              id: bookId,
              title: item.book.title,
              author: item.book.author,
              cover_url: item.book.cover_url,
              status: item.status,
              reviews
            }
          })
        )

        this.books = enrichedBooks
      } catch (error) {
        console.error('Erreur lors de la récupération des livres:', error)
      }
    },
    resetSearch() {
      this.searchTitle = ''
      this.searchAuthor = ''
      this.filterStatus = ''
    },
    async updateBookStatus(book) {
      try {
        await api.patch(`/userbooks/${book.userbook_id}`, { status: book.status })
      } catch (error) {
        console.error('Erreur lors de la mise à jour du statut :', error)
      }
    }
  },
  mounted() {
    this.fetchBooks()
    if (this.$bus) {
      this.$bus.on('book-added', this.fetchBooks)
    }
  },
  beforeUnmount() {
    if (this.$bus) {
      this.$bus.off('book-added', this.fetchBooks)
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Trocchi&family=Oswald:wght@500&display=swap');

.books-container {
  max-width: 900px;
  margin: 5rem auto;
  padding: 2.5rem 2rem;
  background-color: #ffffff;
  border: 2px solid #99775C;
  border-radius: 12px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08);
  color: #3e2f23;
  font-family: Georgia, serif;
}

.title {
  text-align: center;
  margin-bottom: 2rem;
  font-family: 'Trocchi', serif;
  color: #99775C;
  font-size: 1.9rem;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
}

.filters input,
.filters select {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #cbb6a2;
  border-radius: 6px;
  background-color: #FAF5E9;
  color: #3e2f23;
  font-family: Georgia, serif;
  font-size: 0.95rem;
}

.filters input::placeholder {
  color: #a08978;
}

.filters button {
  padding: 0.75rem 1.2rem;
  background-color: #99775C;
  color: #FAF5E9;
  border: none;
  border-radius: 6px;
  font-family: 'Oswald', sans-serif;
  text-transform: uppercase;
  font-size: 0.95rem;
  letter-spacing: 1px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.filters button:hover {
  background-color: #7a5c46;
  transform: translateY(-2px);
}

.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 2rem;
}

.book-card {
  background-color: #FAF5E9;
  border: 1px solid #cbb6a2;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  font-family: Georgia, serif;
  color: #3e2f23;
  box-shadow: 0 6px 14px rgba(0,0,0,0.05);
}

.book-card img {
  max-height: 160px;
  margin-bottom: 1rem;
  border-radius: 6px;
}

.book-info h3 {
  font-size: 1.05rem;
  margin-bottom: 0.5rem;
  color: #3e2f23;
}

.book-info select {
  margin-top: 0.5rem;
  padding: 0.45rem;
  border: 1px solid #cbb6a2;
  border-radius: 6px;
  background-color: #ffffff;
  font-family: Georgia, serif;
  color: #3e2f23;
}

.review-block {
  margin-top: 1rem;
  background-color: #fffdf7;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid #e3d3c2;
  font-size: 0.9rem;
  font-family: Georgia, serif;
  text-align: left;
}

.review-title {
  margin-bottom: 0.5rem;
  color: #99775C;
  font-weight: bold;
}

.review-block ul {
  padding-left: 1rem;
  list-style: disc;
}

.review-block li {
  margin-bottom: 0.3rem;
}

.no-result {
  margin-top: 3rem;
  text-align: center;
  font-style: italic;
  color: #99775C;
}
</style>

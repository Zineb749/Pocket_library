<template>
  <div class="search-container">
    <div class="search-card">
      <h1 class="title">🔍 Recherche</h1>
      <p class="tagline">Ajoutez des livres et découvrez les avis des lecteurs</p>

      <input
        v-model="query"
        @input="onSearch"
        placeholder="Titre, auteur, mot-clé…"
        class="search-input"
        type="text"
      />

      <p v-if="query && !searchResults.length && !isLoading" class="no-result">
        Aucun résultat trouvé pour "{{ query }}"
      </p>

      <div class="results">
        <div class="book-card" v-for="book in searchResults" :key="book.title + book.author">
          <img v-if="book.cover_url" :src="book.cover_url" alt="Couverture" />
          <h3>{{ book.title }}</h3>
          <p><strong>Auteur :</strong> {{ book.author }}</p>

          <select v-model="book.status">
            <option value="a_lire">À lire</option>
            <option value="en_cours">En cours</option>
            <option value="lu">Lu</option>
          </select>

          <button @click="addBook(book)" class="btn-cta">📥 Ajouter à ma bibliothèque</button>

          <div v-if="book.reviews?.length" class="review-block">
            <h4 class="review-title">💬 Avis des lecteurs :</h4>
            <ul>
              <li v-for="(review, index) in book.reviews" :key="index">
                <strong>{{ review.user_name }}</strong> : {{ review.comment || '—' }} ({{ review.rating }}⭐)
              </li>
            </ul>
          </div>

          <form @submit.prevent="submitReview(book)" class="review-form">
            <h4>Laisser un avis</h4>
            <StarInput v-model:rating="book.newRating" />
            <p v-if="book.newRating > 0" class="rating-text">
              Note : {{ book.newRating }}/5
            </p>
            <textarea
              v-model="book.newComment"
              rows="2"
              placeholder="Votre commentaire…"
            ></textarea>
            <button type="submit" class="btn-cta">📝 Envoyer</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import api from '../services/api.js'
import debounce from 'lodash.debounce'
import StarInput from './StarInput.vue'

export default {
  components: { StarInput },
  data() {
    return {
      query: '',
      searchResults: [],
      isLoading: false
    }
  },
  mounted() {
    const lastQuery = localStorage.getItem('lastGoogleSearch')
    if (lastQuery) {
      this.query = lastQuery
      this.onSearch()
    }
  },
  methods: {
    onSearch: debounce(async function () {
      if (!this.query) {
        this.searchResults = []
        return
      }

      this.isLoading = true
      localStorage.setItem('lastGoogleSearch', this.query)

      try {
        const res = await api.get('/books/import-google-books/', {
          params: { query: this.query },
        })

        this.searchResults = await Promise.all(
          res.data.map(async (book) => {
            let reviews = []
            if (book.id) {
              try {
                const r = await api.get(`/reviews/book/${book.id}`)
                reviews = r.data
              } catch (e) {
                reviews = []
              }
            }

            return {
              ...book,
              status: 'a_lire',
              newRating: 0,
              newComment: '',
              reviews
            }
          })
        )
      } catch (e) {
        console.error('Erreur recherche :', e)
      } finally {
        this.isLoading = false
      }
    }, 500),

    async addBook(book) {
      try {
        const created = await api.post('/books/', {
          title: book.title,
          author: book.author,
          description: book.description,
          purchase_date: book.purchase_date,
          cover_url: book.cover_url,
          status: book.status,
          source: 'google_books'
        })

        await api.post('/userbooks/me', {
          book_id: created.data.id,
          status: book.status || 'a_lire'
        })

        book.id = created.data.id

        alert('✅ Livre ajouté à ta bibliothèque !')
        if (this.$bus) {
          this.$bus.emit('book-added')
        }
      } catch (e) {
        console.error('Erreur ajout livre :', e)
        alert('❌ Échec de l’ajout du livre.')
      }
    },

    async submitReview(book) {
      if (!book.id || !book.newRating) {
        alert("⚠️ Ajoute le livre et choisis une note avant d'envoyer ton avis.")
        return
      }

      try {
        await api.post('/reviews/', {
          book_id: book.id,
          rating: book.newRating,
          comment: book.newComment || null
        })

        const res = await api.get(`/reviews/book/${book.id}`)
        book.reviews = res.data

        alert('✅ Avis enregistré !')
        book.newRating = 0
        book.newComment = ''
      } catch (error) {
        console.error('Erreur envoi avis :', error)
        alert('❌ Impossible d’enregistrer l’avis.')
      }
    }
  }
}
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Trocchi&family=Oswald:wght@500&display=swap');

.search-container {
  background-color: #EAE7DD;
  min-height: calc(100vh - 80px);
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 3rem 1.5rem;
}

.search-card {
  background-color: #ffffff;
  padding: 2.5rem;
  border-radius: 14px;
  max-width: 850px;
  width: 100%;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.08);
  border: 2px solid #99775C;
  font-family: Georgia, serif;
}

.title {
  font-family: 'Trocchi', serif;
  font-size: 2rem;
  color: #99775C;
  margin-bottom: 0.5rem;
  text-align: center;
}

.tagline {
  font-family: 'Oswald', sans-serif;
  font-size: 1.1rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #7a5c46;
  margin-bottom: 2rem;
  text-align: center;
}

.search-input {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border-radius: 8px;
  border: 1px solid #cbb6a2;
  background-color: #FAF5E9;
  margin-bottom: 2rem;
  font-family: Georgia, serif;
  color: #3e2f23;
}

.results {
  display: grid;
  gap: 2rem;
}

.book-card {
  background-color: #FAF5E9;
  border: 1px solid #cbb6a2;
  border-radius: 12px;
  padding: 1.4rem;
  box-shadow: 0 6px 14px rgba(0,0,0,0.05);
}

.book-card img {
  max-height: 160px;
  margin-bottom: 1rem;
  border-radius: 6px;
}

.book-card h3 {
  font-family: 'Trocchi', serif;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.book-card p {
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
}

.book-card select {
  margin-bottom: 1rem;
  width: 100%;
  padding: 0.5rem;
  font-family: Georgia, serif;
  background-color: #ffffff;
  border: 1px solid #cbb6a2;
  border-radius: 6px;
}

.btn-cta {
  background-color: #99775C;
  color: #FAF5E9;
  padding: 0.7rem 1.2rem;
  border-radius: 6px;
  font-family: 'Oswald', sans-serif;
  text-transform: uppercase;
  font-weight: bold;
  font-size: 0.95rem;
  border: none;
  width: 100%;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  margin-top: 0.5rem;
}

.btn-cta:hover {
  background-color: #7a5c46;
  transform: translateY(-2px);
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

.review-form {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #ddd3c2;
}

.review-form textarea {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #cbb6a2;
  border-radius: 8px;
  font-family: Georgia, serif;
  font-size: 0.95rem;
  background-color: #FAF5E9;
  margin-top: 0.5rem;
  resize: vertical;
}

.rating-text {
  font-size: 0.85rem;
  font-family: 'Oswald', sans-serif;
  color: #7a5c46;
  margin-top: 0.3rem;
}

.no-result {
  margin-top: 1.5rem;
  font-style: italic;
  text-align: center;
  color: #99775C;
}
</style>

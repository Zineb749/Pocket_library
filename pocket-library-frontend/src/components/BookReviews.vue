<template>
  <div class="review-card">
    <h2 class="section-title">Avis des lecteurs</h2>

    <div v-if="reviews.length === 0" class="no-review">
      Aucun avis pour ce livre pour le moment.
    </div>

    <div v-else class="review-list">
      <div v-for="review in reviews" :key="review.id" class="review-item">
        <div class="review-header">
          <span class="review-author">{{ review.user_name }}</span>
          <StarDisplay :rating="review.rating" />
        </div>
        <p class="review-comment">“{{ review.comment }}”</p>
      </div>
    </div>

    <!-- Formulaire pour laisser un avis -->
    <form @submit.prevent="submitReview" class="review-form">
      <h3 class="form-title">Laisser un avis</h3>

      <div class="form-group">
        <label>Note :</label>
        <StarInput v-model:rating="newReview.rating" />
        <p v-if="newReview.rating > 0" class="rating-text">
          Note sélectionnée : {{ newReview.rating }}/5
        </p>
      </div>

      <div class="form-group">
        <label for="comment">Commentaire :</label>
        <textarea
          v-model="newReview.comment"
          rows="3"
          placeholder="Partagez votre avis..."
          required
        ></textarea>
      </div>

      <button type="submit" class="btn-cta">Envoyer l’avis</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

// ✅ Imports locaux du même dossier
import StarDisplay from './StarDisplay.vue'
import StarInput from './StarInput.vue'

const route = useRoute()
const bookId = route.params.id

const reviews = ref([])

const newReview = ref({
  rating: 0,
  comment: '',
  book_id: bookId,
  user_id: 1 // 🔐 À connecter dynamiquement plus tard
})

onMounted(async () => {
  try {
    const res = await axios.get(`http://localhost:8000/reviews/book/${bookId}`)
    reviews.value = res.data
  } catch (error) {
    console.error("Erreur chargement avis :", error)
  }
})

const submitReview = async () => {
  try {
    const res = await axios.post('http://localhost:8000/reviews/', newReview.value)
    reviews.value.push(res.data)
    newReview.value.rating = 0
    newReview.value.comment = ''
  } catch (error) {
    console.error("Erreur envoi avis :", error)
  }
}
</script>

<style scoped>
.review-card {
  background-color: #ffffff;
  padding: 2.5rem;
  border-radius: 14px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08);
  border: 2px solid #99775C;
  max-width: 650px;
  margin: 2rem auto;
}

.section-title {
  font-family: 'Trocchi', serif;
  font-size: 1.8rem;
  color: #99775C;
  margin-bottom: 1.5rem;
  text-align: center;
}

.no-review {
  font-family: Georgia, serif;
  font-size: 1rem;
  color: #7a5c46;
  text-align: center;
  margin-top: 1rem;
}

.review-list {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.review-item {
  background-color: #FAF5E9;
  border: 1px solid #ddd3c2;
  border-radius: 10px;
  padding: 1rem 1.2rem;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.6rem;
}

.review-author {
  font-family: 'Oswald', sans-serif;
  font-size: 1rem;
  color: #7a5c46;
  text-transform: uppercase;
  font-weight: 600;
}

.review-comment {
  font-family: Georgia, serif;
  font-size: 0.95rem;
  color: #3e2f23;
  line-height: 1.4;
}

.review-form {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #ddd3c2;
}

.form-title {
  font-family: 'Oswald', sans-serif;
  font-size: 1.2rem;
  color: #99775C;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.3rem;
  color: #3e2f23;
}

.rating-text {
  font-size: 0.95rem;
  color: #7a5c46;
  font-family: 'Oswald', sans-serif;
  margin-top: 0.3rem;
}

textarea {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ddd3c2;
  border-radius: 8px;
  font-family: Georgia, serif;
  font-size: 1rem;
  color: #3e2f23;
  background-color: #FAF5E9;
  resize: vertical;
}
</style>

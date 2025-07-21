<template>
  <div class="test-stars">
    <h2>Test des étoiles cliquables</h2>
    <StarInput v-model:rating="rating" />
    <p v-if="rating > 0">Vous avez sélectionné : {{ rating }} étoile{{ rating > 1 ? 's' : '' }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import StarInput from '../components/StarInput.vue' // adapte le chemin si nécessaire

const rating = ref(0)
</script>

<style scoped>
.test-stars {
  max-width: 400px;
  margin: 2rem auto;
  padding: 1rem;
  background: #f9f5f0;
  border: 1px solid #ddd3c2;
  border-radius: 10px;
  text-align: center;
  font-family: Georgia, serif;
}

h2 {
  color: #7a5c46;
  margin-bottom: 1rem;
}
</style>

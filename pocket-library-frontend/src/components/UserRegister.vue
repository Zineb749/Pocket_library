<template>
  <div class="form-container">
    <h2>Créer un compte</h2>
    <form @submit.prevent="registerUser">
      <input v-model="username" placeholder="Nom d'utilisateur" required />
      <input v-model="password" type="password" placeholder="Mot de passe" required />
      <button type="submit" :disabled="loading">
        {{ loading ? 'Enregistrement...' : 'Créer un compte' }}
      </button>
    </form>

    <p v-if="successMessage" class="success">{{ successMessage }}</p>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import api from '../services/api.js'

export default {
  data() {
    return {
      username: '',
      password: '',
      loading: false,
      errorMessage: '',
      successMessage: '',
    }
  },
  methods: {
    async registerUser() {
      this.loading = true
      this.errorMessage = ''
      this.successMessage = ''

      try {
        const response = await api.post('/users/', {
          username: this.username,
          password: this.password
        })
        this.successMessage = `Utilisateur "${response.data.username}" créé avec succès !`
        this.username = ''
        this.password = ''
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || "Erreur lors de la création du compte."
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Trocchi&family=Oswald:wght@500&display=swap');

.form-container {
  max-width: 420px;
  margin: 5rem auto;
  padding: 2.5rem 2rem;
  background-color: #ffffff;
  border: 2px solid #99775C;
  border-radius: 12px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.1);
  color: #3e2f23;
  font-family: Georgia, serif;
}

h2 {
  text-align: center;
  margin-bottom: 2rem;
  font-family: 'Trocchi', serif;
  font-size: 1.8rem;
  color: #99775C;
}

input {
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1.2rem;
  border: 1px solid #cbb6a2;
  border-radius: 6px;
  background-color: #FAF5E9;
  color: #3e2f23;
  font-family: Georgia, serif;
  font-size: 0.95rem;
  transition: border-color 0.3s ease;
}

input::placeholder {
  color: #a08978;
}

input:focus {
  outline: none;
  border-color: #99775C;
}

button {
  width: 100%;
  padding: 0.75rem;
  background-color: #99775C;
  color: #FAF5E9;
  border: none;
  border-radius: 6px;
  font-family: 'Oswald', sans-serif;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-size: 0.95rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

button:hover {
  background-color: #7a5c46;
  transform: translateY(-2px);
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.success {
  color: #2e7d32;
  margin-top: 1.2rem;
  text-align: center;
  font-weight: bold;
}

.error {
  color: #c0392b;
  margin-top: 1.2rem;
  text-align: center;
  font-weight: bold;
}
</style>

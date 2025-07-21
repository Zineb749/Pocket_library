<template>
  <div class="form-container">
    <h2>Se connecter</h2>
    <form @submit.prevent="submitLogin">
      <input v-model="username" placeholder="Nom d'utilisateur" required />
      <input v-model="password" type="password" placeholder="Mot de passe" required />
      <button type="submit">Connexion</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  data() {
    return {
      username: '',
      password: '',
      error: null,
    }
  },
  methods: {
    async submitLogin() {
      try {
        const params = new URLSearchParams()
        params.append('username', this.username)
        params.append('password', this.password)

        const response = await api.post('/auth/login', params)
        localStorage.setItem('token', response.data.access_token)

        this.$bus.emit('login-success')  // ✅ Event émis via mitt
        this.$router.push('/')
      } catch (err) {
        console.error("Réponse complète API (login) :", err.response)
        this.error = err.response?.data?.detail || "Identifiant ou mot de passe incorrect."
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Trocchi&family=Oswald:wght@500&display=swap');

.form-container {
  max-width: 400px;
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
  color: #99775C;
  font-size: 1.8rem;
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

.error {
  color: #c0392b;
  margin-top: 1rem;
  text-align: center;
  font-weight: bold;
}
</style>

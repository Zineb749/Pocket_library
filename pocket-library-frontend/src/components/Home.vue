<template>
  <div class="home">
    <div class="welcome-card">
      <h1 class="title">Bienvenue sur Pocket Library</h1>
      <p class="tagline">Votre univers littéraire personnalisé</p>
      <p class="description">
        Suivez vos lectures, organisez vos coups de cœur et partez à la découverte de nouveaux livres inspirants.
      </p>
      <router-link
        v-if="username"
        to="/books"
        class="btn-cta"
      >
        Voir ma bibliothèque
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  props: {
    username: {
      type: String,
      default: null,
    },
  },
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Trocchi&family=Oswald:wght@500&display=swap');

.home {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 80px);
  background-color: #EAE7DD;
  padding: 2rem;
}

.welcome-card {
  background: #ffffff;
  padding: 3rem 2.5rem;
  border-radius: 14px;
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.1);
  max-width: 650px;
  width: 100%;
  text-align: center;
  border: 2px solid #99775C;
}

.title {
  font-family: 'Trocchi', serif; /* pour Clarendon-like */
  font-size: 2.5rem;
  color: #99775C;
  margin-bottom: 0.6rem;
}

.tagline {
  font-family: 'Oswald', sans-serif; /* pour Lulo Clean-like */
  font-size: 1.2rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #7a5c46;
  margin-bottom: 1.2rem;
}

.description {
  font-family: Georgia, serif;
  font-size: 1rem;
  line-height: 1.6;
  color: #3e2f23;
  margin-bottom: 2rem;
}

.btn-cta {
  display: inline-block;
  background-color: #99775C;
  color: #FAF5E9;
  padding: 0.9rem 1.8rem;
  border-radius: 6px;
  font-family: 'Oswald', sans-serif;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  text-decoration: none;
  font-weight: 600;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.btn-cta:hover {
  background-color: #7a5c46;
  transform: translateY(-2px);
}
</style>

<template>
  <span class="stars">
    <i v-for="i in 5" :key="i" :class="i <= rating ? 'fas fa-star filled' : 'far fa-star empty'"></i>
  </span>
</template>

<script setup>
defineProps({
  rating: Number
})
</script>

<style scoped>
.stars {
  color: #F4C430;
  font-size: 1rem;
}
.filled {
  color: #F4C430;
}
.empty {
  color: #ddd3c2;
}
</style>

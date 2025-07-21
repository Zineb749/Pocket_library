<template>
  <div class="star-input">
    <i
      v-for="n in 5"
      :key="n"
      class="fa-star"
      :class="n <= localRating ? 'fas filled' : 'far empty'"
      @click="selectRating(n)"
    ></i>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({ rating: Number })
const emit = defineEmits(['update:rating'])

const localRating = ref(props.rating || 0)

watch(() => props.rating, (val) => {
  localRating.value = val
})

function selectRating(n) {
  localRating.value = n
  emit('update:rating', n)
}
</script>

<style scoped>
.star-input {
  display: flex;
  gap: 0.4rem;
  font-size: 1.6rem;
  cursor: pointer;
}
.filled {
  color: #F4C430;
  transition: transform 0.2s;
}
.empty {
  color: #ddd3c2;
  transition: transform 0.2s;
}
.fa-star:hover {
  transform: scale(1.2);
}
</style>

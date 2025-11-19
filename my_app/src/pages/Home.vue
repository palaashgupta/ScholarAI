<template>
  <div class="home-page">
    <!-- Hero Section -->
    <div
      class="hero d-flex flex-column justify-content-center align-items-center text-center"
      :style="{ backgroundImage: `url(${backgroundImg})` }"
    >
      <h1 class="display-4 text-white fw-bold">Welcome to ScholarAI</h1>
      <p class="lead text-white mb-4">
        Search and explore research papers easily.
      </p>

      <!-- Search form -->
      <form class="d-flex w-50 justify-content-center" @submit.prevent="search">
        <input
          v-model="query"
          class="form-control me-2"
          type="search"
          placeholder="Search papers..."
          required
        />
        <button class="btn btn-outline-light" type="submit">Search</button>
      </form>

      <!-- Get Started button -->
      <router-link
        v-if="!isLoggedIn"
        to="/login"
        class="btn btn-primary btn-lg mt-4"
      >
        Get Started
      </router-link>
    </div>

    <!-- Optional features section -->
    <div class="container my-5">
      <div class="row text-center">
        <div class="col-md-4">
          <i class="bi bi-search display-3 text-primary mb-2"></i>
          <h4>Powerful Search</h4>
          <p>Quickly find research papers and abstracts from top sources.</p>
        </div>
        <div class="col-md-4">
          <i class="bi bi-file-earmark-text display-3 text-primary mb-2"></i>
          <h4>Paper Summaries</h4>
          <p>Get concise summaries to save time on reading full papers.</p>
        </div>
        <div class="col-md-4">
          <i class="bi bi-bar-chart-line display-3 text-primary mb-2"></i>
          <h4>Analytics</h4>
          <p>Track trends, citations, and research impact over time.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, watchEffect } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useSearch } from '../composables/useSearch';
import backgroundImg from '../assets/background_home.png';

const auth = useAuthStore();
const { query, search, loading } = useSearch();

const isLoggedIn = computed(() => !!auth.user);

watchEffect(() => {
  console.log('Auth changed →', auth.user);
});

onMounted(() => {
  auth.fetchCurrentUser();
});
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.hero {
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  min-height: 80vh;
  padding: 100px 20px;
  position: relative;
}

.hero::after {
  content: "";
  position: absolute;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5); /* overlay */
}

.hero h1,
.hero p,
.hero form,
.hero a {
  position: relative;
  z-index: 1;
}

.hero input.form-control {
  border-radius: 50px;
}

.hero button {
  border-radius: 50px;
}
</style>

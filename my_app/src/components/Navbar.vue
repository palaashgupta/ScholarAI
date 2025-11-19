<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">

      <!-- Brand -->
      <a class="navbar-brand" href="#" @click.prevent="goHome">ScholarAI</a>

      <!-- Search form -->
      <form class="d-flex ms-3" @submit.prevent="search">
        <input
          v-model="query"
          class="form-control me-2"
          type="search"
          placeholder="Search papers"
        />
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>

      <!-- Dashboard Button -->
      <button
        v-if="isLoggedIn"
        class="btn btn-outline-success ms-2 me-2"
        @click="goDashboard"
      >
        Dashboard
      </button>

      <!-- Navbar toggle for mobile -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNavDropdown"
        aria-controls="navbarNavDropdown"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- RIGHT SIDE: Theme Toggle + Dropdown Menu -->
      <div class="collapse navbar-collapse justify-content-end" id="navbarNavDropdown">
        <ul class="navbar-nav align-items-center">

          <!-- Theme Toggle -->
          <li class="nav-item">
            <button
              class="btn btn-link me-2"
              @click="toggleTheme"
              style="font-size: 1.4rem;"
            >
              <i :class="themeStore.theme === 'light' ? 'bi bi-brightness-high' : 'bi bi-brightness-high-fill'"></i>
            </button>
          </li>

          <!-- Dropdown Menu -->
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              id="navbarDropdown"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Menu
            </a>

            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">

              <!-- Login / Logout -->
              <li v-if="!isLoggedIn">
                <router-link class="dropdown-item" to="/login">Login</router-link>
              </li>

              <li v-else>
                <a class="dropdown-item" href="#" @click.prevent="logoutUser">Logout</a>
              </li>

              <!-- About Us -->
              <li>
                <router-link class="dropdown-item" to="/about-us">About Us</router-link>
              </li>

              <!-- Admin Control -->
              <li v-if="isAdmin">
                <router-link class="dropdown-item" to="/admin">Admin Control</router-link>
              </li>

            </ul>
          </li>

        </ul>
      </div>

    </div>
  </nav>
</template>

<script setup>
import { computed, onMounted, watchEffect } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useThemeStore } from '../stores/theme';
import { useSearch } from '../composables/useSearch';
import { useRouter } from 'vue-router';

const auth = useAuthStore();
const themeStore = useThemeStore();
const router = useRouter();

const { query, search, loading } = useSearch();

// Computed states
const isLoggedIn = computed(() => !!auth.user);
const isAdmin = computed(() => auth.user?.role === 'ADMIN');

watchEffect(() => {
  console.log('Auth changed →', auth.user);
});

onMounted(() => {
  auth.fetchCurrentUser();
});

function goDashboard() {
  if (!isLoggedIn.value) {
    alert('You must login first!');
    setTimeout(() => router.push('/login'), 1500);
    return;
  }
  router.push('/dashboard');
}

function goHome() {
  router.push('/');
}

async function logoutUser() {
  await auth.logout();
  router.push('/');
}

function toggleTheme() {
  themeStore.toggleTheme();
}
</script>

<style scoped>
.navbar-brand {
  cursor: pointer;
}
</style>

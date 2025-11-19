<template>
  <nav class="navbar navbar-expand-lg navbar-gradient">
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
        <button class="btn btn-outline-light" type="submit">Search</button>
      </form>

      <!-- Dashboard Button -->
      <button
        v-if="isLoggedIn"
        class="btn btn-outline-light ms-2 me-2"
        @click="goDashboard"
      >
        Dashboard
      </button>

      <!-- Navbar toggle for mobile -->
      <button
        class="navbar-toggler"
        type="button"
        @click="toggleCollapse"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- RIGHT SIDE: Theme Toggle + Dropdown Menu -->
      <div ref="collapseMenu" class="collapse navbar-collapse justify-content-end">
        <ul class="navbar-nav align-items-center">

          <!-- Theme Toggle -->
          <li class="nav-item">
            <button
              class="btn btn-link me-2"
              @click="toggleTheme"
              style="font-size: 1.4rem;"
            >
              <i :class="themeStore.theme === 'light' ? 'bi bi-brightness-high' : 'bi bi-moon-stars-fill'"></i>
            </button>
          </li>

          <!-- Dropdown Menu -->
          <li class="nav-item dropdown" ref="dropdownEl">
            <a
              class="nav-link dropdown-toggle always-white"
              href="#"
              role="button"
              @click.prevent="toggleDropdown"
            >
              Menu
            </a>

            <ul class="dropdown-menu dropdown-menu-end">
              <li v-if="!isLoggedIn">
                <router-link class="dropdown-item" to="/login">Login</router-link>
              </li>

              <li v-else>
                <a class="dropdown-item" href="#" @click.prevent="logoutUser">Logout</a>
              </li>

              <li>
                <router-link class="dropdown-item" to="/about-us">About Us</router-link>
              </li>

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
import { ref, computed, onMounted, watch } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useThemeStore } from '../stores/theme';
import { useSearch } from '../composables/useSearch';
import { useRouter } from 'vue-router';
import { Collapse, Dropdown } from 'bootstrap';

const auth = useAuthStore();
const themeStore = useThemeStore();
const router = useRouter();

const { query, search } = useSearch();
const isLoggedIn = computed(() => !!auth.user);
const isAdmin = computed(() => auth.user?.role === 'ADMIN');

const collapseMenu = ref(null);
let bsCollapse = null;

const dropdownEl = ref(null);
let bsDropdown = null;

onMounted(() => {
  auth.fetchCurrentUser();

  if (collapseMenu.value) bsCollapse = new Collapse(collapseMenu.value, { toggle: false });
  if (dropdownEl.value) bsDropdown = new Dropdown(dropdownEl.value, { autoClose: true });

  applyTheme();
});

watch(() => themeStore.theme, () => applyTheme());

function toggleCollapse() { if (bsCollapse) bsCollapse.toggle(); }
function toggleDropdown() { if (bsDropdown) bsDropdown.toggle(); }
function goDashboard() {
  if (!isLoggedIn.value) {
    alert('You must login first!');
    setTimeout(() => router.push('/login'), 1500);
    return;
  }
  router.push('/dashboard');
}
function goHome() { router.push('/'); }
async function logoutUser() { await auth.logout(); router.push('/'); }
function toggleTheme() { themeStore.toggleTheme(); }

function applyTheme() {
  const navbar = document.querySelector('.navbar-gradient');
  if (themeStore.theme === 'light') {
    navbar.style.background = 'linear-gradient(90deg, #4b6cb7, #182848)';
  } else {
    navbar.style.background = 'linear-gradient(90deg, #333, #000)';
  }
}
</script>

<style scoped>
.navbar-gradient {
  transition: background 0.3s ease;
}
.navbar-gradient .nav-item.dropdown > .nav-link.dropdown-toggle {
  color: white !important; /* force white text */
}

.navbar-gradient .nav-item.dropdown > .nav-link.dropdown-toggle:hover {
  opacity: 0.8; /* subtle hover effect */
}
.navbar-brand,
.btn-outline-light {
  color: inherit;
  transition: color 0.3s ease;
}

.navbar-brand:hover {
  opacity: 0.8;
}

/* Make Menu text always white */
.always-white {
  color: white !important;
}

.dropdown-menu {
  min-width: 180px;
}
</style>

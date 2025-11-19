<template>
  <Navbar />
  <router-view />
  <AppFooter />
</template>

<script setup>
import Navbar from './components/Navbar.vue';
import AppFooter from './components/AppFooter.vue';
import { onMounted } from 'vue';
import { useAuthStore } from './stores/auth';

const auth = useAuthStore();

onMounted(async () => {
  if (!auth.user) {
    await auth.fetchCurrentUser();
  }
});
</script>


<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
}
/* DARK THEME DROPDOWN */
html[data-theme="dark"] .dropdown-menu {
  background-color: #222;        /* dark menu background */
  color: #eee;                   /* text color */
  border: 1px solid #444;
}

html[data-theme="dark"] .dropdown-menu .dropdown-item {
  color: #eee;
}

html[data-theme="dark"] .dropdown-menu .dropdown-item:hover,
html[data-theme="dark"] .dropdown-menu .dropdown-item:focus {
  background-color: #333;
  color: white;
}

</style>

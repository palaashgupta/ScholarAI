<template>
  <Navbar />
  <router-view />
</template>

<script setup>
import Navbar from './components/Navbar.vue';
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
</style>

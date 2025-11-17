<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-5">
        <div class="card shadow-sm">
          <div class="card-body">
            <h3 class="card-title text-center mb-4">Login to ScholarAI</h3>

            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label for="email" class="form-label">Email address</label>
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  v-model="email"
                  placeholder="Enter email"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  v-model="password"
                  placeholder="Password"
                  required
                />
              </div>

              <div v-if="error" class="alert alert-danger">
                {{ error }}
              </div>

              <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                Login
              </button>
            </form>

            <p class="text-center mt-3">
              Don't have an account?
              <router-link to="/register">Register here</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const email = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');

const router = useRouter();
const auth = useAuthStore();

async function handleLogin() {
  error.value = '';
  loading.value = true;

  try {
    const success = await auth.login(email.value, password.value);
    if (success) {
      router.push('/dashboard'); // redirect after successful login
    } else {
      error.value = 'Invalid email or password';
    }
  } catch (err) {
    console.error(err);
    error.value = 'An error occurred during login';
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
body {
  background-color: #f8f9fa;
}
.card {
  border-radius: 0.75rem;
}
</style>

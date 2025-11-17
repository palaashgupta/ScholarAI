<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-5">
        <div class="card shadow-sm">
          <div class="card-body">
            <h3 class="card-title text-center mb-4">Register for ScholarAI</h3>

            <form @submit.prevent="handleRegister">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input
                  type="text"
                  class="form-control"
                  id="username"
                  v-model="username"
                  placeholder="Enter username"
                  required
                />
              </div>

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

              <div class="mb-3">
                <label for="retypePassword" class="form-label">Confirm Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="retypePassword"
                  v-model="retypePassword"
                  placeholder="Confirm password"
                  required
                />
              </div>

              <div v-if="error" class="alert alert-danger">
                {{ error }}
              </div>
              <div v-if="success" class="alert alert-success">
                {{ success }}
              </div>

              <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                Register
              </button>
            </form>

            <p class="text-center mt-3">
              Already have an account?
              <router-link to="/login">Login here</router-link>
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

const username = ref('');
const email = ref('');
const password = ref('');
const retypePassword = ref('');
const loading = ref(false);
const error = ref('');
const success = ref('');

const router = useRouter();

async function handleRegister() {
  error.value = '';
  success.value = '';
  loading.value = true;

  if (password.value !== retypePassword.value) {
    error.value = "Passwords do not match";
    loading.value = false;
    return;
  }

  try {
    const res = await fetch('http://localhost:8000/users/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        email_address: email.value,
        password: password.value,
        retype_password: retypePassword.value
      })
    });

    const data = await res.json();

    if (!res.ok) {
      error.value = data.detail || 'Registration failed';
      loading.value = false;
      return;
    }

    success.value = "Registration successful! Redirecting to login...";
    setTimeout(() => router.push('/login'), 2000);

  } catch (err) {
    console.error(err);
    error.value = "An error occurred during registration";
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

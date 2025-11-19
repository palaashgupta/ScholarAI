<template>
  <div class="dashboard-container">
    <h1>Welcome, {{ auth.user?.username }}</h1>
    <button @click="logout" class="btn btn-outline-danger mb-3">Logout</button>

    <h2>Your Search Queries</h2>

    <div v-if="loading" class="loading">Loading queries...</div>
    <div v-else-if="queries.length === 0" class="no-queries">
      You have no queries yet.
    </div>

    <table v-else class="table table-striped">
      <thead>
        <tr>
          <th>Query</th>
          <th>Date</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="q in queries" :key="q.query_text">
          <td>{{ q.query_text }}</td>
          <td>{{ formatDate(q.created_at) }}</td>
          <td>
            <router-link
              :to="{ path: '/search-result', query: { id: q.query_id, q: q.query_text } }"
              class="btn btn-primary btn-sm me-2"
            >
              View Results
            </router-link>
            <button
              @click="deleteQuery(q.query_text)"
              class="btn btn-danger btn-sm"
            >
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "../stores/auth";
import axios from "axios";

const auth = useAuthStore();
const queries = ref([]);
const loading = ref(true);

// Fetch user queries
async function fetchQueries() {
  try {
    const res = await axios.get("http://localhost:8000/users/me/queries", {
      withCredentials: true,
    });
    // Remove duplicates based on query_text
    const unique = {};
    res.data.forEach(q => { unique[q.query_text] = q; });
    queries.value = Object.values(unique);
  } catch (err) {
    console.error("Failed to fetch queries:", err);
    queries.value = [];
  } finally {
    loading.value = false;
  }
}

// Logout
async function logout() {
  await auth.logout();
  window.location.reload();
}

// Delete query
async function deleteQuery(queryText) {
  if (!confirm(`Are you sure you want to delete all queries for "${queryText}"?`)) return;

  try {
    await axios.delete("http://localhost:8000/users/queries", {
      withCredentials: true,
      data: { query_text: queryText },
    });
    // Remove deleted queries from frontend instantly
    queries.value = queries.value.filter(q => q.query_text !== queryText);
  } catch (err) {
    console.error("Failed to delete query:", err);
    alert("Failed to delete query. Please try again.");
  }
}

// Format date
function formatDate(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleString();
}

onMounted(() => {
  fetchQueries();
});
</script>

<style scoped>
.dashboard-container {
  padding: 30px;
  max-width: 900px;
  margin: auto;
}

.loading,
.no-queries {
  margin-top: 20px;
  font-size: 18px;
}

.table th,
.table td {
  vertical-align: middle;
}

.btn {
  border-radius: 6px;
}
</style>

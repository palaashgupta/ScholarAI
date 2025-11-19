<template>
  <div class="admin-container">
    <h1 class="admin-title">Admin Control Panel</h1>

    <!-- Statistics Cards -->
    <div class="admin-stats">
      <div class="stat-card">
        <h3>Total Users</h3>
        <p>{{ stats.total_users }}</p>
      </div>
      <div class="stat-card">
        <h3>Total Queries</h3>
        <p>{{ stats.total_queries }}</p>
      </div>
      <div class="stat-card">
        <h3>Guest Queries</h3>
        <p>{{ stats.guest_queries }}</p>
      </div>
      <div class="stat-card">
        <h3>Research Papers</h3>
        <p>{{ stats.total_papers }}</p>
      </div>
    </div>

    <!-- Table Selection Buttons -->
    <div class="table-selector my-3 text-center">
      <button
        class="btn"
        :class="selectedTable === 'users' ? 'btn-primary' : 'btn-outline-primary'"
        @click="selectedTable = 'users'"
      >Users</button>
      <button
        class="btn"
        :class="selectedTable === 'queries' ? 'btn-primary' : 'btn-outline-primary'"
        @click="selectedTable = 'queries'"
      >Search Queries</button>
      <button
        class="btn"
        :class="selectedTable === 'papers' ? 'btn-primary' : 'btn-outline-primary'"
        @click="selectedTable = 'papers'"
      >Research Papers</button>
    </div>

    <!-- Users Table -->
    <div v-if="selectedTable === 'users'" class="admin-tables mt-4">
      <h2>Users</h2>
      <table v-if="users.length" class="table table-striped">
        <thead>
          <tr>
            <th>User ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Role</th>
            <th>Created At</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.user_id">
            <td>{{ u.user_id }}</td>
            <td>{{ u.username }}</td>
            <td>{{ u.email_address }}</td>
            <td>{{ u.role }}</td>
            <td>{{ formatDate(u.created_at) }}</td>
            <td>
              <button class="btn btn-danger btn-sm" @click="deleteUser(u.user_id)">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No users found.</p>
    </div>

    <!-- Queries Table -->
    <div v-if="selectedTable === 'queries'" class="admin-tables mt-4">
      <h2>Search Queries</h2>
      <table v-if="queries.length" class="table table-striped">
        <thead>
          <tr>
            <th>Query ID</th>
            <th>User ID</th>
            <th>Query Text</th>
            <th>Date</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="q in queries" :key="q.query_id">
            <td>{{ q.query_id }}</td>
            <td>{{ q.user_id }}</td>
            <td>{{ q.query }}</td>
            <td>{{ formatDate(q.created_at) }}</td>
            <td>
              <button class="btn btn-danger btn-sm" @click="deleteQuery(q.query_id)">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No queries found.</p>
    </div>

    <!-- Research Papers Table -->
    <div v-if="selectedTable === 'papers'" class="admin-tables mt-4">
      <h2>Research Papers</h2>
      <table v-if="papers.length" class="table table-striped">
        <thead>
          <tr>
            <th>Paper ID</th>
            <th>Title</th>
            <th>Authors</th>
            <th>Year</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in papers" :key="p.paper_id">
            <td>{{ p.paper_id }}</td>
            <td>{{ p.title }}</td>
            <td>{{ p.authors }}</td>
            <td>{{ formatYear(p.created_at) }}</td>
            <td>
              <button class="btn btn-danger btn-sm" @click="deletePaper(p.paper_id)">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No papers found.</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue';
import axios from 'axios';

const stats = reactive({
  total_users: 0,
  total_queries: 0,
  guest_queries: 0,
  total_papers: 0
});

const users = ref([]);
const queries = ref([]);
const papers = ref([]);
const selectedTable = ref('users');

function formatYear(dateStr) {
  const d = new Date(dateStr);
  return d.getFullYear(); // Only returns the year
}

// Fetch statistics
async function fetchStats() {
  try {
    const res = await axios.get('http://localhost:8000/admin/stats', { withCredentials: true });
    Object.assign(stats, res.data);
  } catch (err) {
    console.error('Failed to fetch admin stats:', err);
  }
}

// Fetch tables
async function fetchTables() {
  try {
    const [usersRes, queriesRes, papersRes] = await Promise.all([
      axios.get('http://localhost:8000/admin/users', { withCredentials: true }),
      axios.get('http://localhost:8000/admin/queries', { withCredentials: true }),
      axios.get('http://localhost:8000/admin/research-papers', { withCredentials: true })
    ]);
    users.value = usersRes.data;
    queries.value = queriesRes.data;
    papers.value = papersRes.data;
  } catch (err) {
    console.error('Failed to fetch admin tables:', err);
  }
}

// Delete handlers
async function deleteUser(user_id) {
  if (!confirm(`Are you sure you want to delete user ${user_id}?`)) return;
  try {
    await axios.delete(`http://localhost:8000/admin/users/${user_id}`, { withCredentials: true });
    users.value = users.value.filter(u => u.user_id !== user_id);
    stats.total_users--;
  } catch (err) {
    console.error('Failed to delete user:', err);
  }
}

async function deleteQuery(query_id) {
  if (!confirm(`Are you sure you want to delete query ${query_id}?`)) return;
  try {
    await axios.delete(`http://localhost:8000/admin/queries/${query_id}`, { withCredentials: true });
    queries.value = queries.value.filter(q => q.query_id !== query_id);
    stats.total_queries--;
  } catch (err) {
    console.error('Failed to delete query:', err);
  }
}

async function deletePaper(paper_id) {
  if (!confirm(`Are you sure you want to delete paper ${paper_id}?`)) return;
  try {
    await axios.delete(`http://localhost:8000/admin/research-paper/${paper_id}`, { withCredentials: true });
    papers.value = papers.value.filter(p => p.paper_id !== paper_id);
    stats.total_papers--;
  } catch (err) {
    console.error('Failed to delete paper:', err);
  }
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString();
}

onMounted(() => {
  fetchStats();
  fetchTables();
});
</script>

<style scoped>
.admin-container {
  max-width: 1200px;
  margin: 30px auto;
  padding: 0 15px;
}

.admin-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 30px;
}

.admin-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  margin-bottom: 30px;
}

.stat-card {
  flex: 1 1 200px;
  min-width: 180px;
  background: linear-gradient(90deg, #4b6cb7, #182848);
  color: white;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-card h3 {
  margin-bottom: 10px;
}

.stat-card p {
  font-size: 1.5rem;
  font-weight: 600;
}

.table-selector .btn {
  margin: 0 5px;
}

.admin-tables {
  margin-top: 20px;
}

.admin-tables table {
  width: 100%;
}

.admin-tables h2 {
  margin-bottom: 15px;
}
</style>

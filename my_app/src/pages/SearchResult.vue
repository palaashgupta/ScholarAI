<template>
  <div class="search-results-container">
    <!-- Query Header -->
    <h1 class="query-title">
      Results for: <span>"{{ query }}"</span>
    </h1>
    <p class="query-id" v-if="query_id">
      <strong>Query ID:</strong> {{ query_id }}
    </p>

    <!-- Loading -->
    <div v-if="loading" class="loading">Loading results...</div>

    <!-- No results -->
    <div v-else-if="results.length === 0" class="no-results">
      No results found.
    </div>

    <!-- Card Grid -->
    <div class="results-grid">
      <div class="result-card" v-for="paper in results" :key="paper.paper_id">
        <h2 class="paper-title">
          {{
            paper.title
              ? paper.title.split(" ").length > 7
                ? paper.title.split(" ").slice(0, 7).join(" ") + "..."
                : paper.title
              : "Untitled"
          }}
        </h2>

        <p class="paper-authors">
          <strong>Authors:</strong>
          {{
            paper.authors
              ? paper.authors.length > 2
                ? paper.authors.slice(0, 2).join(", ") + ", ..."
                : paper.authors.join(", ")
              : "N/A"
          }}
        </p>


        <p class="paper-year">
          <strong>Year:</strong> {{ paper.created_at ? paper.created_at.substring(0, 4) : "N/A" }}
        </p>

        <a
          class="paper-link"
          :href="paper.paper_url"
          target="_blank"
          rel="noopener noreferrer"
        >
          🔗 View Paper
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const query = ref(route.query.q || "");
const query_id = ref(route.query.id || null);

const results = ref([]);
const loading = ref(true);

onMounted(async () => {
  if (!query_id.value) {
    loading.value = false;
    return;
  }

  try {
    const res = await axios.get(`http://localhost:8000/search/query/${query_id.value}`, {
      withCredentials: true,
    });

    query.value = res.data.query || query.value;
    results.value = res.data.papers || [];
  } catch (err) {
    console.error("Failed to fetch search results:", err);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.search-results-container {
  padding: 40px;
  max-width: 1000px;
  margin: auto;
}

.query-title {
  font-size: 28px;
  margin-bottom: 20px;
}

.query-title span {
  color: #3498db;
  font-weight: bold;
}

.loading,
.no-results {
  margin-top: 20px;
  font-size: 18px;
  text-align: center;
}

.results-grid {
  margin-top: 30px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.result-card {
  background: var(--card-bg);
  color: var(--card-text);
  border-radius: 10px;
  padding: 20px;
  border: 1px solid var(--card-border);
  transition: transform 0.15s ease-in-out;
}


.result-card:hover {
  transform: scale(1.03);
}

.paper-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 12px;
}

.paper-authors,
.paper-year {
  margin-bottom: 10px;
  font-size: 14px;
}

.paper-link {
  display: inline-block;
  margin-top: 10px;
  padding: 8px 14px;
  background: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  transition: 0.2s;
}

.paper-link:hover {
  background: #217dbb;
}

.query-id {
  font-size: 14px;
  color: #666;
  margin-bottom: 15px;
}
</style>

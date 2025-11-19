// src/composables/useSearch.js
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export function useSearch() {
  const router = useRouter();
  const query = ref('');
  const loading = ref(false);

  const search = async () => {
    if (!query.value.trim()) return;
    loading.value = true;

    try {
      const res = await fetch('http://localhost:8000/search/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ query: query.value })
      });

      if (!res.ok) throw new Error('Search failed');

      const data = await res.json(); // Includes query_id, papers, etc.

      // Redirect to search results page
      router.push({
        path: '/search-result',
        query: { q: query.value, id: data.query_id }
      });

    } catch (err) {
      console.error(err);
      alert('Search failed');
    } finally {
      loading.value = false;
    }
  };

  return { query, search, loading };
}

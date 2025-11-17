import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useAuthStore = defineStore('auth', () => {
    const user = ref(null);
    const loading = ref(false);

    // Fetch current logged-in user
    async function fetchCurrentUser() {
        try {
            const res = await fetch('http://localhost:8000/users/me', {
                credentials: 'include'
            });
            if (!res.ok) {
                user.value = null;
                return null;
            }
            const data = await res.json();
            user.value = data;
            return data;
        } catch (err) {
            console.error(err);
            user.value = null;
            return null;
        }
    }

    // Login function
    async function login(email, password) {
        loading.value = true;
        try {
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', password);

            const res = await fetch('http://localhost:8000/users/login', {
                method: 'POST',
                body: formData,
                credentials: 'include'
            });

            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.detail || 'Login failed');
            }

            const data = await res.json();
            user.value = data;
            loading.value = false;
            return true;
        } catch (err) {
            console.error(err);
            loading.value = false;
            return false;
        }
    }

    // Logout function
    async function logout() {
        loading.value = true;
        try {
            const res = await fetch('http://localhost:8000/users/logout', {
                method: 'POST',
                credentials: 'include' // important to send cookie
            });

            if (!res.ok) {
                throw new Error('Logout failed');
            }

            user.value = null;
            loading.value = false;
            return true;
        } catch (err) {
            console.error(err);
            loading.value = false;
            return false;
        }
    }

    return { user, loading, login, fetchCurrentUser, logout };
},
{
    persist: true // ← this persists user state in localStorage
});

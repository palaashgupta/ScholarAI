import { defineStore } from 'pinia';
import { ref,watch } from 'vue';

export const useThemeStore = defineStore('theme', () => {
    const theme = ref(localStorage.getItem('theme') || 'light');

    const applyTheme = () => {
        document.documentElement.setAttribute('data-theme', theme.value);
    };
    applyTheme();

    watch(theme, (newTheme) => {
        localStorage.setItem('theme', newTheme);
        applyTheme();
    });

    function toggleTheme() {
        theme.value = theme.value === 'light' ? 'dark' : 'light';
    }

    return { theme, toggleTheme };
});
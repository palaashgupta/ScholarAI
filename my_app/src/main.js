import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import piniaPersist from 'pinia-plugin-persistedstate';

// --- Import Bootstrap CSS & JS ---
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

const pinia = createPinia();
pinia.use(piniaPersist);

createApp(App).use(pinia).use(router).mount('#app');

import { createRouter, createWebHistory} from 'vue-router';
import Home from '../pages/Home.vue';
import Login from '../pages/Login.vue';
import Logout from '../pages/Logout.vue';
import SearchResult from '../pages/SearchResult.vue';
import AboutUs from '../pages/AboutUs.vue';
import Dashboard from '../pages/Dashboard.vue';
import Admin from '../pages/Admin.vue';
import { useAuthStore } from '../stores/auth';


const routes = [
    { path: "/", component: Home},
    { path: "/login", component: Login },
    { path: "/logout", component: Logout, meta: { requiresAuth: true } },
    { path: "/search-result", component: SearchResult},
    { path: "/about-us", component: AboutUs},
    { path: "/admin", component: Admin, meta: { requiresAuth: true } },
    {
        path: "/dashboard",
        component: Dashboard,
        meta: { requiresAuth: true },
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// Guard protected routes
router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore();

  if (auth.user === null) {
    await auth.fetchCurrentUser();
  }

  if (to.meta.requiresAuth && !auth.user) {
    next("/login");
  } else {
    next();
  }
});


export default router;
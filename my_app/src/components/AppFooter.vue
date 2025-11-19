<template>
  <footer class="app-footer">
    <div class="footer-content">
      <span class="name">{{ name }}</span>
      <span class="divider">|</span>
      <a :href="`mailto:${email}`" class="email">{{ email }}</a>
      <span class="divider">|</span>
      <a :href="github" class="github" target="_blank" rel="noopener noreferrer">{{ github }}</a>
    </div>
  </footer>
</template>

<script setup>
import { watch, onMounted } from "vue";
import { useThemeStore } from "../stores/theme";

const themeStore = useThemeStore();

const name = "Palaash Gupta";
const email = "palaashgupta2584@gmail.com";
const github = "https://github.com/palaashgupta";

function applyTheme() {
  const footer = document.querySelector(".app-footer");
  if (!footer) return;

  if (themeStore.theme === "light") {
    footer.style.background = "linear-gradient(90deg, #4b6cb7, #182848)";
    footer.style.color = "#ffffff";
  } else {
    footer.style.background = "linear-gradient(90deg, #222, #000)";
    footer.style.color = "#ffffff";
  }
}

watch(() => themeStore.theme, applyTheme);

onMounted(() => {
  applyTheme();
});
</script>

<style scoped>
.app-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  color: #ffffff;
  text-align: center;
  padding: 12px 0;
  font-size: 0.95rem;
  font-weight: 500;
  box-shadow: 0 -3px 6px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: background 0.3s ease, color 0.3s ease;
}

.app-footer:hover {
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.footer-content {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
}

.name {
  font-size: 1rem;
  font-weight: 600;
}

.divider {
  color: #ffffff88;
}

.email {
  color: #ffffffcc;
  text-decoration: none;
  transition: color 0.3s ease;
}

.email:hover {
  color: #ffd700; /* subtle gold highlight */
  text-decoration: underline;
}

.github {
  color: #ffffffcc;
  text-decoration: none;
  transition: color 0.3s ease;
}

.github:hover {
  color: #ffd700;
  text-decoration: underline;
}

@media (max-width: 500px) {
  .footer-content {
    flex-direction: column;
    gap: 4px;
  }
}
</style>

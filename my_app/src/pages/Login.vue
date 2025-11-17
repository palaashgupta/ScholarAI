<template>
    <div class="login-container">
        <h2>login</h2>
        <form @submit.prevent="handle">
            <input v-model="email" placeholder="Email"/>
            <input v-model="password" type="password" placeholder="Password"/>

            <button :disabled="useAuthStore.loading">Login</button>
        </form>
        <p v-if="error" class="error">Invalid Email or password</p>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const auth = useAuthStore();
const router = useRouter(); 
const email = ref('');
const password = ref('');
const error = ref(false);

async function handle() {
    const ok = await auth.login(email.value, password.value);

    if (ok) {
        router.push('/');
    } else {
        error.value = true;
    }
    
}
</script>
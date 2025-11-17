<template>
    <div>
        <h1>Welcome {{ auth.user?.name }}</h1>
        <button @click="logout">Logout</button>

        <button @click="deleteAccount" class="danger">Delete My Account</button>
    </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth';
import api from '../api/axios';
const auth = useAuthStore();

async function logout() {
    await auth.logout();
    window.location.reload();
}

async function deleteAccount() {
    await api.delete('/users/delete-account');
    await auth.logout();
    alert('Your account has been deleted.');
    window.location.reload();
}
</script>
<style>
.danger { color:red;}
</style>
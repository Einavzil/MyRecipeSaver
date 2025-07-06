<template>
    <div>
        <h1>Register</h1>
        <form @submit.prevent="handleRegister">
            <div class="input-group">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" required />
            </div>
            <div class="input-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required />
            </div>
            <button type="submit">Register</button>
        </form>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
</template>
<script setup>
    import { ref } from 'vue';
    import { registerUser } from '../services/auth';
    async function handleRegister() {
        try {
            const response = await registerUser(username.value, password.value);
            console.log('Registration response:', response);
            localStorage.setItem('token', response.userToken);
            localStorage.setItem('userId', response.userId);
        } catch (error) {
            errorMessage.value = error.message || 'Registration failed';
        }
    }
</script>
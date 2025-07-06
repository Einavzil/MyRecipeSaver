
<template>
  <div class="login-page-container">
    <BContainer fluid class="d-flex justify-content-center align-items-start vh-100">
      <BRow class="justify-content-center w-100">
        <BCol cols="12" md="6" lg="4" class="mt-5">
          <h3 class="text-center mb-5">Log In to Your Account</h3>

            <BForm @submit.prevent="handleLogin">
              <BFormGroup
                id="input-group-username"
                label="Username:"
                label-for="username-input"
                class="mb-3"
              >
                <BFormInput
                  id="username-input"
                  v-model="username"
                  type="text"
                  placeholder="Enter your username"
                  required

                ></BFormInput>
              </BFormGroup>

              <BFormGroup
                id="input-group-password"
                label="Password:"
                label-for="password-input"
                class="mb-4"
              >
                <BFormInput
                  id="password-input"
                  v-model="password"
                  type="password"
                  placeholder="Enter your password"
                  required
                ></BFormInput>
              </BFormGroup>

              <BButton type="submit" variant="primary" class="w-100 mb-3">Login</BButton>
            </BForm>

            <BAlert v-if="errorMessage" show variant="danger" class="mt-3">{{ errorMessage }}</BAlert>

            <hr class="my-4">

            <p class="text-center mb-0">
              Don't have an account?
              <router-link to="/register">Register here</router-link>
            </p>
        </BCol>
      </BRow>
    </BContainer>
  </div>
</template>

<script>
import { loginUser } from '../services/auth';

export default {
    name: 'Login',
    data() {
        return {
            username: '',
            password: '',
            errorMessage: null
        };
    },
    mounted() {
        // Check if user is already logged in
        const userToken = localStorage.getItem('token');
        if (userToken) {
            this.$router.push({ name: 'recipe-list' }); // Redirect to the recipes page if already logged in
        }
    },

    methods: {
         async handleLogin() {
            try{
              const response = await loginUser(this.username, this.password);
              console.log('Login response:', response);
              localStorage.setItem('token', response.userToken);
              localStorage.setItem('userId', response.userId);
              this.$root.checkLoginStatus();
              await this.$router.push({ name: 'recipe-list' });
            } catch(error) {
              console.error('Login error:', error);
              this.errorMessage = 'Login failed. Please check your credentials.';
            }
         }
    }
}
</script>
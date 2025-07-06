<template>
  <div>
    <header class="app-header">
      <BNavbar toggleable="lg" type="dark" variant="dark">
        <BNavbarBrand to="/">My Recipe Saver</BNavbarBrand> <BNavbarToggle target="nav-collapse"></BNavbarToggle>
          <BCollapse id="nav-collapse" is-nav>
          <BNavbarNav class="ms-auto"> 
            <BNavItem v-if="isLoggedIn" to="/recipe" active-class="active" exact-active-class="active">Recipes</BNavItem>
            <BNavItem v-if="isLoggedIn" to="/add-recipe" active-class="active" exact-active-class="active">Add Recipe</BNavItem>
            <BNavItem v-if="!isLoggedIn" to="/login" active-class="active" exact-active-class="active">Login</BNavItem>
            <BNavItem v-if="!isLoggedIn" to="/register" active-class="active" exact-active-class="active">Register</BNavItem>
            <BNavItem v-if="isLoggedIn" @click="handleLogout">Logout</BNavItem> 
          </BNavbarNav>
        </BCollapse>
      </BNavbar>
    </header>
    <router-view></router-view>
  </div>
</template>
<script>
import { BNavbar, BNavbarBrand, BNavbarNav, BNavItem, BNavbarToggle, BCollapse } from 'bootstrap-vue-next';
export default {
  name: 'App',
  components: {
    BNavbar,
    BNavbarBrand,
    BNavbarNav,
    BNavItem,
    BNavbarToggle,
    BCollapse
  },
  data() {
    return {
      isLoggedIn: !!localStorage.getItem('token')
    };
  },
  methods: {
    checkLoginStatus() {
      this.isLoggedIn = !!localStorage.getItem('token');
    },
    handleLogout() {
      this.isLoggedIn = false;
      localStorage.removeItem('token');
      localStorage.removeItem('userId');
      this.$router.push('/login'); // Redirect to login page after logout
    }
  }
};
</script>
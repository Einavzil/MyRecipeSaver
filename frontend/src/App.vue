<template>
  <div>
    <header class="app-header">
      <BNavbar toggleable="lg" type="dark" variant="dark">
        <BNavbarBrand to="/">My Recipe Saver</BNavbarBrand> <BNavbarToggle target="nav-collapse"></BNavbarToggle>
          <BCollapse id="nav-collapse" is-nav>
          <BNavbarNav class="ms-auto"> <BNavItem to="/recipe" active-class="active" exact-active-class="active">Recipes</BNavItem>
            <BNavItem to="/add-recipe" active-class="active" exact-active-class="active">Add Recipe</BNavItem>
            <!-- <BNavItem v-if="!isLoggedIn" to="/login" active-class="active" exact-active-class="active">Login</BNavItem>
            <BNavItem v-if="!isLoggedIn" to="/register" active-class="active" exact-active-class="active">Register</BNavItem>
            <BNavItem v-else @click="handleLogout">Logout</BNavItem> -->
          </BNavbarNav>
        </BCollapse>
      </BNavbar>
    </header>
    <router-view></router-view>
  </div>
</template>
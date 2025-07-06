import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'

import { createBootstrap } from 'bootstrap-vue-next'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

import Login from './views/Login.vue'
import Register from './views/Register.vue'
import RecipeList from './views/RecipeList.vue'
import Recipe from './views/Recipe.vue'
import EditRecipe from './views/EditRecipe.vue'
import AddRecipe from './views/AddRecipe.vue'

const router =  createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/login', component: Login},
        {path: '/register', component: Register},
        {path: '/recipe', component: RecipeList, name: 'recipe-list'},
        {path: '/recipe/:recipeId', component: Recipe, name: 'recipe-detail'},
        {path: '/recipe/:recipeId/edit', component: EditRecipe, name: 'edit-recipe'},
        {path: '/add-recipe', component: AddRecipe, name: 'add-recipe'},
        {path: '/', redirect: '/login'}
    ]
});

const app = createApp(App)
app.use(router)
app.use(createBootstrap())
app.mount('#app')
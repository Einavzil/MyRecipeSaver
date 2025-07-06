<template>
    <BContainer fluid class="d-flex justify-content-center align-items-start vh-100">
        <BRow class="justify-content-center w-100">
            <BCol cols="12" md="6" lg="4" class="mt-5">
                <h3 class="text-center mb-5">Your Recipe List</h3>

                <div v-if="loading" class="text-center my-4">
                    <BSpinner type="grow" label=""></BSpinner>
                    <p class="mt-2">Loading recipes...</p>
                </div>

                <BAlert v-if="errorMessage" show variant="danger" class="mt-3">{{ errorMessage }}</BAlert>

                <BAlert v-if="!loading && !errorMessage && recipeList.length === 0" show variant="info" class="mt-3">
                    You don't have any recipes yet.
                </BAlert>
    
                <BListGroup v-if="recipeList.length > 0 && !loading">
                    <BListGroupItem
                        v-for="recipe in recipeList" 
                        :key="recipe._id"
                        class="d-flex justify-content-between align-items-center mb-2 shadow-sm recipe-item"
                        >
                        <router-link :to="{ name: 'recipe-detail', params: { recipeId: recipe._id } }" class="recipe-title-link">
                            {{ recipe.name }}
                        </router-link>
                    </BListGroupItem>
                </BListGroup>

                <div class="text-center mt-4">
                    <BButton variant="success" @click="$router.push('/add-recipe')" class="w-100">
                        Add New Recipe
                    </BButton>
                </div>
            </BCol>
        </BRow>
    </BContainer>
  
</template>
<script>
import { fetchRecipes } from '../services/recipes';
import { getAuthHeaders } from '../services/auth';
import { BContainer, BRow, BCol, BSpinner, BListGroup, BListGroupItem,
    BButton, BAlert
} from 'bootstrap-vue-next';
   export default {
        name: 'RecipeList',
        data() {
            return {
                recipeList: [],
                loading: true,
                errorMessage: ''
            };
        },
        async mounted() {
            // check if user is logged in
            const userToken = localStorage.getItem('token');
            if (!userToken) {
                this.errorMessage = 'User not logged in. Please log in to view recipes.';
                this.loading = false;
                this.$router.push('/login'); // Redirect to login page
                return;
            }
            // fetch recipes for the logged in user
            await this.fetchUserRecipes();
        },
        methods: {
            async fetchUserRecipes() {
                this.loading = true;
                this.errorMessage = '';
                try {
                    const response = await fetchRecipes();
                    this.recipeList = response.recipes;
                    console.log('Fetched recipes:', response.recipes);
                } catch(error) {
                    if (error.status === 401) {
                        this.errorMessage = 'Unauthorized access. Please log in again.';
                        localStorage.removeItem('token'); // Clear token on unauthorized access
                        this.$router.push('/login'); // Redirect to login page
                    } else {
                        this.errorMessage = 'Failed to fetch recipes. Please try again later.';
                        this.recipeList = [];
                        // Log error for debugging
                        console.error('Error fetching recipes:', error);
                    }
                    
                } finally {
                    this.loading = false;
                }
            }
        }
    };
   
</script>
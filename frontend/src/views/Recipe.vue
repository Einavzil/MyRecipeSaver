<template>
    <div>
        <BContainer fluid class="d-flex justify-content-center align-items-start vh-100">
            <BRow class="justify-content-center w-100">
                <BCol cols="12" md="8" lg="6" class="mt-5">
                    <h1 class="text-center mb-3">Recipe Details</h1>
                        
                    <div v-if="loading" class="text-center my-4">
                        <BSpinner type="grow" label="Loading..."></BSpinner>
                        <p class="mt-2">Loading recipe...</p>
                    </div>

                    <BAlert v-if="errorMessage" show variant="danger" class="mt-3">{{ errorMessage }}</BAlert>

                    <BCard v-if="recipe && !loading && !errorMessage" class="recipe-details-card">
                    <h2>{{ recipe.name }}</h2>
                    <p>{{ recipe.description }}</p>
                    
                    <strong>Cook Time:</strong> {{ recipe.cookTime || 'N/A' }}
                    <br>
                    <strong>Servings:</strong> {{ recipe.servings || 'N/A' }}

                    <hr>
                    <h3>Ingredients:</h3>
                    <BListGroup class="mb-4"> 
                        <BListGroupItem v-for="(ingredient, index) in recipe.ingredients" :key="index">
                            {{ ingredient.quantity }} {{ ingredient.unit }} {{ ingredient.name }}
                        </BListGroupItem>
                    </BListGroup>

                    <h3>Instructions:</h3>
                    <BListGroup class="list-group list-group-numbered mb-4">
                        <BListGroupItem v-for="(instruction, index) in recipe.instructions" :key="index">
                            {{ instruction.order}}. {{instruction.content }}
                        </BListGroupItem>
                    </BListGroup>

                    <div class="actions text-center mt-4">
                        <BButton variant="primary" class="me-2" @click="editRecipe(recipe._id)">Edit Recipe</BButton>
                        <BButton variant="danger" @click="deleteRecipe(recipe._id)">Delete Recipe</BButton>
                    </div>
                    </BCard>
                    <p v-else-if="!loading && !errorMessage && !recipe" class="text-center mt-5">
                        Recipe not found or could not be loaded.
                    </p>
                </BCol>
            </BRow>
        </BContainer>
    </div>
</template>
<script>
import { BListGroupItem } from 'bootstrap-vue-next';
import { getAuthHeaders } from '../services/auth';
import { fetchSingleRecipe, deleteRecipe } from '../services/recipes'; // Correct function name

export default {
    name: 'Recipe',
    data() {
        return {
            recipe: null,
            loading: true,
            errorMessage: ''
        };
    },
    async mounted() {
        // call method to fetch single recipe
        await this.fetchRecipeData();
    },
    methods: {
        async fetchRecipeData() {
            this.errorMessage = '';
            this.loading = true; 
            this.recipe = null; 

            try {
                // Access route parameters to get the recipe ID
                const recipeId = this.$route.params.recipeId;

                if (!recipeId) {
                    // set an error message and throw an error if there is no recipeId
                    this.errorMessage = 'Recipe ID is missing from the URL.';
                    throw new Error('Recipe ID is required'); // This will stop execution
                }

                // pass the recipeId to the fetchSingleRecipe function
                const fetchedRecipe = await fetchSingleRecipe(recipeId);
                this.recipe = fetchedRecipe;

                // convert cook time to hours and minutes
                const hours = Math.floor(this.recipe.cookTime / 60);
                const minutes = this.recipe.cookTime % 60;

                // format cook time to show Nh Nm
                this.recipe.cookTime = `${hours}h ${minutes}m`; 

                // sort instructions by order
                this.recipe.instructions.sort((a, b) => a.order - b.order);
                console.log('Fetched recipe:', this.recipe);

            } catch (error) {
                console.error('Error fetching recipe:', error);
                // Ensure errorMessage is updated if an error occurs
                this.errorMessage = error.message || 'Failed to fetch recipe details.';
            } finally {
                this.loading = false; // Set loading state to false after fetching
            }
        },
        editRecipe(recipeId) {
            // Navigate to the edit recipe page with the recipe ID
            console.log('Navigating to edit recipe with ID:', recipeId);
            this.$router.push({ name: 'edit-recipe', params: { recipeId } });
        },
        async deleteRecipe(recipeId) {
            const confirmation = confirm('Are you sure you want to delete this recipe?');
            console.log('Deleting recipe with ID:', recipeId);
            // if user cancels the deletion, do not proceed
            if (!confirmation) {
                console.log('Recipe deletion cancelled by user.');
                return; 
            }
            const result = await deleteRecipe(recipeId, getAuthHeaders());
            console.log('Delete result:', result);
            // return to recipe list
            this.$router.push({ name: 'recipe-list' }); // Redirect to the recipe list after deletion
        }
    }
};
</script>
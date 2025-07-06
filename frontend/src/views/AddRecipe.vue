<template>
    <BContainer fluid class="d-flex justify-content-center align-items-start vh-100">
    <BRow class="justify-content-center w-100">
      <BCol cols="12" md="8" lg="7" class="mt-5"> <BCard title="Add New Recipe" class="shadow-lg p-4 my-5">
          <template #header>
            <h4 class="text-center mb-0">Create a New Recipe</h4>
          </template>

          <BForm @submit.prevent="addRecipe">
            <BFormGroup label="Recipe Name:" label-for="recipe-name-input" class="mb-3">
              <BFormInput
                id="recipe-name-input"
                v-model="recipe.name"
                type="text"
                placeholder="e.g., Pasta Carbonara"
                required
              ></BFormInput>
            </BFormGroup>

            <BFormGroup label="Description:" label-for="recipe-description-input" class="mb-3">
              <BFormTextarea
                id="recipe-description-input"
                v-model="recipe.description"
                placeholder="A brief description of your recipe..."
                rows="3"
              ></BFormTextarea>
            </BFormGroup>

             <BRow class="mb-3 align-items-end"> 
                <BCol cols="4" md="2"> <BFormGroup label="Hours:" label-for="cook-time-hours-input">
                  <BFormInput
                    id="cook-time-hours-input"
                    v-model.number="cookingTime.hours"
                    type="number"
                    placeholder="h"
                    min="0"
                  ></BFormInput>
                </BFormGroup>
              </BCol>
              <BCol cols="4" md="2"> <BFormGroup label="Minutes:" label-for="cook-time-minutes-input">
                  <BFormInput
                    id="cook-time-minutes-input"
                    v-model.number="cookingTime.minutes"
                    type="number"
                    placeholder="m"
                    min="0"
                    max="59"
                  ></BFormInput>
                </BFormGroup>
              </BCol>
              <BCol cols="4" md="2"> <BFormGroup label="Servings:" label-for="servings-input">
                  <BFormInput
                    id="servings-input"
                    v-model.number="recipe.servings"
                    type="number"
                    placeholder="e.g., 4"
                    min="1"
                  ></BFormInput>
                </BFormGroup>
              </BCol>
            </BRow>

            <BFormGroup label="Ingredients:" class="mb-3">
              <div v-for="(ingredient, index) in recipe.ingredients" :key="index" class="d-flex mb-2">
                <BFormInput v-model="ingredient.quantity" type="number" placeholder="Quantity" class="me-2" style="width: 25%;"></BFormInput>
                <BFormSelect v-model="ingredient.unit" :options="ingredientsUnits" placeholder="Select unit" class="me-2 form-control" style="width: 35%;">
                  <template #first>
                    <option value="" disabled>Unit</option>
                  </template>
                </BFormSelect>
                
                <BFormInput v-model="ingredient.name" placeholder="Name (e.g., Pasta)" required></BFormInput>
                <BButton variant="danger" size="sm" class="ms-2" @click="deleteIngredient(index)">-</BButton>
              </div>
              <BButton variant="info" size="sm" @click="addIngredient">Add Ingredient</BButton>
            </BFormGroup>

            <BFormGroup label="Instructions:" class="mb-4">
              <div v-for="(instruction, index) in recipe.instructions" :key="index" class="d-flex mb-2 align-items-center">
                <span class="me-2 text-muted">Step {{ instruction.order }}:</span>
                <BFormInput v-model="instruction.content" placeholder="Enter instruction details" required></BFormInput>
                <BButton variant="danger" size="sm" class="ms-2" @click="removeInstruction(index)">-</BButton>
              </div>
              <BButton variant="info" size="sm" @click="addInstruction">Add Instruction</BButton>
            </BFormGroup>

            <BButton type="submit" variant="success" class="w-100 mb-3">Add Recipe</BButton>
            <BButton variant="secondary" class="w-100" @click="cancelAdd">Cancel</BButton>
          </BForm>

          <BAlert v-if="errorMessage" show variant="danger" class="mt-3">{{ errorMessage }}</BAlert>
          <BAlert v-if="successMessage" show variant="success" class="mt-3">{{ successMessage }}</BAlert>
        </BCard>
      </BCol>
    </BRow>
  </BContainer>
</template>
<script>
import { addRecipe } from '../services/recipes';
import {
  BContainer, BRow, BCol, BCard, BForm, BFormGroup, BFormInput, BFormTextarea,
  BButton, BAlert,
  BFormSelect
} from 'bootstrap-vue-next'

export default {
    name: 'AddRecipe',
    components: {
        BContainer, BRow, BCol, BCard, BForm, BFormGroup, BFormInput, BFormTextarea,
        BButton, BAlert
    },
    data() {
        return {
            recipe: {
                name: '',
                description: '',
                ingredients: [{name: '', quantity: 0, unit: ''}],
                instructions: [{order : 0, text: ''}],
                cookTime : null,
                servings : null
            },
            errorMessage: '',
            successMessage: '',
            cookingTime: {
                hours: 0,
                minutes: 0
            },
            ingredientsUnits: [
              { text: 'grams', value: 'g' },
              { text: 'kilograms', value: 'kg' },
              { text: 'liters', value: 'l' },
              { text: 'milliliters', value: 'ml' },
              { text: 'cups', value: 'cup' },
              { text: 'tablespoons', value: 'tbsp' },
              { text: 'teaspoons', value: 'tsp' },
              { text: 'units', value: 'units'},
            ]
        }
    },
    async mounted() {
        const storedUserId = localStorage.getItem('userId');
        const storedUserToken = localStorage.getItem('token');
        if (!storedUserToken || !storedUserId) {
            this.errorMessage = 'User not logged in. Please log in to add recipes.';
            this.$router.push({ name: 'login' });
            return;
        }
    },
    methods: {
        // add a new ingredient to the list
        addIngredient() {
            this.recipe.ingredients.push({ name: '', quantity: 0, unit: '' });
        },
        // remove an ingredient from the list
        deleteIngredient(index) {
            if (this.recipe.ingredients.length > 1) {
                this.recipe.ingredients.splice(index, 1);
            }
        },
        // add a new instruction to the list, assign order based on current length
        addInstruction() {
            const newOrder = this.recipe.instructions.length + 1;
            this.recipe.instructions.push({ order: newOrder, content: '' });
        },
        removeInstruction (index) {
            if (this.recipe.instructions.length > 1) {
                this.recipe.instructions.splice(index, 1);
                // reorder instructions after deletion
                this.recipe.instructions.forEach((instruction, idx) => {
                    instruction.order = idx + 1; // Reset order based on index
                });
            }
        },
        // form submission handler
        async addRecipe() {
            this.errorMessage = '';
            this.successMessage = '';

            try {

                const filteredIngredients = this.recipe.ingredients.filter(
                    ingredient => (ingredient.name !== '') && (ingredient.quantity > 0) && ingredient.unit !== ''
                )
                if (filteredIngredients.length === 0) {
                    this.errorMessage = 'Please add at least one ingredient';
                    return;
                }

                const filteredInstructions = this.recipe.instructions.filter(
                    instruction => instruction.content  !== ''
                )
                if (filteredInstructions.length === 0) {
                    this.errorMessage = 'Please add at least one instruction';
                    return;
                }
                const recipeData = {
                    name: this.recipe.name,
                    description: this.recipe.description,
                    cookTime: this.cookingTime.hours * 60 + this.cookingTime.minutes,
                    servings: this.recipe.servings,

                    // filter out empty ingredients/instructions
                    ingredients: 
                        filteredIngredients.map(ingredient => ({
                            name: ingredient.name.trim(),
                            quantity: ingredient.quantity,
                            unit: ingredient.unit
                        })),
                    instructions: this.recipe.instructions.filter(
                        instruction => instruction.content && instruction.content.trim() !== ''
                    )
                };

                if (!recipeData.name || !recipeData.ingredients.length || !recipeData.instructions.length) {
                    this.errorMessage = 'Please fill in all required fields.';
                    return;
                }

                // call the addRecipe function to save the recipe
                const response = await addRecipe(recipeData);
                this.successMessage = response.message || 'Recipe added successfully!';
                console.log('Recipe added:', response);

                this.resetForm();
                
                // redirect the user to the recipe list
                this.$router.push({ name: 'recipe-list' });
            } catch (error) {
                console.error('Error adding recipe:', error);
                this.errorMessage = error.message || 'Failed to add recipe.';
                if (error.status === 401) {
                    this.errorMessage = 'Unauthorized access. Please log in again.';
                    localStorage.removeItem('token');
                    localStorage.removeItem('userId');
                    this.$router.push('/login'); 
                }
            }
        },
        resetForm() {
            this.recipe = {
                name: '',
                description: '',
                ingredients: [{name: '', quantity: 0, unit: ''}],
                instructions: [{order : 0, content: ''}],
                cookTime : null,
                servings : null
            };
            this.cookingTime = {
                hours: 0,
                minutes: 0
            };
            this.errorMessage = '';
            this.successMessage = '';
        },
        cancelAdd() {
            this.$router.push({ name: 'recipe-list' });
        }
    }
}
</script>
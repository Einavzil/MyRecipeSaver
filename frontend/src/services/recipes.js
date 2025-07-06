import { getAuthHeaders } from "./auth";

const API_BASE_URL = 'http://localhost:5000';

export const fetchRecipes = async (userId) => {
    try {
        const response = await fetch(`${API_BASE_URL}/recipe`, {
        method: 'GET',
        headers: getAuthHeaders()
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Failed to fetch recipes');
        }
        console.log('Fetched recipes:', data);
        return data; 
    } catch (error) {
        console.error('Error fetching recipes:', error);
        throw error;
    }
};

export const fetchSingleRecipe = async (recipeId) => { // <-- Add 'headers' parameter here
    try {
        // Use the 'headers' parameter directly
        const response = await fetch(`${API_BASE_URL}/recipe/${recipeId}`, {
            method: 'GET',
            headers: getAuthHeaders(), // <-- Use the passed 'headers' object here
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Failed to fetch recipe');
        }
        console.log('Fetched recipe:', data);
        return data;
    } catch (error) {
        console.error('Error fetching recipe:', error);
        throw error;
    }
};

export const addRecipe = async (recipeData) => {
    try {
        const response = await fetch(`${API_BASE_URL}/recipe`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(recipeData)
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error adding recipe:', error);
        throw error;
    }
};

export const updateRecipe = async (recipeId, updatedData) => {
    try {
        const response = await fetch(`${API_BASE_URL}/recipe/${recipeId}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify(updatedData)
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Failed to update recipe');
        }
        console.log('Updated recipe:', data);
        return data;
    } catch (error) {
        console.error('Error updating recipe:', error);
        throw error;
    }
};

export const deleteRecipe = async (recipeId) => {
    try {
        const response = await fetch(`${API_BASE_URL}/recipe/${recipeId}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Failed to delete recipe');
        }
        console.log('Deleted recipe:', data);
        return data;
    } catch (error) {
        console.error('Error deleting recipe:', error);
        throw error;
    }
};

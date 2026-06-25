import axios from 'axios';

/**
 * API Client — Centralized HTTP client for backend communication
 * 
 * Using axios instead of fetch() because it provides:
 * - Automatic JSON parsing
 * - Request/response interceptors
 * - Better error handling
 * - Timeout support
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Make a prediction from student data
 * @param {Object} data — Student feature values
 * @returns {Promise} — API response with prediction
 */
export const predictScore = async (data) => {
  const response = await client.post('/predict', data);
  return response.data;
};

/**
 * Get model information
 * @returns {Promise} — Model name, features, etc.
 */
export const getModelInfo = async () => {
  const response = await client.get('/models');
  return response.data;
};

/**
 * Health check
 * @returns {Promise} — Status information
 */
export const healthCheck = async () => {
  const response = await client.get('/health');
  return response.data;
};

export default client;
import axios from 'axios';

// Create an axios instance with default config
const apiClient = axios.create({
  baseURL: 'http://localhost:9575/api', // Update this with your backend URL in production
  timeout: 30000, // 30 seconds (increased for analysis operations)
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Request interceptor for adding auth token if available
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling common errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Handle HTTP errors
      console.error('API Error:', error.response.status, error.response.data);
      
      // Handle specific status codes
      if (error.response.status === 401) {
        // Handle unauthorized access
        console.error('Unauthorized access - please login');
        // You might want to redirect to login page here
      } else if (error.response.status === 404) {
        console.error('The requested resource was not found');
      } else if (error.response.status >= 500) {
        console.error('Server error occurred');
      }
    } else if (error.request) {
      // The request was made but no response was received
      console.error('No response received from server');
    } else {
      // Something happened in setting up the request
      console.error('Error setting up request:', error.message);
    }
    return Promise.reject(error);
  }
);

// API methods
export default {
  // ====== Transcript Endpoints ======
  async getTranscript(mode = 'speaker') {
    try {
      const response = await apiClient.get(`/transcript?mode=${mode}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching transcript:', error);
      throw error;
    }
  },

  // ====== Analysis Endpoints ======
  async analyzeEmotion(text, speakerId = null) {
    try {
      const response = await apiClient.post('/analyze/emotion', {
        text,
        speaker_id: speakerId,
        timestamp: Date.now() / 1000
      });
      return response.data;
    } catch (error) {
      console.error('Error analyzing emotion:', error);
      throw error;
    }
  },

  async analyzeSentiment(text, speakerId = null) {
    try {
      const response = await apiClient.post('/analyze/sentiment', {
        text,
        speaker_id: speakerId,
        timestamp: Date.now() / 1000
      });
      return response.data;
    } catch (error) {
      console.error('Error analyzing sentiment:', error);
      throw error;
    }
  },

  async generateSummary(text, speakerId = null) {
    try {
      const response = await apiClient.post('/analyze/summary', {
        text,
        speaker_id: speakerId,
        timestamp: Date.now() / 1000
      });
      return response.data;
    } catch (error) {
      console.error('Error generating summary:', error);
      throw error;
    }
  },

  async extractKeywords(text, speakerId = null) {
    try {
      const response = await apiClient.post('/analyze/keywords', {
        text,
        speaker_id: speakerId,
        timestamp: Date.now() / 1000
      });
      return response.data;
    } catch (error) {
      console.error('Error extracting keywords:', error);
      throw error;
    }
  },

  // ====== System Endpoints ======
  async getStatus() {
    try {
      const response = await apiClient.get('/status');
      return response.data;
    } catch (error) {
      console.error('Error fetching status:', error);
      throw error;
    }
  },

  async checkHealth() {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }
};

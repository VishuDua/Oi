const config = {
  api: {
    // Base URL for API requests
    baseURL: 'http://localhost:9575/api',
    
    // Timeout for API requests in milliseconds
    timeout: 10000,
    
    // Default number of retries for failed requests
    retries: 2,
    
    // Delay between retries in milliseconds
    retryDelay: 1000,
  },
  
  // WebSocket configuration (if needed)
  websocket: {
    url: 'ws://localhost:9575/ws',
    reconnectInterval: 3000,
    maxReconnectAttempts: 5,
  },
  
  // Feature flags
  features: {
    realtimeUpdates: true,
    analytics: true,
  },
  
  // UI configuration
  ui: {
    theme: 'light', // 'light' or 'dark'
    language: 'en',
    dateFormat: 'en-US',
    itemsPerPage: 10,
  },
};

export default config;

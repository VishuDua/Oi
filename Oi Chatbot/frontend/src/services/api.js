import axios from 'axios';

const TEXT_API_URL = 'http://localhost:8989';
const SPEECH_API_URL = 'http://localhost:9575';

const api = {
  // Text Generation API
  async getResponse(input) {
    try {
      const response = await axios.post(`${TEXT_API_URL}/respond`, { input });
      return response.data;
    } catch (error) {
      console.error('Error getting response:', error);
      throw error;
    }
  },

  async toggleMode() {
    try {
      const response = await axios.post(`${TEXT_API_URL}/toggle_mode`);
      return response.data;
    } catch (error) {
      console.error('Error toggling mode:', error);
      throw error;
    }
  },

  // Speech API
  async getTranscript() {
    try {
      const response = await axios.get(`${SPEECH_API_URL}/transcript?mode=plain`);
      return response.data;
    } catch (error) {
      console.error('Error getting transcript:', error);
      throw error;
    }
  },

  // WebSocket connection for real-time speech transcription
  connectSpeechWebSocket(onMessage) {
    const ws = new WebSocket(`ws://localhost:9575/ws`);
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    return ws;
  }
};

export default api; 
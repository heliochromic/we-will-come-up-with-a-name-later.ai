const API_BASE_URL = '/api';

class APIError extends Error {
  constructor(message, status, data) {
    super(message);
    this.name = 'APIError';
    this.status = status;
    this.data = data;
  }
}

const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` })
  };
};

const handleResponse = async (response) => {
  if (response.status === 204) {
    return null;
  }

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new APIError(
      data?.detail || 'An error occurred',
      response.status,
      data
    );
  }

  return data;
};

// Auth API
export const authAPI = {
  register: async (userData) => {
    const response = await fetch(`${API_BASE_URL}/users/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    });
    return handleResponse(response);
  },

  login: async (email, password) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch(`${API_BASE_URL}/users/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    });
    return handleResponse(response);
  },

  getCurrentUser: async () => {
    const response = await fetch(`${API_BASE_URL}/users/me`, {
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  updateProfile: async (userData) => {
    const response = await fetch(`${API_BASE_URL}/users/me`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(userData),
    });
    return handleResponse(response);
  },
};

// Transcript API
export const transcriptAPI = {
  create: async (videoUrl) => {
    const response = await fetch(`${API_BASE_URL}/transcripts/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ video_url: videoUrl }),
    });
    return handleResponse(response);
  },

  getById: async (transcriptId) => {
    const response = await fetch(`${API_BASE_URL}/transcripts/${transcriptId}`, {
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  getAll: async () => {
    const response = await fetch(`${API_BASE_URL}/transcripts/`, {
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },
};

// Chat API
export const chatAPI = {
  create: async (transcriptId) => {
    const response = await fetch(`${API_BASE_URL}/chats/`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ transcript_id: transcriptId }),
    });
    return handleResponse(response);
  },

  getById: async (chatId) => {
    const response = await fetch(`${API_BASE_URL}/chats/${chatId}`, {
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  getMessages: async (chatId) => {
    const response = await fetch(`${API_BASE_URL}/chats/${chatId}/messages`, {
      headers: getAuthHeaders(),
    });
    return handleResponse(response);
  },

  sendMessage: async (chatId, userMessage, provider = 'claude') => {
    const response = await fetch(`${API_BASE_URL}/chats/${chatId}/llm`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({
        user_message: userMessage,
        provider: provider
      }),
    });
    return handleResponse(response);
  },
};

export { APIError };

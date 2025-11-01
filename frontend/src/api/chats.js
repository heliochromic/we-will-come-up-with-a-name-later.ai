import { apiRequest } from './config';

export const createChat = async (transcriptId, title) => {
  return apiRequest('/api/chats/', {
    method: 'POST',
    body: JSON.stringify({ transcript_id: transcriptId, title }),
  });
};

export const getUserChats = async () => {
  return apiRequest('/api/chats/');
};

export const getChat = async (chatId) => {
  return apiRequest(`/api/chats/${chatId}`);
};

export const getChatsByTranscript = async (transcriptId) => {
  return apiRequest(`/api/chats/transcript/${transcriptId}`);
};

export const addMessage = async (chatId, content, role = 'user') => {
  return apiRequest(`/api/chats/${chatId}/messages`, {
    method: 'POST',
    body: JSON.stringify({ content, role }),
  });
};

export const getChatMessages = async (chatId) => {
  return apiRequest(`/api/chats/${chatId}/messages`);
};

export const sendMessageToLLM = async (chatId, message) => {
  return apiRequest(`/api/chats/${chatId}/llm`, {
    method: 'POST',
    body: JSON.stringify({ message }),
  });
};

export const deleteChat = async (chatId) => {
  return apiRequest(`/api/chats/${chatId}`, {
    method: 'DELETE',
  });
};

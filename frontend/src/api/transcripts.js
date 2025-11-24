import { apiRequest } from './config';

export const createTranscript = async (youtubeUrl) => {
  return apiRequest('/api/transcripts/', {
    method: 'POST',
    body: JSON.stringify({ youtube_url: youtubeUrl }),
  });
};

export const getTranscript = async (transcriptId) => {
  return apiRequest(`/api/transcripts/${transcriptId}`);
};

export const getAllTranscripts = async () => {
  return apiRequest('/api/transcripts/');
};

export const deleteTranscript = async (transcriptId) => {
  return apiRequest(`/api/transcripts/${transcriptId}`, {
    method: 'DELETE',
  });
};

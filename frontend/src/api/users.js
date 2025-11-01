import { apiRequest } from './config';

export const getUser = async (userId) => {
  return apiRequest(`/api/users/${userId}`);
};

export const updateUser = async (updateData) => {
  return apiRequest('/api/users/me', {
    method: 'PUT',
    body: JSON.stringify(updateData),
  });
};

export const deleteUser = async () => {
  return apiRequest('/api/users/me', {
    method: 'DELETE',
  });
};

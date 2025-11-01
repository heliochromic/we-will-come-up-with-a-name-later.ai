import { apiRequest } from './config';

export const login = async (email, password) => {
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);

  const response = await fetch('http://localhost:8000/api/users/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Login failed' }));
    throw new Error(error.detail || 'Login failed');
  }

  const data = await response.json();
  localStorage.setItem('token', data.access_token);
  return data;
};

export const register = async (email, password, fullName) => {
  const data = await apiRequest('/api/users/register', {
    method: 'POST',
    body: JSON.stringify({
      email,
      password,
      name: fullName,
    }),
  });

  localStorage.setItem('token', data.access_token);

  console.log(email, password, fullName)
  return data;
};

export const logout = () => {
  localStorage.removeItem('token');
};

export const getCurrentUser = async () => {
  return apiRequest('/api/users/me');
};

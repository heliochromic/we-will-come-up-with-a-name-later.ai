import { useState } from 'react';
import AuthPage from './pages/AuthPage';
import MainPage from './pages/MainPage';
import ProfilePage from './pages/ProfilePage';

export default function App() {
  const [currentPage, setCurrentPage] = useState('login');
  const [user, setUser] = useState(null);

  const handleAuth = (userData) => {
    setUser(userData);
    setCurrentPage('main');
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    setCurrentPage('login');
  };

  const handleUpdateUser = (updatedUser) => {
    setUser(updatedUser);
  };

  if (currentPage === 'login') {
    return <AuthPage onAuth={handleAuth} />;
  }

  if (currentPage === 'profile') {
    return (
      <ProfilePage
        user={user}
        onLogout={handleLogout}
        onNavigateBack={() => setCurrentPage('main')}
        onUpdateUser={handleUpdateUser}
      />
    );
  }

  return (
    <MainPage
      user={user}
      onNavigateToProfile={() => setCurrentPage('profile')}
    />
  );
}
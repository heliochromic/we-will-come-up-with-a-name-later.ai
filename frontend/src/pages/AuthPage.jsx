import { useState } from 'react';
import { FileText, Loader2 } from 'lucide-react';
import { authAPI } from '../services/api';

export default function AuthPage({ onAuth }) {
  const [isLogin, setIsLogin] = useState(true);
  const [authForm, setAuthForm] = useState({ email: '', password: '', name: '' });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAuth = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      if (isLogin) {
        const data = await authAPI.login(authForm.email, authForm.password);
        localStorage.setItem('access_token', data.access_token);
        onAuth(data.user);
      } else {
        await authAPI.register({
          email: authForm.email,
          password: authForm.password,
          name: authForm.name
        });
        const loginData = await authAPI.login(authForm.email, authForm.password);
        localStorage.setItem('access_token', loginData.access_token);
        onAuth(loginData.user);
      }
    } catch (err) {
      setError(err.message || 'Authentication failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-full mb-4">
            <FileText className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">RAG System</h1>
          <p className="text-gray-600 mt-2">
            {isLogin ? 'Welcome back!' : 'Create your account'}
          </p>
        </div>

        <form onSubmit={handleAuth} className="space-y-4">
          {error && (
            <div className="bg-red-50 text-red-600 px-4 py-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          {!isLogin && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Full Name
              </label>
              <input
                type="text"
                required={!isLogin}
                value={authForm.name}
                onChange={(e) => setAuthForm({ ...authForm, name: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
                placeholder="John Doe"
              />
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input
              type="email"
              required
              value={authForm.email}
              onChange={(e) => setAuthForm({ ...authForm, email: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              type="password"
              required
              value={authForm.password}
              onChange={(e) => setAuthForm({ ...authForm, password: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                {isLogin ? 'Signing in...' : 'Signing up...'}
              </>
            ) : (
              isLogin ? 'Sign In' : 'Sign Up'
            )}
          </button>
        </form>

        <div className="mt-6 text-center">
          <button
            onClick={() => setIsLogin(!isLogin)}
            className="w-full text-blue-600 hover:text-blue-700 text-sm font-medium"
          >
            {isLogin
              ? "Don't have an account? Sign up"
              : 'Already have an account? Sign in'}
          </button>
        </div>
      </div>
    </div>
  );
}

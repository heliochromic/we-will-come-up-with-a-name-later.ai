import { useState } from 'react';
import { LogOut, FileText, ArrowLeft, Loader2, AlertCircle } from 'lucide-react';
import { authAPI } from '../services/api';

export default function ProfilePage({ user, onLogout, onNavigateBack, onUpdateUser }) {
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [profileForm, setProfileForm] = useState({ name: user?.name || '' });
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSaveProfile = async () => {
    setIsSaving(true);
    setError('');
    setSuccess('');

    try {
      const updatedUser = await authAPI.updateProfile({
        name: profileForm.name,
        email: user?.email,
        password: user?.password
      });
      onUpdateUser(updatedUser);
      setSuccess('Profile updated successfully!');
      setIsEditingProfile(false);
    } catch (err) {
      setError(err.message || 'Failed to update profile');
    } finally {
      setIsSaving(false);
    }
  };

  const handleCancel = () => {
    setIsEditingProfile(false);
    setProfileForm({ name: user?.name || '' });
    setError('');
    setSuccess('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <nav className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <button
              onClick={onNavigateBack}
              className="flex items-center text-gray-700 hover:text-gray-900 transition-colors"
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              <FileText className="w-8 h-8 text-blue-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">RAG System</span>
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-8 py-6">
            <h1 className="text-2xl font-bold text-white">User Profile</h1>
            <p className="text-blue-100 mt-1">Manage your account settings</p>
          </div>

          <div className="p-8 space-y-8">
            <div className="flex items-center space-x-6">
              <div className="w-24 h-24 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center shadow-lg ring-4 ring-blue-100">
                <span className="text-4xl font-bold text-white">
                  {user?.name?.charAt(0).toUpperCase()}
                </span>
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-900">{user?.name}</h2>
                <p className="text-gray-600 mt-1">{user?.email}</p>
              </div>
            </div>

            <div className="border-t border-gray-200 pt-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-6">
                Account Information
              </h3>

              {error && (
                <div className="mb-4 bg-red-50 text-red-600 px-4 py-3 rounded-lg text-sm flex items-center">
                  <AlertCircle className="w-5 h-5 mr-2" />
                  {error}
                </div>
              )}

              {success && (
                <div className="mb-4 bg-green-50 text-green-600 px-4 py-3 rounded-lg text-sm">
                  {success}
                </div>
              )}

              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Full Name
                  </label>
                  {isEditingProfile ? (
                    <input
                      type="text"
                      value={profileForm.name}
                      onChange={(e) => setProfileForm({ name: e.target.value })}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 transition-shadow"
                      placeholder="Enter your full name"
                    />
                  ) : (
                    <p className="text-gray-900 text-lg">{user?.name}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email Address
                  </label>
                  <p className="text-gray-900 text-lg">{user?.email}</p>
                  <p className="text-sm text-gray-500 mt-1">Email cannot be changed</p>
                </div>
              </div>

              <div className="flex space-x-4 mt-8">
                {isEditingProfile ? (
                  <>
                    <button
                      onClick={handleSaveProfile}
                      disabled={isSaving}
                      className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                    >
                      {isSaving ? (
                        <>
                          <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                          Saving...
                        </>
                      ) : (
                        'Save Changes'
                      )}
                    </button>
                    <button
                      onClick={handleCancel}
                      disabled={isSaving}
                      className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Cancel
                    </button>
                  </>
                ) : (
                  <button
                    onClick={() => setIsEditingProfile(true)}
                    className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium shadow-md hover:shadow-lg"
                  >
                    Edit Profile
                  </button>
                )}
              </div>
            </div>

            <div className="border-t border-gray-200 pt-8">
              <button
                onClick={onLogout}
                className="flex items-center text-red-600 hover:text-red-700 font-medium transition-colors px-4 py-2 rounded-lg hover:bg-red-50"
              >
                <LogOut className="w-5 h-5 mr-2" />
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
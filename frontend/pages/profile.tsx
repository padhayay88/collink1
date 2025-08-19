import React from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';
import { useAuth } from '../lib/auth';
import { useRouter } from 'next/router';
import UserProfile from '../components/UserProfile';

const ProfilePage = () => {
  const { user, isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  // Redirect to login if not authenticated
  React.useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Will redirect
  }

  return (
    <>
      <Head>
        <title>Profile - Collink</title>
        <meta name="description" content="Your Collink profile" />
      </Head>
      
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 py-12 px-4">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-12"
          >
            <h1 className="text-4xl font-bold text-gray-900 mb-4">Your Profile</h1>
            <p className="text-xl text-gray-600">Manage your account and preferences</p>
          </motion.div>

          {/* Profile Content */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Main Profile */}
            <div className="lg:col-span-2">
              <UserProfile />
            </div>

            {/* Sidebar */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="space-y-6"
            >
              {/* Quick Stats */}
              <div className="bg-white rounded-2xl shadow-xl p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Stats</h3>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Predictions Made</span>
                    <span className="text-2xl font-bold text-blue-600">0</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Colleges Saved</span>
                    <span className="text-2xl font-bold text-purple-600">0</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Days Active</span>
                    <span className="text-2xl font-bold text-green-600">1</span>
                  </div>
                </div>
              </div>

              {/* Recent Activity */}
              <div className="bg-white rounded-2xl shadow-xl p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
                <div className="space-y-3">
                  <div className="text-sm text-gray-600">
                    <p>• Account created</p>
                    <p className="text-xs text-gray-400">Just now</p>
                  </div>
                </div>
              </div>

              {/* Quick Actions */}
              <div className="bg-white rounded-2xl shadow-xl p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
                <div className="space-y-3">
                  <button className="w-full text-left px-4 py-3 bg-blue-50 text-blue-700 hover:bg-blue-100 rounded-lg font-medium transition-colors">
                    Make a Prediction
                  </button>
                  <button className="w-full text-left px-4 py-3 bg-purple-50 text-purple-700 hover:bg-purple-100 rounded-lg font-medium transition-colors">
                    Browse Colleges
                  </button>
                  <button className="w-full text-left px-4 py-3 bg-green-50 text-green-700 hover:bg-green-100 rounded-lg font-medium transition-colors">
                    Chat with AI
                  </button>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ProfilePage;

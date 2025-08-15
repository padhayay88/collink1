import React from 'react';
import { motion } from 'framer-motion';
import { User, Mail, Phone, Settings, LogOut } from 'lucide-react';
import { useAuth } from '../lib/auth';

const UserProfile = () => {
  const { user, logout } = useAuth();

  if (!user) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-2xl shadow-xl p-6 max-w-md mx-auto"
    >
      {/* Header */}
      <div className="text-center mb-6">
        <div className="w-20 h-20 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
          <User className="w-10 h-10 text-white" />
        </div>
        <h2 className="text-2xl font-bold text-gray-900">{user.name}</h2>
        <p className="text-gray-600">Welcome to Collink!</p>
      </div>

      {/* User Info */}
      <div className="space-y-4 mb-6">
        {user.email && (
          <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
            <Mail className="w-5 h-5 text-gray-400" />
            <div>
              <p className="text-sm text-gray-500">Email</p>
              <p className="text-gray-900 font-medium">{user.email}</p>
            </div>
          </div>
        )}
        
        {user.phone && (
          <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
            <Phone className="w-5 h-5 text-gray-400" />
            <div>
              <p className="text-sm text-gray-500">Phone</p>
              <p className="text-gray-900 font-medium">{user.phone}</p>
            </div>
          </div>
        )}
      </div>

      {/* Actions */}
      <div className="space-y-3">
        <button className="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-gray-100 text-gray-700 hover:bg-gray-200 rounded-lg font-medium transition-colors">
          <Settings className="w-4 h-4" />
          <span>Account Settings</span>
        </button>
        
        <button
          onClick={logout}
          className="w-full flex items-center justify-center space-x-2 px-4 py-3 bg-red-50 text-red-600 hover:bg-red-100 rounded-lg font-medium transition-colors"
        >
          <LogOut className="w-4 h-4" />
          <span>Sign Out</span>
        </button>
      </div>
    </motion.div>
  );
};

export default UserProfile;

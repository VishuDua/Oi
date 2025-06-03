import React from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center h-screen text-center px-4">
      <motion.h1
        className="text-5xl font-bold mb-6 text-gray-800 dark:text-gray-100"
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
      >
        Welcome to OI Chatbot
      </motion.h1>
      <motion.p
        className="text-lg mb-8 text-gray-600 dark:text-gray-300 max-w-md"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1.5 }}
      >
        Your AI companion. Chat, set reminders, and more! Switch between light and dark modes for a comfortable experience.
      </motion.p>
      <motion.button
        className="px-8 py-4 bg-green-500 dark:bg-teal-500 text-white rounded-full text-xl font-semibold shadow-lg hover:bg-green-600 dark:hover:bg-teal-600 transition-colors duration-300"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => navigate('/chat')}
      >
        Get Started
      </motion.button>
    </div>
  );
}

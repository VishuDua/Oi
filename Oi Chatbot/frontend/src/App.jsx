import React, { useEffect, useState } from "react";
import { NavLink, Routes, Route, useLocation } from "react-router-dom";
import HomePage from "./pages/HomePage";
import ChatPage from "./pages/ChatPage";
import AboutPage from "./pages/AboutPage";
import RemindersPage from "./pages/RemindersPage";
import MeetingPage from "./pages/MeetingPage";
import { SunIcon, MoonIcon } from "@heroicons/react/24/outline";
import ParticlesBackground from "./components/ParticlesBackground";
import { motion } from "framer-motion";

export default function App() {
  const [theme, setTheme] = useState("dark");
  const location = useLocation();

  useEffect(() => {
    const root = window.document.documentElement;
    if (theme === "dark") {
      root.classList.remove("light");
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
      root.classList.add("light");
    }
  }, [theme]);

  const isChatPage = location.pathname === "/chat";

  return (
    <div className="relative min-h-screen flex flex-col group bg-transparent">
      <ParticlesBackground />
      <div className="relative z-10 flex flex-col flex-1">
        {/* Navbar */}
        <nav className={`fixed top-0 left-0 w-full ${
            theme === "light" ? "bg-amber-200 bg-opacity-80" : "bg-gray-900 bg-opacity-90"
          } backdrop-blur-md px-8 py-4 flex items-center justify-between z-20`}>
          {/* Animated Brand */}
          <motion.div
            className="text-2xl font-bold text-gray-800 dark:text-white tracking-wider uppercase cursor-pointer"
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ type: "spring", stiffness: 120, damping: 10, delay: 0.2 }}
            whileHover={{ scale: 1.1, color: theme === "dark" ? "#34D399" : "#B45309" }}
          >
            OI Chatbot
          </motion.div>
          {/* Menu Items */}
          <div className="flex space-x-12">
            <NavLink to="/" className={({ isActive }) =>
              isActive
                ? "text-gray-800 dark:text-white font-semibold border-b-2 border-green-500 pb-1 uppercase tracking-wide"
                : "text-gray-700 dark:text-gray-300 hover:text-gray-800 dark:hover:text-white transition-colors duration-200 uppercase tracking-wide"
            }
            >
              Home
            </NavLink>
            <NavLink to="/chat" className={({ isActive }) =>
              isActive
                ? "text-gray-800 dark:text-white font-semibold border-b-2 border-green-500 pb-1 uppercase tracking-wide"
                : "text-gray-700 dark:text-gray-300 hover:text-gray-800 dark:hover:text-white transition-colors duration-200 uppercase tracking-wide"
            }
            >
              Chat
            </NavLink>
            <NavLink to="/meeting" className={({ isActive }) =>
              isActive
                ? "text-gray-800 dark:text-white font-semibold border-b-2 border-green-500 pb-1 uppercase tracking-wide"
                : "text-gray-700 dark:text-gray-300 hover:text-gray-800 dark:hover:text-white transition-colors duration-200 uppercase tracking-wide"
            }
            >
              Meeting
            </NavLink>
            <NavLink to="/reminders" className={({ isActive }) =>
              isActive
                ? "text-gray-800 dark:text-white font-semibold border-b-2 border-green-500 pb-1 uppercase tracking-wide"
                : "text-gray-700 dark:text-gray-300 hover:text-gray-800 dark:hover:text-white transition-colors duration-200 uppercase tracking-wide"
            }
            >
              Reminders
            </NavLink>
            <NavLink to="/about" className={({ isActive }) =>
              isActive
                ? "text-gray-800 dark:text-white font-semibold border-b-2 border-green-500 pb-1 uppercase tracking-wide"
                : "text-gray-700 dark:text-gray-300 hover:text-gray-800 dark:hover:text-white transition-colors duration-200 uppercase tracking-wide"
            }
            >
              About Us
            </NavLink>
          </div>
          {/* Theme Toggle */}
          <button
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="p-2 rounded-full bg-gray-200 dark:bg-gray-800 hover:bg-gray-300 dark:hover:bg-gray-700 transition"
          >
            {theme === "dark" ? (
              <SunIcon className="h-6 w-6 text-yellow-400" />
            ) : (
              <MoonIcon className="h-6 w-6 text-gray-800" />
            )}
          </button>
        </nav>

        {/* Push content down to account for navbar height */}
        <div className="pt-24 flex-1 flex flex-col">
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/chat" element={<ChatPage />} />
              <Route path="/meeting" element={<MeetingPage />} />
              <Route path="/about" element={<AboutPage />} />
              <Route path="/reminders" element={<RemindersPage />} />
            </Routes>
          </main>
        </div>

        {/* Conditional Footer */}
        {!isChatPage && (
          <footer className="fixed bottom-0 left-0 w-full bg-gray-800 bg-opacity-90 backdrop-blur-md text-center py-2">
            <p className="text-gray-400 text-sm">
              © {new Date().getFullYear()} OI Chatbot. All rights reserved.
            </p>
          </footer>
        )}
      </div>
    </div>
  );
}
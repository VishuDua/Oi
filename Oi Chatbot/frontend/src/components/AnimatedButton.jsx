import React from "react";
import { motion } from "framer-motion";

export default function AnimatedButton({ onClick, children, className = "" }) {
  const bars = [
    { delay: 0, height: "0.4rem" },
    { delay: 0.1, height: "0.6rem" },
    { delay: 0.2, height: "0.5rem" },
    { delay: 0.3, height: "0.7rem" },
    { delay: 0.4, height: "0.35rem" }
  ];

  return (
    <button
      onClick={onClick}
      className={`relative overflow-hidden rounded-full text-green-500 dark:text-green-400
                 bg-white dark:bg-gray-800
                 border-2 border-green-500 hover:border-green-400 
                 hover:bg-green-700 hover:text-white 
                 hover:scale-105 transition transform ${className}`}
    >
      <span className="relative z-10">{children}</span>
      <div className="absolute right-4 flex space-x-1 items-end h-full">
        {bars.map((b, idx) => (
          <motion.div
            key={idx}
            initial={{ height: b.height }}
            animate={{ height: ["0.4rem", "1rem", "0.4rem"] }}
            transition={{
              repeat: Infinity,
              repeatType: "reverse",
              duration: 1,
              delay: b.delay,
              ease: "easeInOut"
            }}
            className="w-1 bg-green-500"
          />
        ))}
      </div>
    </button>
  );
}

import React, { useEffect, useRef } from "react";
import { motion } from "framer-motion";

export default function ChatInterface({ messages, isThinking, latencies }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isThinking]);

  return (
    <div className="flex-1 overflow-y-auto bg-white/30 dark:bg-gray-800/30 backdrop-blur-md p-4 rounded-xl space-y-3">
      {messages.map((msg, idx) => (
        <motion.div
          key={idx}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          whileHover={{ scale: 1.02, boxShadow: "0px 4px 8px rgba(0,0,0,0.2)" }}
          className={msg.isUser ? "flex justify-end" : "flex justify-start"}
        >
          <div className={msg.isUser ? "px-4 py-2 rounded-2xl bg-green-500 text-white max-w-xs" : "px-4 py-2 rounded-2xl bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 max-w-xs"}>
            {msg.text}
          </div>
        </motion.div>
      ))}
      {isThinking && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0. }}
          transition={{ duration: 0.3, repeat: Infinity, repeatType: "reverse" }}
          className="flex justify-start"
        >
          <div className="px-4 py-2 rounded-2xl bg-yellow-500 text-black animate-pulse">
            Thinking...
          </div>
        </motion.div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}

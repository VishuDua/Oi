import React, { useState } from "react";
import { motion } from "framer-motion";

export default function RemindersPage() {
  const [reminders, setReminders] = useState([]);
  const [title, setTitle] = useState("");
  const [date, setDate] = useState("");

  const addReminder = () => {
    if (title && date) {
      setReminders([...reminders, { title, date }]);
      setTitle("");
      setDate("");
    }
  };

  return (
    <div className="p-8 max-w-3xl mx-auto text-gray-800 dark:text-gray-200">
      <h2 className="text-3xl font-bold mb-4">Reminders</h2>
      <div className="mb-6 flex flex-col sm:flex-row sm:space-x-4">
        <input
          type="text"
          placeholder="Reminder Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="flex-1 p-2 mb-2 sm:mb-0 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded"
        />
        <input
          type="datetime-local"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          className="flex-1 p-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded"
        />
        <motion.button
          onClick={addReminder}
          className="mt-2 sm:mt-0 px-4 py-2 bg-green-500 dark:bg-teal-500 text-white rounded"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          Add
        </motion.button>
      </div>
      {reminders.length === 0 ? (
        <p className="text-gray-600 dark:text-gray-400">No reminders at the moment.</p>
      ) : (
        <ul className="space-y-2">
          {reminders.map((reminder, idx) => (
            <li key={idx} className="bg-white dark:bg-gray-700 p-4 rounded shadow flex justify-between items-center">
              <div>
                <p className="font-semibold">{reminder.title}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">{new Date(reminder.date).toLocaleString()}</p>
              </div>
              <button
                onClick={() => setReminders(reminders.filter((_, i) => i !== idx))}
                className="text-red-500 hover:text-red-700 transition"
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

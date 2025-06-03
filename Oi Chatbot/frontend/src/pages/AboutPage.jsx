import React from "react";

export default function AboutPage() {
  return (
    <div className="p-8 max-w-3xl mx-auto text-gray-800 dark:text-gray-200">
      <h2 className="text-3xl font-bold mb-4">About OI Chatbot</h2>
      <p className="mb-4">
        OI Chatbot is an interactive AI-powered assistant designed to help you chat, set reminders, and stay organized. It features voice input, dynamic backgrounds, and a sleek user interface that adapts to light and dark modes for comfortable viewing.
      </p>
      <h3 className="text-2xl font-semibold mb-2">Our Team</h3>
      <ul className="list-disc list-inside mb-4">
        <li><strong>Shivang Ayar</strong>: Frontend Developer</li>
        <li><strong>Vishu Dua</strong>: AI Developer</li>
      </ul>
      <p>
        We strive to deliver a top-notch AI experience with polished design and seamless functionality. Thank you for using OI Chatbot!
      </p>
    </div>
  );
}

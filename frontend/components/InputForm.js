import React, { useState } from "react";

export default function InputForm({ onSubmit }) {
  const [inputText, setInputText] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputText.trim()) {
      onSubmit(inputText);
      setInputText("");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div class="mb-4">
        <label htmlFor="inputText" class="block text-gray-600 font-medium mb-2">Enter a time expression:</label>
        <input 
          id="inputText"
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)} 
          placeholder="e.g., Let's meet next Tuesday" 
          class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>
      <button 
        type="submit" 
        class="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition duration-200">
        Parse
      </button>
    </form>
  );
}

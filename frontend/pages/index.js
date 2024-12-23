import React, { useState } from "react";
import InputForm from "../components/InputForm";

export default function Home() {
  const [result, setResult] = useState("");

  const handleSubmit = async (inputText) => {
    try {
      const response = await fetch("/api/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText }),
      });
      const data = await response.json();
      setResult(data.result || "No valid date found");
    } catch (error) {
      setResult("Error processing input");
    }
  };

  return (
    <div className="bg-gray-100 min-h-screen flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-lg p-8 w-full max-w-md">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-6">
          Time Expression Parser
        </h1>
        <InputForm onSubmit={handleSubmit} />
        {result && (
          <div className="mt-4 p-4 bg-gray-50 border-l-4 border-blue-400 text-blue-700">
            {result}
          </div>
        )}
      </div>
    </div>
  );
}

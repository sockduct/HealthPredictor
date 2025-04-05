'use client';

import React, { useState } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';

const Results: React.FC = () => {
  const searchParams = useSearchParams();
  const prediction = searchParams.get('prediction');

  const [userInput, setUserInput] = useState('');
  const [chatMessages, setChatMessages] = useState([
    { sender: 'bot', text: 'Hello! I am here to help. Ask me anything about your results.' }
  ]);
    
  const handleSendMessage = async () => {
    if (userInput.trim() === '') return;
  
    const newMessages = [...chatMessages, { sender: 'user', text: userInput }];
    setChatMessages(newMessages);
  
    try {
      
      const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
      });
  
      const data = await response.json();
  
      setChatMessages([
        ...newMessages,
        {
          sender: 'bot',
          text: data.response || 'Sorry, no response received.',
        },
      ]);
    } catch (error) {
      setChatMessages([
        ...newMessages,
        { sender: 'bot', text: 'Error communicating with server.' },
      ]);
    }
  
    setUserInput('');
  };
  
  return (
    <div className="bg-gradient-to-r from-yellow-600 to-indigo-700 min-h-screen text-white flex flex-col items-center px-4 py-16">
      <div className="text-center max-w-4xl mx-auto mb-16">
        <h1 className="text-4xl font-extrabold mb-6">Prediction Result</h1>
        <p className="text-xl mb-4">Based on the medical data you uploaded, our model predicts:</p>
        <div
          className={`text-6xl font-bold ${prediction === '0' ? 'text-green-500' : 'text-red-500'}`}
        >
          {prediction === '1' ? 'Yes' : 'No'}
        </div>
      </div>
    
      <div className="w-full max-w-3xl mx-auto bg-white p-6 rounded-lg shadow-lg text-gray-800">
        <h2 className="text-2xl font-semibold mb-4">AI Chat</h2>
        <div className="space-y-4 mb-4 h-[450px] overflow-auto p-2 border border-gray-300 rounded-lg">
          {chatMessages.map((msg, index) => (
            <div
              key={index}
              className={`${
                msg.sender === 'user' ? 'text-right' : 'text-left'
              }`}
            >
              <div
                className={`inline-block ${
                  msg.sender === 'user' ? 'bg-teal-500 text-white' : 'bg-gray-200 text-gray-700'
                } p-3 rounded-lg`}
              >
                {msg.text}
              </div>
            </div>
          ))}
        </div>
        <div className="flex">
          <input
            type="text"
            className="flex-1 p-2 border border-gray-300 rounded-l-md"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder="Ask something..."
          />
          <button
            onClick={handleSendMessage}
            className="bg-teal-500 text-white p-2 rounded-r-md"
          >
            Send
          </button>
        </div>
      </div>

      <div className="mt-6">
        <Link href="/">
          <button className="bg-teal-500 text-white px-6 py-3 rounded-lg text-lg font-semibold shadow-md hover:bg-teal-400">
            Go Back to Home
          </button>
        </Link>
      </div>
    </div>
  );
};

export default Results;

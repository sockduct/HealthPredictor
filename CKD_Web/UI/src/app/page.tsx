'use client';

import { useRouter } from 'next/navigation';
import React, { useState } from 'react';
import axios from 'axios';
import error from 'next/error';

const Home: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  const [formData, setFormData] = useState({
    specific_gravity: '1.010',
    albumin: '3.0',
    hemoglobin: '10.8',
    hypertension: '1',
    serum_creatinine: '2.7',
    sodium: '131.0',
    white_blood_cell_count: '4500.0',
    blood_glucose_random: '380.0',
    packed_cell_volume: '32',
    age: '63',

    // // No ckd
    // specific_gravity: '1.025',
    // albumin: '0.0',
    // hemoglobin: '15.8',
    // hypertension: '0',
    // serum_creatinine: '1.1',
    // sodium: '141.0',
    // white_blood_cell_count: '6800.0',
    // blood_glucose_random: '131.0',
    // packed_cell_volume: '53',
    // age: '58',
  });


  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();

  const handleFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
  };

  const validateForm = () => {
    return Object.values(formData).every((value) => value.trim() !== '');
  };

  const handleFileSubmit = async () => {
    if (validateForm()) {
      console.log('Form Data:', formData);
      setIsSubmitting(true);

      try{
        const data = {
          specific_gravity: formData.specific_gravity,
          albumin: formData.albumin,
          hemoglobin: formData.hemoglobin,
          hypertension: formData.hypertension,
          serum_creatinine: formData.serum_creatinine,
          sodium: formData.sodium,
          white_blood_cell_count: formData.white_blood_cell_count,
          blood_glucose_random: formData.blood_glucose_random,
          packed_cell_volume: formData.packed_cell_volume,
          age: formData.age
        };

        const response = await axios.post('http://localhost:5050/predict', data, {withCredentials: true});
        const prediction = response.data.prediction;

        router.push(`/results?prediction=${prediction}`);
      } catch{
        console.error('Error making prediction:', error);
        alert('Error making prediction');
      } finally{
        setIsSubmitting(false);
      }
    } else {
      alert('Please fill all fields before submitting.');
    }
  };

  return (
    <div className="bg-gradient-to-r from-yellow-600 to-indigo-700 min-h-screen text-white flex flex-col justify-center items-center px-4 py-16 relative overflow-hidden">
      <div className="absolute inset-0 z-0">
        <svg className="w-full h-full" viewBox="0 0 500 500" preserveAspectRatio="none">
          <path
            d="M0 250 Q 100 200, 150 250 T 300 250 T 450 250 T 500 250"
            fill="transparent"
            stroke="#ffffff33"
            strokeWidth="4"
            strokeLinecap="round"
            className="animate-line"
          />
        </svg>
      </div>

      <div className="z-10 text-center max-w-4xl mx-auto">
        <h1 className="text-5xl font-extrabold leading-tight mb-6">
          Chronic Kidney Disease Prediction
        </h1>
        <p className="text-lg mb-8">
          Fill the required medical data to receive a prediction on whether you may be at risk of chronic kidney disease.
        </p>
        <p className="text-xl mb-12 opacity-80">
          Our machine learning model analyzes your health data with precision, providing insights into your kidney health.
        </p>

        <button
          onClick={() => setIsModalOpen(true)}
          className="bg-teal-500 text-white px-8 py-4 rounded-lg text-lg font-semibold shadow-md transform transition duration-300 ease-in-out hover:scale-105 hover:bg-teal-400 focus:outline-none focus:ring-4 focus:ring-teal-300"
        >
          Upload Medical Data
        </button>
      </div>

      {isModalOpen && (
        <div
          className="fixed inset-0 backdrop-blur-sm flex justify-center items-center z-50 transition-all duration-300"
          onClick={handleModalClose}
        >
          <div
            className="bg-white text-gray-800 p-8 rounded-lg w-96 shadow-lg"
            onClick={(e) => e.stopPropagation()}
          >
            <h2 className="text-2xl font-bold mb-6">Upload Medical Data</h2>

            <form className="space-y-4">
              {Object.keys(formData).map((key) => (
                <div key={key}>
                  <label htmlFor={key} className="block text-sm font-semibold mb-2">
                    {key.replace('_', ' ').toUpperCase()}
                  </label>
                  <input
                    type="text"
                    id={key}
                    name={key}
                    value={formData[key as keyof typeof formData]}
                    onChange={handleFormChange}
                    required
                    className="w-full p-2 border border-gray-300 rounded-md"
                  />
                </div>
              ))}
            </form>

            <div className="flex justify-between mt-4">
              <button
                onClick={handleFileSubmit}
                className="bg-teal-500 text-white py-2 px-4 rounded-md hover:bg-teal-400"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Predicting...' : 'Predict'}
              </button>
              <button
                onClick={handleModalClose}
                className="bg-red-500 text-white py-2 px-4 rounded-md hover:bg-red-400"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="mt-24 max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-16 z-10">
        <div className="bg-white text-gray-800 p-8 rounded-lg shadow-lg">
          <h3 className="text-2xl font-semibold mb-4">Why Choose Us?</h3>
          <p className="text-lg">
            Our system offers accurate predictions based on your medical data and provides actionable insights to help you monitor your kidney health over time.
          </p>
        </div>
        <div className="bg-white text-gray-800 p-8 rounded-lg shadow-lg">
          <h3 className="text-2xl font-semibold mb-4">How It Works</h3>
          <p className="text-lg">
            Simply fill your medical data in form, and our AI-powered prediction model will analyze it to provide you with a risk assessment for chronic kidney disease.
          </p>
        </div>
      </div>

      <footer className="mt-24 text-center opacity-70">
        <p>&copy; 2025 Chronic Kidney Disease Prediction App. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Home;

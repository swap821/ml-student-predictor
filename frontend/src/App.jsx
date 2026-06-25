import { useState } from 'react';
import axios from 'axios';
import InputForm from './components/InputForm';
import ResultCard from './components/ResultCard';
import ModelInfo from './components/ModelInfo';
import Footer from './components/Footer';

/**
 * App.jsx — Main Application Component
 * 
 * This is the root component that manages the application state:
 * - formData: The student's input data
 * - prediction: The predicted exam score from the API
 * - loading: Whether a prediction request is in progress
 * - error: Any error that occurred during the request
 */
function App() {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Handle form submission — send data to Flask API
   * 
   * This function is called when the user submits the form.
   * It makes a POST request to the Flask backend with the student data.
   */
  const handlePredict = async (formData) => {
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      // Convert form values to the correct types (numbers vs strings)
      const processedData = {};
      for (const [key, value] of Object.entries(formData)) {
        // Try to convert to number, keep as string if it fails
        const num = Number(value);
        processedData[key] = isNaN(num) ? value : num;
      }

      // Send request to Flask API
      const response = await axios.post(
        'http://localhost:5000/predict',
        processedData
      );

      setPrediction(response.data);
    } catch (err) {
      setError(
        err.response?.data?.message || 
        'Failed to get prediction. Is the backend running?'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0b10] text-white">
      {/* Navbar */}
      <nav className="border-b border-white/10 bg-[#10121a]/80 backdrop-blur-md">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold tracking-tight">
            Student <span className="text-blue-400">Predictor</span>
          </h1>
          <a
            href="https://github.com/swap821/ml-student-predictor"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-gray-400 hover:text-white transition-colors"
          >
            View on GitHub
          </a>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-6 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h2 className="text-4xl md:text-5xl font-extrabold mb-4 tracking-tight">
            Student Performance{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">
              Predictor
            </span>
          </h2>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto">
            AI-powered exam score prediction using Random Forest, XGBoost, and Linear Regression.
            Enter student details below to get an instant prediction.
          </p>
        </div>

        {/* Form + Results Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Input Form */}
          <div className="lg:col-span-2">
            <InputForm
              onSubmit={handlePredict}
              loading={loading}
            />
          </div>

          {/* Results Sidebar */}
          <div className="space-y-6">
            {error && (
              <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-red-400">
                {error}
              </div>
            )}
            <ResultCard prediction={prediction} loading={loading} />
            <ModelInfo />
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;
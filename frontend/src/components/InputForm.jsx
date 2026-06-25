/**
 * InputForm.jsx — Student Data Input Form
 * 
 * A comprehensive form with 19 input fields matching the dataset features.
 * Collects all student information needed for the ML model to make a prediction.
 */

import { useState } from 'react';

// Define all form fields with their types and options
const FORM_FIELDS = [
  // Numerical inputs
  { name: 'Hours_Studied', label: 'Hours Studied (per day)', type: 'number', min: 0, max: 12 },
  { name: 'Attendance', label: 'Attendance (%)', type: 'number', min: 0, max: 100 },
  { name: 'Sleep_Hours', label: 'Sleep Hours (per night)', type: 'number', min: 4, max: 10 },
  { name: 'Previous_Scores', label: 'Previous Scores (0-100)', type: 'number', min: 0, max: 100 },
  { name: 'Tutoring_Sessions', label: 'Tutoring Sessions (per week)', type: 'number', min: 0, max: 8 },
  { name: 'Physical_Activity', label: 'Physical Activity (hours/week)', type: 'number', min: 0, max: 6 },
  
  // Categorical selects
  { name: 'Parental_Involvement', label: 'Parental Involvement', type: 'select', options: ['Low', 'Medium', 'High'] },
  { name: 'Access_to_Resources', label: 'Access to Resources', type: 'select', options: ['Low', 'Medium', 'High'] },
  { name: 'Motivation_Level', label: 'Motivation Level', type: 'select', options: ['Low', 'Medium', 'High'] },
  { name: 'Family_Income', label: 'Family Income', type: 'select', options: ['Low', 'Medium', 'High'] },
  { name: 'Teacher_Quality', label: 'Teacher Quality', type: 'select', options: ['Low', 'Medium', 'High'] },
  { name: 'Peer_Influence', label: 'Peer Influence', type: 'select', options: ['Positive', 'Neutral', 'Negative'] },
  { name: 'Extracurricular_Activities', label: 'Extracurricular Activities', type: 'select', options: ['Yes', 'No'] },
  { name: 'Internet_Access', label: 'Internet Access', type: 'select', options: ['Yes', 'No'] },
  { name: 'Learning_Disabilities', label: 'Learning Disabilities', type: 'select', options: ['Yes', 'No'] },
  { name: 'Distance_from_Home', label: 'Distance from Home', type: 'select', options: ['Near', 'Moderate', 'Far'] },
  { name: 'Gender', label: 'Gender', type: 'select', options: ['Male', 'Female'] },
  { name: 'School_Type', label: 'School Type', type: 'select', options: ['Public', 'Private'] },
  { name: 'Parental_Education_Level', label: 'Parental Education', type: 'select', options: ['High School', 'College', 'Postgraduate'] },
];

const InputForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({});

  const handleChange = (name, value) => {
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-[#10121a] border border-white/10 rounded-2xl p-6">
      <h3 className="text-xl font-bold mb-6">Student Information</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {FORM_FIELDS.map((field) => (
          <div key={field.name} className="space-y-1">
            <label className="text-sm text-gray-400 block">
              {field.label}
            </label>
            
            {field.type === 'number' ? (
              <input
                type="number"
                min={field.min}
                max={field.max}
                value={formData[field.name] || ''}
                onChange={(e) => handleChange(field.name, e.target.value)}
                className="w-full bg-[#0a0b10] border border-white/10 rounded-lg px-4 py-2 text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                required
              />
            ) : (
              <select
                value={formData[field.name] || ''}
                onChange={(e) => handleChange(field.name, e.target.value)}
                className="w-full bg-[#0a0b10] border border-white/10 rounded-lg px-4 py-2 text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                required
              >
                <option value="">Select...</option>
                {field.options.map((opt) => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
            )}
          </div>
        ))}
      </div>

      <button
        type="submit"
        disabled={loading}
        className="mt-6 w-full bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 text-white font-bold py-3 px-6 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? 'Predicting...' : 'Predict Exam Score'}
      </button>
    </form>
  );
};

export default InputForm;
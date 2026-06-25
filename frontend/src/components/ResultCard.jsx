/**
 * ResultCard.jsx — Prediction Result Display
 * 
 * Displays the predicted exam score with a color-coded visual indicator.
 * Green for high scores (90+), yellow for medium (70-89), red for low (<70).
 */

const ResultCard = ({ prediction, loading }) => {
  if (loading) {
    return (
      <div className="bg-[#10121a] border border-white/10 rounded-2xl p-6 text-center">
        <div className="animate-pulse">
          <div className="h-16 bg-white/10 rounded-lg mb-4"></div>
          <div className="h-4 bg-white/10 rounded w-3/4 mx-auto"></div>
        </div>
      </div>
    );
  }

  if (!prediction) {
    return (
      <div className="bg-[#10121a] border border-white/10 rounded-2xl p-6 text-center text-gray-500">
        <p>Fill in the form and click "Predict" to see the result</p>
      </div>
    );
  }

  const score = prediction.prediction;
  
  // Color code the score
  const getColor = (s) => {
    if (s >= 90) return 'text-green-400';
    if (s >= 70) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getBgColor = (s) => {
    if (s >= 90) return 'bg-green-500/10 border-green-500/30';
    if (s >= 70) return 'bg-yellow-500/10 border-yellow-500/30';
    return 'bg-red-500/10 border-red-500/30';
  };

  return (
    <div className={`${getBgColor(score)} border rounded-2xl p-6`}>
      <p className="text-sm text-gray-400 mb-2">Predicted Exam Score</p>
      <p className={`text-5xl font-extrabold ${getColor(score)}`}>
        {score}
      </p>
      <p className="text-sm text-gray-400 mt-2">
        Model: {prediction.model_used}
      </p>
    </div>
  );
};

export default ResultCard;
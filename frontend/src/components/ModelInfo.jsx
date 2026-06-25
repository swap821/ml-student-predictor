/**
 * ModelInfo.jsx — Model Information Card
 * 
 * Displays information about the ML model being used.
 */

const ModelInfo = () => {
  return (
    <div className="bg-[#10121a] border border-white/10 rounded-2xl p-6">
      <h4 className="font-bold mb-4">How It Works</h4>
      <div className="space-y-3 text-sm text-gray-400">
        <div className="flex items-start gap-3">
          <div className="w-6 h-6 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center text-xs font-bold flex-shrink-0">1</div>
          <p>You enter 19 student features (study hours, attendance, etc.)</p>
        </div>
        <div className="flex items-start gap-3">
          <div className="w-6 h-6 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center text-xs font-bold flex-shrink-0">2</div>
          <p>Data is preprocessed (encoded, scaled) the same way as training data</p>
        </div>
        <div className="flex items-start gap-3">
          <div className="w-6 h-6 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center text-xs font-bold flex-shrink-0">3</div>
          <p>The trained ML model (Random Forest/XGBoost) makes a prediction</p>
        </div>
        <div className="flex items-start gap-3">
          <div className="w-6 h-6 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center text-xs font-bold flex-shrink-0">4</div>
          <p>You get a predicted exam score (0-100)</p>
        </div>
      </div>
    </div>
  );
};

export default ModelInfo;
import React from "react";
import { PredictionResponse } from "@/types/weather";
import { Sparkles, ThermometerSun, CloudRain, ShieldAlert, Info } from "lucide-react";

interface PredictionCardProps {
  prediction: PredictionResponse;
}

export const PredictionCard: React.FC<PredictionCardProps> = ({ prediction }) => {
  const getRiskColor = (risk: string) => {
    switch (risk) {
      case "LOW":
        return {
          badge: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
          glow: "from-emerald-500/20 to-teal-500/10",
          text: "text-emerald-400"
        };
      case "MODERATE":
        return {
          badge: "bg-amber-500/10 text-amber-400 border-amber-500/30",
          glow: "from-amber-500/20 to-orange-500/10",
          text: "text-amber-400"
        };
      case "HIGH":
        return {
          badge: "bg-orange-500/10 text-orange-400 border-orange-500/30",
          glow: "from-orange-500/20 to-red-500/10",
          text: "text-orange-400"
        };
      case "VERY HIGH":
        return {
          badge: "bg-rose-500/15 text-rose-400 border-rose-500/30 animate-pulse",
          glow: "from-rose-500/25 to-red-600/15",
          text: "text-rose-400"
        };
      default:
        return {
          badge: "bg-cyan-500/10 text-cyan-400 border-cyan-500/30",
          glow: "from-cyan-500/20 to-blue-500/10",
          text: "text-cyan-400"
        };
    }
  };

  const riskStyle = getRiskColor(prediction.risk_level);

  return (
    <div className={`relative overflow-hidden bg-slate-900/80 backdrop-blur-xl border border-slate-800 rounded-2xl p-6 shadow-2xl bg-gradient-to-br ${riskStyle.glow}`}>
      {/* Background Accent Decorative Blur */}
      <div className="absolute -right-12 -top-12 w-48 h-48 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="flex items-center justify-between pb-4 border-b border-slate-800/80 mb-6">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 bg-gradient-to-tr from-cyan-500 to-indigo-600 rounded-lg text-white shadow-md">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white tracking-wide">Tomorrow's AI Prediction</h2>
            <p className="text-xs text-slate-400">Random Forest Machine Learning Inference</p>
          </div>
        </div>

        <span className={`px-3.5 py-1 rounded-full text-xs font-semibold border ${riskStyle.badge} uppercase tracking-wider flex items-center gap-1.5`}>
          <ShieldAlert className="w-3.5 h-3.5" />
          Risk: {prediction.risk_level}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Temperature Prediction Card */}
        <div className="bg-slate-800/50 border border-slate-700/60 rounded-xl p-5 relative overflow-hidden group hover:border-slate-600 transition-colors">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Predicted Max Temp</span>
            <div className="p-2 bg-amber-500/10 rounded-lg border border-amber-500/20">
              <ThermometerSun className="w-5 h-5 text-amber-400" />
            </div>
          </div>
          <div className="flex items-baseline space-x-2">
            <span className="text-4xl font-extrabold text-white tracking-tight">
              {prediction.predicted_temp_max.toFixed(1)}°C
            </span>
            <span className="text-xs text-slate-400 font-mono">Regressor Model</span>
          </div>
          <p className="text-xs text-slate-400 mt-2">Targeted peak daytime temperature for tomorrow.</p>
        </div>

        {/* Rain Probability Card */}
        <div className="bg-slate-800/50 border border-slate-700/60 rounded-xl p-5 relative overflow-hidden group hover:border-slate-600 transition-colors">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Rain Probability</span>
            <div className="p-2 bg-blue-500/10 rounded-lg border border-blue-500/20">
              <CloudRain className="w-5 h-5 text-blue-400" />
            </div>
          </div>
          <div className="flex items-baseline space-x-2">
            <span className="text-4xl font-extrabold text-white tracking-tight">
              {prediction.rain_probability_percent}%
            </span>
            <span className="text-xs text-slate-400 font-mono">({prediction.rain_probability.toFixed(2)})</span>
          </div>
          {/* Progress bar */}
          <div className="w-full bg-slate-700/60 h-2 rounded-full mt-3 overflow-hidden">
            <div
              className="bg-gradient-to-r from-blue-500 to-cyan-400 h-full rounded-full transition-all duration-700 ease-out"
              style={{ width: `${Math.min(prediction.rain_probability_percent, 100)}%` }}
            />
          </div>
        </div>
      </div>

      {/* Weather Advice Section */}
      <div className="mt-6 bg-slate-800/80 border border-slate-700/80 rounded-xl p-4 flex items-start space-x-3">
        <div className="p-2 bg-cyan-500/10 rounded-lg border border-cyan-500/20 shrink-0 mt-0.5">
          <Info className="w-4 h-4 text-cyan-400" />
        </div>
        <div>
          <h4 className="text-xs font-semibold uppercase tracking-wider text-cyan-400">AI Weather Advice</h4>
          <p className="text-sm font-medium text-slate-100 mt-0.5 leading-relaxed">{prediction.advice}</p>
        </div>
      </div>
    </div>
  );
};

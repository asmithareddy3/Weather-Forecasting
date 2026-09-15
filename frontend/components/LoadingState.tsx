import React from "react";
import { Loader2, Sparkles } from "lucide-react";

export const LoadingState: React.FC = () => {
  return (
    <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 flex flex-col items-center justify-center min-h-[60vh]">
      <div className="relative flex items-center justify-center">
        <div className="absolute w-24 h-24 bg-cyan-500/20 rounded-full blur-xl animate-pulse" />
        <div className="p-4 bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl relative z-10">
          <Loader2 className="w-10 h-10 text-cyan-400 animate-spin" />
        </div>
      </div>
      <h3 className="text-xl font-bold text-white mt-6 tracking-wide flex items-center gap-2">
        Fetching Weather & Running AI Models <Sparkles className="w-4 h-4 text-cyan-400 animate-bounce" />
      </h3>
      <p className="text-sm text-slate-400 mt-2 text-center max-w-md">
        Connecting to Open-Meteo API and running Random Forest regressors/classifiers...
      </p>

      {/* Skeleton placeholders */}
      <div className="w-full grid grid-cols-1 md:grid-cols-3 gap-6 mt-10">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-36 bg-slate-900/40 border border-slate-800 rounded-2xl animate-pulse p-4 flex flex-col justify-between">
            <div className="h-4 bg-slate-800 rounded w-1/3" />
            <div className="h-8 bg-slate-800 rounded w-1/2" />
            <div className="h-3 bg-slate-800 rounded w-2/3" />
          </div>
        ))}
      </div>
    </div>
  );
};

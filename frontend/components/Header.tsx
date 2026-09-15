import React from "react";
import { CloudSun, MapPin, Sparkles } from "lucide-react";

export const Header: React.FC = () => {
  return (
    <header className="w-full bg-slate-900/80 backdrop-blur-md border-b border-slate-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 bg-gradient-to-tr from-cyan-500 to-blue-600 rounded-xl shadow-lg shadow-cyan-500/20">
            <CloudSun className="w-7 h-7 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-cyan-400 tracking-tight">
                WeatherAI
              </h1>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                <Sparkles className="w-3 h-3 mr-1" /> AI Powered
              </span>
            </div>
            <p className="text-xs text-slate-400">Accessible AI Weather Forecasting System</p>
          </div>
        </div>

        <div className="flex items-center space-x-2 bg-slate-800/80 border border-slate-700/60 px-3.5 py-1.5 rounded-full text-sm text-slate-200 shadow-inner">
          <MapPin className="w-4 h-4 text-cyan-400 animate-pulse" />
          <span className="font-medium text-xs sm:text-sm">Chennai, Tamil Nadu, India</span>
        </div>
      </div>
    </header>
  );
};

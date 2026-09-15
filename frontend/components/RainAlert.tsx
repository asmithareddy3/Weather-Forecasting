import React from "react";
import { AlertTriangle, Umbrella } from "lucide-react";

interface RainAlertProps {
  riskLevel: string;
  advice: string;
}

export const RainAlert: React.FC<RainAlertProps> = ({ riskLevel, advice }) => {
  if (riskLevel !== "HIGH" && riskLevel !== "VERY HIGH") {
    return null;
  }

  const isVeryHigh = riskLevel === "VERY HIGH";

  return (
    <div
      role="alert"
      aria-live="assertive"
      className={`w-full rounded-2xl p-5 border shadow-2xl transition-all duration-300 ${
        isVeryHigh
          ? "bg-rose-950/70 border-rose-600/60 text-rose-200 shadow-rose-950/50 animate-pulse"
          : "bg-orange-950/70 border-orange-600/60 text-orange-200 shadow-orange-950/50"
      }`}
    >
      <div className="flex items-start space-x-4">
        <div
          className={`p-3 rounded-xl shrink-0 ${
            isVeryHigh ? "bg-rose-600 text-white" : "bg-orange-600 text-white"
          }`}
        >
          <AlertTriangle className="w-6 h-6" />
        </div>
        <div className="flex-1">
          <div className="flex items-center space-x-2">
            <h3 className="text-lg font-extrabold tracking-wide uppercase">
              Rain Warning Alert: {riskLevel} RISK
            </h3>
            <Umbrella className="w-5 h-5 text-current animate-bounce" />
          </div>
          <p className="text-sm font-medium mt-1 text-slate-200 leading-relaxed">
            {advice}
          </p>
          <p className="text-xs opacity-80 mt-2 font-mono">
            Location: Chennai, India | Action Advised: Take precautions before traveling.
          </p>
        </div>
      </div>
    </div>
  );
};

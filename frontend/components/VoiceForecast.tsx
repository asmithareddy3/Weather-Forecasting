"use client";

import React, { useState, useEffect } from "react";
import { PredictionResponse } from "@/types/weather";
import { Volume2, VolumeX, Mic, CheckCircle2 } from "lucide-react";

interface VoiceForecastProps {
  prediction: PredictionResponse;
  cityName?: string;
}

export const VoiceForecast: React.FC<VoiceForecastProps> = ({
  prediction,
  cityName = "Chennai"
}) => {
  const [isSupported, setIsSupported] = useState<boolean>(true);
  const [isSpeaking, setIsSpeaking] = useState<boolean>(false);
  const [voiceEnabled, setVoiceEnabled] = useState<boolean>(false);

  useEffect(() => {
    if (typeof window !== "undefined" && !("speechSynthesis" in window)) {
      setIsSupported(false);
    }
  }, []);

  const buildSpeechText = (): string => {
    const riskPhrase = prediction.risk_level.toLowerCase();
    return `Tomorrow in ${cityName}, the predicted maximum temperature is ${prediction.predicted_temp_max} degrees Celsius. The estimated probability of rain is ${prediction.rain_probability_percent} percent. Rain risk is ${riskPhrase}. ${prediction.advice}`;
  };

  const speakForecast = () => {
    if (!isSupported || typeof window === "undefined") return;

    window.speechSynthesis.cancel(); // Stop any existing speech

    const text = buildSpeechText();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.95; // Slightly slower for speech accessibility clarity
    utterance.pitch = 1.0;

    utterance.onstart = () => {
      setIsSpeaking(true);
    };

    utterance.onend = () => {
      setIsSpeaking(false);
    };

    utterance.onerror = (e) => {
      console.error("SpeechSynthesis error:", e);
      setIsSpeaking(false);
    };

    window.speechSynthesis.speak(utterance);
    setVoiceEnabled(true);
  };

  const stopSpeech = () => {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
    setIsSpeaking(false);
  };

  const toggleVoice = () => {
    if (isSpeaking) {
      stopSpeech();
    } else {
      speakForecast();
    }
  };

  if (!isSupported) {
    return (
      <div className="bg-slate-900/40 border border-slate-800 rounded-xl p-4 text-xs text-slate-400 flex items-center space-x-2">
        <VolumeX className="w-4 h-4 text-slate-500" />
        <span>Browser SpeechSynthesis is not supported on this device.</span>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-r from-cyan-950/60 to-blue-950/60 border border-cyan-800/40 rounded-2xl p-5 shadow-xl flex flex-col sm:flex-row items-center justify-between gap-4">
      <div className="flex items-center space-x-3">
        <div className={`p-3 rounded-xl ${isSpeaking ? "bg-cyan-500 text-white animate-bounce" : "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20"}`}>
          <Mic className="w-6 h-6" />
        </div>
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            Screen Reader & Voice Accessibility
            {voiceEnabled && (
              <span className="text-xs text-emerald-400 font-normal flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" /> Active
              </span>
            )}
          </h3>
          <p className="text-xs text-slate-300 mt-0.5">
            Click below to hear an auditory audio forecast generated for visually impaired users.
          </p>
        </div>
      </div>

      <button
        onClick={toggleVoice}
        aria-label={isSpeaking ? "Stop voice forecast audio" : "Enable and play voice forecast audio"}
        className={`px-5 py-2.5 rounded-xl font-semibold text-sm transition-all duration-200 shadow-lg flex items-center space-x-2 shrink-0 ${
          isSpeaking
            ? "bg-rose-600 hover:bg-rose-500 text-white shadow-rose-600/30"
            : "bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white shadow-cyan-500/25 hover:scale-105"
        }`}
      >
        {isSpeaking ? (
          <>
            <VolumeX className="w-4 h-4" />
            <span>Stop Voice Forecast</span>
          </>
        ) : (
          <>
            <Volume2 className="w-4 h-4" />
            <span>Enable Voice Forecast</span>
          </>
        )}
      </button>
    </div>
  );
};

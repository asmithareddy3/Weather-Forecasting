import React from "react";
import { CurrentWeatherData } from "@/types/weather";
import { Thermometer, Droplets, CloudRain, Wind, Gauge, Cloud } from "lucide-react";

interface WeatherCardProps {
  weather: CurrentWeatherData;
}

export const WeatherCard: React.FC<WeatherCardProps> = ({ weather }) => {
  const metrics = [
    {
      id: "temp",
      label: "Today's Temperature",
      value: `${weather.temp_max.toFixed(1)}°C`,
      subText: `Min ${weather.temp_min.toFixed(1)}°C | Mean ${weather.temp_mean.toFixed(1)}°C`,
      icon: Thermometer,
      color: "text-amber-400",
      bgColor: "bg-amber-500/10",
      borderColor: "border-amber-500/20"
    },
    {
      id: "humidity",
      label: "Humidity",
      value: `${weather.humidity}%`,
      subText: "Relative Air Humidity",
      icon: Droplets,
      color: "text-blue-400",
      bgColor: "bg-blue-500/10",
      borderColor: "border-blue-500/20"
    },
    {
      id: "rain",
      label: "Precipitation",
      value: `${weather.rain.toFixed(1)} mm`,
      subText: "Today's Rainfall Sum",
      icon: CloudRain,
      color: "text-cyan-400",
      bgColor: "bg-cyan-500/10",
      borderColor: "border-cyan-500/20"
    },
    {
      id: "wind",
      label: "Wind Speed",
      value: `${weather.wind_max.toFixed(1)} km/h`,
      subText: "Max 10m Wind Speed",
      icon: Wind,
      color: "text-teal-400",
      bgColor: "bg-teal-500/10",
      borderColor: "border-teal-500/20"
    },
    {
      id: "pressure",
      label: "Pressure",
      value: `${weather.pressure.toFixed(0)} hPa`,
      subText: "Surface Pressure",
      icon: Gauge,
      color: "text-purple-400",
      bgColor: "bg-purple-500/10",
      borderColor: "border-purple-500/20"
    },
    {
      id: "cloud",
      label: "Cloud Cover",
      value: `${weather.cloud_cover}%`,
      subText: "Mean Sky Coverage",
      icon: Cloud,
      color: "text-slate-300",
      bgColor: "bg-slate-500/10",
      borderColor: "border-slate-500/20"
    }
  ];

  return (
    <div className="bg-slate-900/60 backdrop-blur-xl border border-slate-800 rounded-2xl p-6 shadow-xl">
      <div className="flex items-center justify-between mb-6 pb-4 border-b border-slate-800">
        <div>
          <h2 className="text-xl font-semibold text-white tracking-wide">Today's Weather Parameters</h2>
          <p className="text-xs text-slate-400 mt-0.5">Live Open-Meteo Observations for {weather.city}</p>
        </div>
        <div className="text-right">
          <span className="text-xs font-mono text-cyan-400 bg-cyan-950/60 px-3 py-1 rounded-full border border-cyan-800/40">
            {weather.date}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {metrics.map((m) => {
          const Icon = m.icon;
          return (
            <div
              key={m.id}
              className="bg-slate-800/40 hover:bg-slate-800/70 border border-slate-700/50 hover:border-slate-600 rounded-xl p-4 transition-all duration-200 group"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">{m.label}</span>
                <div className={`p-2 rounded-lg ${m.bgColor} border ${m.borderColor} group-hover:scale-105 transition-transform`}>
                  <Icon className={`w-4 h-4 ${m.color}`} />
                </div>
              </div>
              <div className="mt-3">
                <p className="text-2xl font-bold text-white tracking-tight">{m.value}</p>
                <p className="text-xs text-slate-400 mt-1">{m.subText}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

"use client";

import React from "react";
import { WeatherTrendPoint } from "@/types/weather";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend
} from "recharts";
import { TrendingUp } from "lucide-react";

interface WeatherChartProps {
  data: WeatherTrendPoint[];
}

export const WeatherChart: React.FC<WeatherChartProps> = ({ data }) => {
  return (
    <div className="bg-slate-900/60 backdrop-blur-xl border border-slate-800 rounded-2xl p-6 shadow-xl">
      <div className="flex items-center justify-between mb-6 pb-4 border-b border-slate-800">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 bg-indigo-500/10 border border-indigo-500/20 rounded-lg text-indigo-400">
            <TrendingUp className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white tracking-wide">Weekly Weather Trends</h2>
            <p className="text-xs text-slate-400">Temperature & Rain Probability Visualization</p>
          </div>
        </div>
      </div>

      <div className="h-72 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorTemp" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#f59e0b" stopOpacity={0.0} />
              </linearGradient>
              <linearGradient id="colorRain" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.0} />
              </linearGradient>
            </defs>

            <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.5} />
            <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} tickLine={false} />
            <YAxis yAxisId="left" stroke="#f59e0b" fontSize={12} unit="°C" domain={['auto', 'auto']} tickLine={false} />
            <YAxis yAxisId="right" orientation="right" stroke="#3b82f6" fontSize={12} unit="%" domain={[0, 100]} tickLine={false} />

            <Tooltip
              contentStyle={{
                backgroundColor: "#0f172a",
                borderColor: "#334155",
                borderRadius: "0.75rem",
                color: "#f8fafc",
                boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.5)"
              }}
              formatter={(value: any, name: string) => [
                name === "temp" ? `${value}°C` : `${value}%`,
                name === "temp" ? "Max Temp" : "Rain Probability"
              ]}
            />
            <Legend wrapperStyle={{ paddingTop: "10px", fontSize: "12px" }} />

            <Area
              yAxisId="left"
              type="monotone"
              dataKey="temp"
              name="Max Temp (°C)"
              stroke="#f59e0b"
              strokeWidth={3}
              fillOpacity={1}
              fill="url(#colorTemp)"
            />
            <Area
              yAxisId="right"
              type="monotone"
              dataKey="rainProb"
              name="Rain Probability (%)"
              stroke="#3b82f6"
              strokeWidth={3}
              fillOpacity={1}
              fill="url(#colorRain)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

import React from "react";
import { Flight } from "../types/trip";
import { useTheme } from "../context/ThemeContext";
import { Plane, Clock, Luggage, MapPin } from "lucide-react";

interface FlightSelectProps {
  flights: Flight[];
  onSelect: (flight: Flight) => void;
  currentStep: number;
}

export function FlightSelect({
  flights,
  onSelect,
  currentStep,
}: FlightSelectProps) {
  const { theme } = useTheme();
  if (currentStep !== 2) return null; // only show on flight step
  return (
    <div className="space-y-6">
      <h2
        className={`text-xl font-bold ${
          theme === "light" ? "text-gray-800" : "text-white"
        }`}
      >
        Alege un zbor
      </h2>
      <div className="space-y-4">
        {flights.slice(0, 3).map((f, idx) => {
          const stopsClass = f.stops?.toLowerCase().includes("direct")
            ? "bg-green-500/10 text-green-600 border-green-400/40"
            : "bg-amber-500/10 text-amber-600 border-amber-400/40";
          return (
            <button
              key={idx}
              onClick={() => onSelect(f)}
              className={`group w-full text-left rounded-2xl border overflow-hidden transition ${
                theme === "light"
                  ? "bg-white border-blue-200 hover:shadow-lg"
                  : "bg-[#13273F] border-cyan-700/40 hover:shadow-cyan-500/20"
              }`}
            >
              <div className="p-5 flex flex-col gap-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-12 h-12 rounded-xl flex items-center justify-center ${
                        theme === "light" ? "bg-blue-100" : "bg-cyan-900/40"
                      }`}
                    >
                      <Plane
                        className={`w-6 h-6 ${
                          theme === "light" ? "text-blue-500" : "text-cyan-400"
                        }`}
                      />
                    </div>
                    <div>
                      <p
                        className={`font-semibold ${
                          theme === "light" ? "text-gray-800" : "text-white"
                        }`}
                      >
                        {f.airline}
                      </p>
                      <p
                        className={`text-xs ${
                          theme === "light" ? "text-gray-600" : "text-gray-300"
                        }`}
                      >
                        {f.cabinClass || "Economy"} • {f.baggage}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p
                      className={`text-lg font-semibold ${
                        theme === "light" ? "text-blue-600" : "text-cyan-300"
                      }`}
                    >
                      {f.price}€
                    </p>
                    {f.isTopChoice && (
                      <span className="inline-block mt-1 text-[10px] px-2 py-1 rounded-full bg-gradient-to-r from-blue-500 to-cyan-500 text-white">
                        Top Choice
                      </span>
                    )}
                  </div>
                </div>
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div className="flex flex-col">
                    <span className="font-medium">Plecare</span>
                    <span
                      className={`text-xs ${
                        theme === "light" ? "text-gray-600" : "text-gray-300"
                      }`}
                    >
                      {f.originCode} • {f.departureTime}
                    </span>
                  </div>
                  <div className="flex flex-col">
                    <span className="font-medium">Sosire</span>
                    <span
                      className={`text-xs ${
                        theme === "light" ? "text-gray-600" : "text-gray-300"
                      }`}
                    >
                      {f.destinationCode} • {f.arrivalTime}
                    </span>
                  </div>
                  <div className="flex flex-col">
                    <span className="font-medium flex items-center gap-1">
                      <Clock className="w-3 h-3" /> Durată
                    </span>
                    <span
                      className={`text-xs ${
                        theme === "light" ? "text-gray-600" : "text-gray-300"
                      }`}
                    >
                      {f.duration}
                    </span>
                  </div>
                </div>
                <div className="flex items-center flex-wrap gap-3 text-xs">
                  <span
                    className={`px-2 py-1 rounded-full border ${stopsClass}`}
                  >
                    {f.stops}
                  </span>
                  <span
                    className={`px-2 py-1 rounded-full border ${
                      theme === "light"
                        ? "bg-blue-50 text-blue-700 border-blue-200"
                        : "bg-cyan-950/40 text-cyan-300 border-cyan-700/40"
                    }`}
                  >
                    {f.baggage}
                  </span>
                </div>
                <div className="flex justify-end">
                  <span
                    className={`text-sm font-medium ${
                      theme === "light" ? "text-blue-600" : "text-cyan-300"
                    }`}
                  >
                    Selectează →
                  </span>
                </div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}

export default FlightSelect;

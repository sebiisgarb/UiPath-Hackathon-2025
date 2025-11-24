import React from "react";
import { Accommodation } from "../types/trip";
import { useTheme } from "../context/ThemeContext";
import { Building2, Star, MapPin, Wifi, Coffee, Dumbbell } from "lucide-react";

interface HotelSelectProps {
  hotels: Accommodation[];
  onSelect: (hotel: Accommodation) => void;
  currentStep: number;
}

export function HotelSelect({
  hotels,
  onSelect,
  currentStep,
}: HotelSelectProps) {
  const { theme } = useTheme();
  if (currentStep !== 3) return null; // only show on hotel step
  return (
    <div className="space-y-6">
      <h2
        className={`text-xl font-bold ${
          theme === "light" ? "text-gray-800" : "text-white"
        }`}
      >
        Alege cazarea
      </h2>
      <div className="space-y-4">
        {hotels.slice(0, 3).map((h, idx) => (
          <button
            key={idx}
            onClick={() => onSelect(h)}
            className={`group w-full text-left rounded-2xl border overflow-hidden transition ${
              theme === "light"
                ? "bg-white border-blue-200 hover:shadow-lg"
                : "bg-[#13273F] border-cyan-700/40 hover:shadow-cyan-500/20"
            }`}
          >
            <div className="grid md:grid-cols-[160px_1fr] gap-5 p-5">
              {/* Image */}
              <div className="relative h-40 md:h-full rounded-xl overflow-hidden">
                <img
                  src={h.image}
                  alt={h.name}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                />
                {h.isTopChoice && (
                  <span className="absolute top-2 left-2 text-[10px] px-2 py-1 rounded-full bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow">
                    Top Choice
                  </span>
                )}
              </div>
              {/* Details */}
              <div className="flex flex-col gap-3">
                <div className="flex justify-between items-start gap-4">
                  <div>
                    <p
                      className={`font-semibold text-sm md:text-base ${
                        theme === "light" ? "text-gray-800" : "text-white"
                      }`}
                    >
                      {h.name}
                    </p>
                    <p
                      className={`text-xs ${
                        theme === "light" ? "text-gray-600" : "text-gray-300"
                      }`}
                    >
                      {h.type}
                    </p>
                  </div>
                  <div className="text-right">
                    <p
                      className={`text-lg font-semibold ${
                        theme === "light" ? "text-blue-600" : "text-cyan-300"
                      }`}
                    >
                      {h.pricePerNight}€
                      <span className="text-xs font-normal opacity-70">
                        /noapte
                      </span>
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-4 text-xs">
                  <span
                    className={`flex items-center gap-1 ${
                      theme === "light" ? "text-gray-600" : "text-gray-300"
                    }`}
                  >
                    <MapPin className="w-3 h-3" />
                    {h.distanceFromCenter}
                  </span>
                  <span
                    className={`flex items-center gap-1 ${
                      theme === "light" ? "text-gray-600" : "text-gray-300"
                    }`}
                  >
                    <Star className="w-3 h-3 fill-yellow-400 text-yellow-400" />
                    {h.rating}
                  </span>
                </div>
                {h.amenities && (
                  <div className="flex flex-wrap gap-2">
                    {h.amenities.slice(0, 5).map((a, i) => (
                      <span
                        key={i}
                        className={`px-2 py-1 rounded-full text-[11px] border ${
                          theme === "light"
                            ? "bg-blue-50 border-blue-200 text-blue-700"
                            : "bg-cyan-950/40 border-cyan-800 text-cyan-300"
                        }`}
                      >
                        {a}
                      </span>
                    ))}
                  </div>
                )}
                <div className="flex justify-end mt-auto">
                  <span
                    className={`text-sm font-medium ${
                      theme === "light" ? "text-blue-600" : "text-cyan-300"
                    }`}
                  >
                    Selectează →
                  </span>
                </div>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

export default HotelSelect;

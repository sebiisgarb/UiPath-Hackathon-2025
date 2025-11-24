import { Calendar } from "lucide-react";
import { useTheme } from "../context/ThemeContext";
import { ItineraryDay } from "../types/trip";

interface ItineraryTimelineProps {
  itinerary: ItineraryDay[];
}

export function ItineraryTimeline({ itinerary }: ItineraryTimelineProps) {
  const { theme } = useTheme();

  return (
    <div className="space-y-6">
      <h2
        className={`text-2xl font-bold flex items-center gap-3 ${
          theme === "light" ? "text-gray-800" : "text-white"
        }`}
      >
        <Calendar
          className={theme === "light" ? "text-blue-600" : "text-cyan-400"}
        />
        Itinerary
      </h2>

      <div
        className={`rounded-2xl p-8 ${
          theme === "light"
            ? "bg-white shadow-lg"
            : "bg-[#13273F] shadow-lg shadow-blue-900/20 border border-yellow-300/70"
        }`}
      >
        <div className="space-y-6">
          {itinerary.map((day, index) => (
            <div key={index} className="flex gap-6">
              <div className="flex flex-col items-center">
                <div
                  className={`w-12 h-12 rounded-full flex items-center justify-center font-bold ${
                    theme === "light"
                      ? "bg-gradient-to-br from-purple-500 to-blue-500 text-white"
                      : "bg-gradient-to-br from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/30"
                  }`}
                >
                  {day.day}
                </div>
                {index < itinerary.length - 1 && (
                  <div
                    className={`w-0.5 flex-1 mt-2 ${
                      theme === "light" ? "bg-blue-200" : "bg-cyan-500/20"
                    }`}
                    style={{ minHeight: "40px" }}
                  />
                )}
              </div>
              <div className="flex-1 pb-6">
                <h3
                  className={`text-lg font-semibold mb-2 ${
                    theme === "light" ? "text-gray-800" : "text-white"
                  }`}
                >
                  {day.title}
                </h3>
                <p
                  className={`${
                    theme === "light" ? "text-gray-600" : "text-gray-300"
                  }`}
                >
                  {day.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

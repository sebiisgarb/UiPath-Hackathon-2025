import { MapPin, Calendar, DollarSign, Award } from "lucide-react";
import { useTheme } from "../context/ThemeContext";
import { TripPlan } from "../types/trip";

interface BestOptionProps {
  plan: TripPlan;
  onBuyNow: () => void;
}

export function BestOption({ plan, onBuyNow }: BestOptionProps) {
  const { theme } = useTheme();

  return (
    <div
      className={`rounded-3xl p-8 transition-all duration-300 ${
        theme === "light"
          ? "bg-white shadow-xl border-2 border-blue-300/70"
          : "bg-[#13273F] shadow-2xl shadow-blue-900/30 border border-yellow-500/70"
      }`}
    >
      <div className="flex items-center justify-between mb-6">
        <h2
          className={`text-2xl font-bold ${
            theme === "light" ? "text-gray-800" : "text-white"
          }`}
        >
          Best Option
        </h2>
        <div
          className={`px-4 py-2 rounded-full flex items-center gap-2 ${
            theme === "light"
              ? "bg-blue-500 text-white"
              : "bg-blue-500 text-white shadow-lg shadow-cyan-500/30"
          }`}
        >
          <Award className="w-4 h-4" />
          <span className="text-sm font-semibold">Top Choice</span>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6 mb-6">
        <div
          className={`rounded-2xl overflow-hidden ${
            theme === "light" ? "bg-gray-100" : "bg-[#0A1A2F]"
          }`}
        >
          <img
            src="https://images.pexels.com/photos/2412609/pexels-photo-2412609.jpeg?auto=compress&cs=tinysrgb&w=600"
            alt={plan.destination}
            className="w-full h-64 object-cover"
          />
        </div>

        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <MapPin
              className={`w-5 h-5 ${
                theme === "light" ? "text-blue-600" : "text-cyan-400"
              }`}
            />
            <div>
              <p
                className={`text-sm ${
                  theme === "light" ? "text-gray-500" : "text-gray-400"
                }`}
              >
                Destination
              </p>
              <p
                className={`text-xl font-semibold ${
                  theme === "light" ? "text-gray-800" : "text-white"
                }`}
              >
                {plan.destination}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Calendar
              className={`w-5 h-5 ${
                theme === "light" ? "text-blue-600" : "text-cyan-400"
              }`}
            />
            <div>
              <p
                className={`text-sm ${
                  theme === "light" ? "text-gray-500" : "text-gray-400"
                }`}
              >
                Optimal Period
              </p>
              <p
                className={`text-lg font-semibold ${
                  theme === "light" ? "text-gray-800" : "text-white"
                }`}
              >
                {plan.period}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <DollarSign
              className={`w-5 h-5 ${
                theme === "light" ? "text-blue-600" : "text-cyan-400"
              }`}
            />
            <div>
              <p
                className={`text-sm ${
                  theme === "light" ? "text-gray-500" : "text-gray-400"
                }`}
              >
                Total Estimated Price
              </p>
              <p
                className={`text-2xl font-bold ${
                  theme === "light"
                    ? "bg-yellow-400 bg-clip-text text-transparent"
                    : "bg-yellow-300 bg-clip-text text-transparent"
                }`}
              >
                €{plan.totalPrice}
              </p>
            </div>
          </div>
        </div>
      </div>

      <p
        className={`mb-6 leading-relaxed ${
          theme === "light" ? "text-gray-600" : "text-gray-300"
        }`}
      >
        {plan.summary}
      </p>

      <button
        onClick={onBuyNow}
        className={`w-full py-4 rounded-2xl font-bold text-white text-lg transition-all duration-300 ${
          theme === "light"
            ? "bg-blue-400 hover:shadow-xl hover:shadow-blue-500/30 hover:scale-[1.02]"
            : "bg-blue-600 hover:shadow-xl hover:shadow-blue-500/50 hover:scale-[1.02]"
        }`}
      >
        BUY NOW
      </button>
    </div>
  );
}

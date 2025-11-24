import { Plane, Award } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { Flight } from '../types/trip';

interface FlightRecommendationsProps {
  flights: Flight[];
}

export function FlightRecommendations({ flights }: FlightRecommendationsProps) {
  const { theme } = useTheme();

  return (
    <div className="space-y-6">
      <h2
        className={`text-2xl font-bold flex items-center gap-3 ${
          theme === 'light' ? 'text-gray-800' : 'text-white'
        }`}
      >
        <Plane
          className={theme === 'light' ? 'text-blue-600' : 'text-cyan-400'}
        />
        Flight Recommendations
      </h2>

      <div className="grid md:grid-cols-3 gap-6">
        {flights.map((flight, index) => (
          <div
            key={index}
            className={`rounded-2xl p-6 transition-all duration-300 hover:scale-105 ${
              theme === 'light'
                ? 'bg-white shadow-lg hover:shadow-xl'
                : 'bg-[#13273F] shadow-lg shadow-blue-900/20 border border-cyan-500/10 hover:border-cyan-500/30'
            }`}
          >
            {flight.isTopChoice && (
              <div
                className={`mb-4 px-3 py-1.5 rounded-full inline-flex items-center gap-2 text-sm font-semibold ${
                  theme === 'light'
                    ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white'
                    : 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/30'
                }`}
              >
                <Award className="w-4 h-4" />
                Best Flight
              </div>
            )}
            <h3
              className={`text-lg font-semibold mb-2 ${
                theme === 'light' ? 'text-gray-800' : 'text-white'
              }`}
            >
              {flight.airline}
            </h3>
            <p
              className={`text-3xl font-bold ${
                theme === 'light'
                  ? 'bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent'
                  : 'bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent'
              }`}
            >
              €{flight.price}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

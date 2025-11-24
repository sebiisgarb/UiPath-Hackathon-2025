import { Hotel, MapPin, Star, Award } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { Accommodation } from '../types/trip';

interface AccommodationRecommendationsProps {
  accommodations: Accommodation[];
}

export function AccommodationRecommendations({
  accommodations,
}: AccommodationRecommendationsProps) {
  const { theme } = useTheme();

  const hotelImages = [
    'https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg?auto=compress&cs=tinysrgb&w=600',
    'https://images.pexels.com/photos/164595/pexels-photo-164595.jpeg?auto=compress&cs=tinysrgb&w=600',
    'https://images.pexels.com/photos/1457842/pexels-photo-1457842.jpeg?auto=compress&cs=tinysrgb&w=600',
  ];

  return (
    <div className="space-y-6">
      <h2
        className={`text-2xl font-bold flex items-center gap-3 ${
          theme === 'light' ? 'text-gray-800' : 'text-white'
        }`}
      >
        <Hotel
          className={theme === 'light' ? 'text-blue-600' : 'text-cyan-400'}
        />
        Accommodation Recommendations
      </h2>

      <div className="grid md:grid-cols-3 gap-6">
        {accommodations.map((accommodation, index) => (
          <div
            key={index}
            className={`rounded-2xl overflow-hidden transition-all duration-300 hover:scale-105 ${
              theme === 'light'
                ? 'bg-white shadow-lg hover:shadow-xl'
                : 'bg-[#13273F] shadow-lg shadow-blue-900/20 border border-cyan-500/10 hover:border-cyan-500/30'
            }`}
          >
            <img
              src={hotelImages[index]}
              alt={accommodation.name}
              className="w-full h-48 object-cover"
            />
            <div className="p-5">
              {accommodation.isTopChoice && (
                <div
                  className={`mb-3 px-3 py-1.5 rounded-full inline-flex items-center gap-2 text-sm font-semibold ${
                    theme === 'light'
                      ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white'
                      : 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/30'
                  }`}
                >
                  <Award className="w-4 h-4" />
                  Best Option
                </div>
              )}
              <h3
                className={`text-lg font-semibold mb-2 ${
                  theme === 'light' ? 'text-gray-800' : 'text-white'
                }`}
              >
                {accommodation.name}
              </h3>
              <p
                className={`text-2xl font-bold mb-3 ${
                  theme === 'light'
                    ? 'bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent'
                    : 'bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent'
                }`}
              >
                €{accommodation.pricePerNight}
                <span
                  className={`text-sm font-normal ${
                    theme === 'light' ? 'text-gray-500' : 'text-gray-400'
                  }`}
                >
                  /night
                </span>
              </p>
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <MapPin
                    className={`w-4 h-4 ${
                      theme === 'light' ? 'text-blue-600' : 'text-cyan-400'
                    }`}
                  />
                  <span
                    className={`text-sm ${
                      theme === 'light' ? 'text-gray-600' : 'text-gray-300'
                    }`}
                  >
                    {accommodation.distanceFromCenter}
                  </span>
                </div>
                <p
                  className={`text-sm ${
                    theme === 'light' ? 'text-gray-600' : 'text-gray-300'
                  }`}
                >
                  {accommodation.type}
                </p>
                <div className="flex items-center gap-1">
                  <Star
                    className={`w-4 h-4 fill-current ${
                      theme === 'light' ? 'text-yellow-500' : 'text-yellow-400'
                    }`}
                  />
                  <span
                    className={`text-sm font-semibold ${
                      theme === 'light' ? 'text-gray-700' : 'text-white'
                    }`}
                  >
                    {accommodation.rating.toFixed(1)}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

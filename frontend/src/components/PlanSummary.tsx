// PlanSummary component (no React import needed with TS + JSX transform)
import { Flight, Accommodation } from "../types/trip";
import { useTheme } from "../context/ThemeContext";
import { Calendar, Plane, Building2, CreditCard, MapPin } from "lucide-react";

interface PlanSummaryProps {
  destination: string;
  travelDates: string;
  flight: Flight | null;
  hotel: Accommodation | null;
  nights: number;
  onBookNow: () => void;
}

export function PlanSummary({
  destination,
  travelDates,
  flight,
  hotel,
  nights,
  onBookNow,
}: PlanSummaryProps) {
  const { theme } = useTheme();

  const flightCost = flight?.price || 0;
  const hotelCost = (hotel?.pricePerNight || 0) * nights;
  const totalCost = flightCost + hotelCost; // only flight + hotel as requested

  // (Weather chart removed per latest request)

  // Rich mocked activity pool (Barcelona)
  const activityPool = [
    {
      name: "Sagrada Familia",
      img: "https://images.pexels.com/photos/427009/pexels-photo-427009.jpeg?auto=compress&cs=tinysrgb&w=600",
      desc: "Capodopera lui Gaudí cu detalii organice și vitralii uimitoare.",
      tag: "Cultural",
      cost: 26,
    },
    {
      name: "La Rambla Walk",
      img: "https://images.pexels.com/photos/1005644/pexels-photo-1005644.jpeg?auto=compress&cs=tinysrgb&w=600",
      desc: "Artiști stradali, florării colorate și energie urbană vibrantă.",
      tag: "Explorare",
      cost: 0,
    },
    {
      name: "Parc Güell",
      img: "https://images.pexels.com/photos/208745/pexels-photo-208745.jpeg?auto=compress&cs=tinysrgb&w=600",
      desc: "Mozaicuri ondulate și panoramă superbă asupra orașului.",
      tag: "Arhitectură",
      cost: 10,
    },
    {
      name: "Barceloneta Sunset",
      img: "https://images.pexels.com/photos/994605/pexels-photo-994605.jpeg?auto=compress&cs=tinysrgb&w=600",
      desc: "Apus auriu pe plajă și briză mediteraneană relaxantă.",
      tag: "Relaxare",
      cost: 0,
    },
    {
      name: "El Born District",
      img: "https://images.pexels.com/photos/1796715/pexels-photo-1796715.jpeg?auto=compress&cs=tinysrgb&w=600",
      desc: "Străduțe boeme cu ateliere artizanale și boutique-uri locale.",
      tag: "Explorare",
      cost: 0,
    },
    {
      name: "Museu Picasso",
      img: "https://images.pexels.com/photos/3734020/pexels-photo-3734020.jpeg?auto=compress&cs=tinysrgb&w=600",
      desc: "Colecție majoră din perioadele formative ale artistului.",
      tag: "Cultural",
      cost: 12,
    },
    {
      name: "Tapas Experience",
      img: "https://images.pexels.com/photos/1484516/pexels-photo-1484516.jpeg?auto=compress&cs=tinysrgb&w=600",
      desc: "Degustare de jamón, patatas bravas și pan con tomate.",
      tag: "Gastronomie",
      cost: 25,
    },
    {
      name: "Mercat Boqueria",
      img: "https://images.pexels.com/photos/615103/pexels-photo-615103.jpeg?auto=compress&cs=tinysrgb&w=600",
      desc: "Fructe exotice, sucuri proaspete și culori vibrante locale.",
      tag: "Gastronomie",
      cost: 8,
    },
    {
      name: "Gothic Quarter",
      img: "https://images.pexels.com/photos/357964/pexels-photo-357964.jpeg?auto=compress&cs=tinysrgb&w=600",
      desc: "Arcuri medievale, curți ascunse și istorie la fiecare colț.",
      tag: "Istorie",
      cost: 0,
    },
  ];

  // Build itinerary: 3 activities / day rotating through pool
  const itinerary = Array.from({ length: nights }, (_, i) => {
    const startIndex = (i * 3) % activityPool.length;
    const slice = activityPool
      .slice(startIndex, startIndex + 3)
      .concat(
        startIndex + 3 > activityPool.length
          ? activityPool.slice(0, (startIndex + 3) % activityPool.length)
          : []
      )
      .slice(0, 3);
    return { day: i + 1, activities: slice };
  });

  return (
    <div className="space-y-10">
      {/* Summary Section */}
      <div
        className={`relative rounded-3xl p-8 overflow-hidden border backdrop-blur-xl transition ${
          theme === "light"
            ? "bg-white/90 border-blue-300 shadow-lg"
            : "bg-[#3f6794]/10 shadow-xl shadow-black/40 border-yellow-300"
        }`}
      >
        <h2
          className={`text-3xl font-bold mb-8 tracking-tight ${
            theme === "light" ? "text-[#3f6794]" : "text-white"
          }`}
        >
          Planul Tău de Călătorie
        </h2>
        <div className="grid lg:grid-cols-2 gap-12">
          <div className="space-y-6">
            <div className="flex items-start gap-3">
              <Calendar
                className={`w-5 h-5 mt-0.5 ${
                  theme === "light" ? "text-blue-300" : "text-cyan-400"
                }`}
              />
              <div
                className={` ${
                  theme === "light" ? "text-black" : "text-white"
                }`}
              >
                <p className="text-xs uppercase tracking-wide opacity-60">
                  Perioadă
                </p>
                <p className="font-semibold text-sm">
                  {travelDates} • {nights} nopți
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <MapPin
                className={`w-5 h-5 mt-0.5 ${
                  theme === "light" ? "text-blue-300" : "text-cyan-400"
                }`}
              />
              <div
                className={` ${
                  theme === "light" ? "text-black" : "text-white"
                }`}
              >
                <p className="text-xs uppercase tracking-wide opacity-60">
                  Destinație
                </p>
                <p className="font-semibold text-sm">{destination}</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <Plane
                className={`w-5 h-5 mt-0.5 ${
                  theme === "light" ? "text-blue-300" : "text-cyan-400"
                }`}
              />
              <div
                className={` ${
                  theme === "light" ? "text-black" : "text-white"
                }`}
              >
                <p className="text-xs uppercase tracking-wide opacity-60">
                  Zbor
                </p>
                <p className="font-semibold text-sm">
                  {flight
                    ? `${flight.airline} • ${flight.price}€`
                    : "Neselectat"}
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <Building2
                className={`w-5 h-5 mt-0.5 ${
                  theme === "light" ? "text-blue-300" : "text-cyan-400"
                }`}
              />
              <div
                className={` ${
                  theme === "light" ? "text-black" : "text-white"
                }`}
              >
                <p className="text-xs uppercase tracking-wide opacity-60">
                  Cazare
                </p>
                <p className="font-semibold text-sm">
                  {hotel
                    ? `${hotel.name} • ${hotel.pricePerNight}€/noapte`
                    : "Neselectată"}
                </p>
              </div>
            </div>
          </div>
          <div className="flex flex-col gap-6">
            <div
              className={`rounded-2xl p-5 border relative ${
                theme === "light"
                  ? "bg-gradient-to-br from-blue-50 to-white border-blue-300"
                  : "bg-gradient-to-br from-[#1E293B] to-[#0F172A] border-slate-700"
              }`}
            >
              <p
                className={`text-md  ${
                  theme === "light" ? "text-black" : "text-white"
                } uppercase tracking-wide mb-3`}
              >
                Costuri
              </p>
              <div
                className={`flex justify-between text-sm mb-1 ${
                  theme === "light" ? "text-black" : "text-white"
                }`}
              >
                <span>Zbor</span>
                <span>{flightCost}€</span>
              </div>
              <div
                className={`flex justify-between text-sm mb-1 ${
                  theme === "light" ? "text-black" : "text-white"
                }`}
              >
                <span>Cazare ({nights} nopți)</span>
                <span>{hotelCost}€</span>
              </div>
              <div className="h-px bg-gradient-to-r from-transparent via-blue-400/40 to-transparent my-4" />
              <div
                className={`flex justify-between text-sm font-semibold ${
                  theme === "light" ? "text-black" : "text-white"
                }`}
              >
                <span>Total estimat</span>
                <span className="text-yellow-400">{totalCost}€</span>
              </div>
            </div>
            <button
              onClick={onBookNow}
              className={`w-full flex items-center justify-center gap-2 rounded-xl py-4 text-sm font-semibold transition ${
                theme === "light"
                  ? "bg-[#3f6794]/70 hover:bg-[#3f6794]/90 text-white shadow-lg shadow-blue-300/40"
                  : "bg-blue-300/70 hover:bg-blue-300 text-white shadow-lg shadow-cyan-900/40"
              }`}
            >
              <CreditCard className="w-4 h-4" /> Rezervă
            </button>
          </div>
        </div>
      </div>

      {/* Itinerary Section */}
      <div
        className={`rounded-3xl p-8 backdrop-blur-xl border transition ${
          theme === "light"
            ? "bg-white/90 border-blue-300"
            : "bg-[#3f6794]/10 shadow-xl shadow-black/40 border-yellow-300"
        }`}
      >
        <h3
          className={`text-2xl font-semibold mb-8 ${
            theme === "light" ? "text-[#3f6794]" : "text-white"
          }`}
        >
          Itinerariu Detaliat
        </h3>
        <div className="space-y-12">
          {itinerary.map((day) => (
            <div key={day.day}>
              <div className="flex items-center gap-3 mb-5">
                <div
                  className={`px-3 py-1 rounded-full text-xs font-semibold ${
                    theme === "light"
                      ? "bg-blue-100 text-blue-700"
                      : "bg-slate-800/60 text-cyan-200"
                  }`}
                >
                  Ziua {day.day}
                </div>
                <div className="h-px flex-1 bg-gradient-to-r from-blue-400/40 to-transparent" />
              </div>
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {day.activities.map((act, i) => (
                  <div
                    key={i}
                    className={`group rounded-2xl overflow-hidden border relative flex flex-col ${
                      theme === "light"
                        ? "bg-white border-blue-300 hover:shadow-md hover:shadow-blue-300/40"
                        : "bg-[#1E293B] border-slate-700/70 hover:shadow-lg hover:shadow-cyan-900/30"
                    } transition`}
                  >
                    <div className="h-40 w-full overflow-hidden">
                      <img
                        src={act.img}
                        alt={act.name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      />
                    </div>
                    <div className="p-4 flex flex-col gap-2 flex-1">
                      <p
                        className={`text-sm font-semibold leading-tight ${
                          theme === "light" ? "text-gray-800" : "text-white"
                        }`}
                      >
                        {act.name}
                      </p>
                      <p
                        className={`text-xs opacity-80 leading-relaxed ${
                          theme === "light" ? "text-gray-600" : "text-white/80"
                        }`}
                      >
                        {act.desc}
                      </p>
                      <div className="mt-auto pt-2 flex justify-between items-center">
                        <span
                          className={`inline-block text-[10px] tracking-wide px-2 py-1 rounded-full ${
                            theme === "light"
                              ? "bg-blue-100 text-blue-700 border border-blue-200"
                              : "bg-cyan-950/40 text-cyan-300 border border-slate-700"
                          }`}
                        >
                          {act.tag}
                        </span>
                        <span
                          className={`text-[11px] font-semibold ${
                            theme === "light" ? "text-gray-700" : "text-white"
                          }`}
                        >
                          {act.cost === 0 ? "Gratuit" : `${act.cost}€`}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default PlanSummary;

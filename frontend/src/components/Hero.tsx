import React from "react";
import { Sparkles, Plane, Map, Clock } from "lucide-react";
import { useTheme } from "../context/ThemeContext";

interface HeroProps {
  onStart: () => void;
}

export function Hero({ onStart }: HeroProps) {
  const { theme } = useTheme();
  return (
    <section className="relative overflow-hidden pt-32 pb-28">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute -top-32 -left-32 w-[520px] h-[520px] rounded-full bg-gradient-to-br from-blue-400/40 to-cyan-400/10 blur-3xl opacity-60" />
        <div className="absolute -bottom-40 -right-40 w-[600px] h-[600px] rounded-full bg-gradient-to-tr from-indigo-500/30 to-purple-500/20 blur-3xl opacity-50" />
      </div>
      <div className="relative max-w-7xl mx-auto px-6">
        <div className="max-w-3xl">
          <div className="flex items-center gap-3 mb-6">
            <div
              className={`p-3 rounded-2xl shadow-lg ${
                theme === "light" ? "bg-blue-500" : "bg-cyan-600"
              }`}
            >
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <span
              className={`text-sm tracking-wide font-medium uppercase ${
                theme === "light" ? "text-blue-700" : "text-cyan-300"
              }`}
            >
              AI Travel Assistant
            </span>
          </div>
          <h1
            className={`text-5xl md:text-6xl font-extrabold leading-tight mb-6 ${
              theme === "light" ? "text-gray-800" : "text-white"
            }`}
          >
            Planifică vacanțe memorabile în câteva secunde cu AI
          </h1>
          <p
            className={`text-lg md:text-xl mb-10 ${
              theme === "light" ? "text-gray-600" : "text-gray-300"
            }`}
          >
            Generează instant itinerarii personalizate, recomandări de zboruri
            și cazări potrivite stilului tău. Economisește timp și buget
            explorând opțiuni curate, gata de rezervat.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-12">
            <Feature
              icon={<Plane className="w-5 h-5" />}
              label="Zboruri optime"
              theme={theme}
            />
            <Feature
              icon={<Map className="w-5 h-5" />}
              label="Itinerariu smart"
              theme={theme}
            />
            <Feature
              icon={<Clock className="w-5 h-5" />}
              label="Rapid & flexibil"
              theme={theme}
            />
          </div>
          <div className="flex flex-col sm:flex-row gap-4">
            <button
              onClick={onStart}
              className={`group relative overflow-hidden rounded-2xl px-8 py-5 font-semibold text-lg flex items-center justify-center gap-2 transition-all ${
                theme === "light"
                  ? "bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-lg hover:shadow-xl hover:scale-[1.02]"
                  : "bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/30 hover:shadow-cyan-500/50 hover:scale-[1.02]"
              }`}
            >
              <span>Începe planificarea</span>
            </button>
            <button
              className={`rounded-2xl px-8 py-5 font-medium backdrop-blur-sm border text-lg transition-all ${
                theme === "light"
                  ? "border-blue-300/60 bg-white/70 text-blue-700 hover:bg-blue-50"
                  : "border-cyan-600/40 bg-white/5 text-cyan-300 hover:bg-cyan-600/10"
              }`}
            >
              Află mai multe
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}

function Feature({
  icon,
  label,
  theme,
}: {
  icon: React.ReactNode;
  label: string;
  theme: string;
}) {
  return (
    <div
      className={`flex items-center gap-3 rounded-xl px-5 py-4 border text-sm font-medium ${
        theme === "light"
          ? "bg-white/70 border-blue-200 text-gray-700"
          : "bg-white/5 border-cyan-600/30 text-cyan-200"
      }`}
    >
      <div
        className={`w-8 h-8 flex items-center justify-center rounded-lg ${
          theme === "light"
            ? "bg-blue-500 text-white"
            : "bg-cyan-600 text-white"
        }`}
      >
        {icon}
      </div>
      {label}
    </div>
  );
}

export default Hero;

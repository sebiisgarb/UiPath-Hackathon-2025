import { useTheme } from "../context/ThemeContext";

export const HomeHero = ({ onStart }: { onStart: () => void }) => {
  const { theme } = useTheme();
  return (
    <section className="text-center pt-40 px-6 max-w-5xl mx-auto">
      <p
        className={`text-4xl md:text-6xl font-bold drop-shadow-lg transition-colors ${
          theme === "light" ? "text-[#3f6794]" : "text-white"
        }`}
      >
        Planifici
        <span
          className={`${
            theme === "light" ? "text-blue-400" : "text-yellow-300"
          }`}
        >
          .
        </span>{" "}
        Explorezi
        <span
          className={`${
            theme === "light" ? "text-blue-400" : "text-yellow-300"
          }`}
        >
          .
        </span>{" "}
        Călătorești
        <span
          className={`${
            theme === "light" ? "text-blue-400" : "text-yellow-300"
          }`}
        >
          .
        </span>
      </p>

      <p
        className={`mt-10 text-md max-w-2xl mx-auto transition-colors ${
          theme === "light" ? "text-[#274970]/60" : "text-blue-200"
        }`}
      >
        Creează în câteva secunde itinerarii perfecte, personalizate pentru
        tine.
      </p>

      <button
        onClick={onStart}
        className={`mt-10 text-sm font-semibold px-7 py-3 rounded-full shadow-xl hover:scale-105 transition border ${
          theme === "light"
            ? "bg-[#3f6794]/80 text-white border-[#3f6794]/80 hover:bg-[#3f6794]/90 "
            : "text-white border-blue-200 hover:bg-blue-800/30"
        }`}
      >
        Începe acum - e{" "}
        <span
          className={`${
            theme === "light" ? "text-blue-300 font-bold" : "text-yellow-300/90"
          }`}
        >
          gratuit!
        </span>
      </button>
    </section>
  );
};

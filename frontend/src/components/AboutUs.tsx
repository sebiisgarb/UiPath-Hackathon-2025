import { useTheme } from "../context/ThemeContext";

export const AboutUs = () => {
  const { theme } = useTheme();
  return (
    <section
      className={`max-w-5xl mx-auto px-4 py-16 text-center backdrop-blur-sm rounded-3xl shadow-xl border  mt-12 ${
        theme === "light"
          ? "bg-[#619bde]/10 border-[#30537b]/30"
          : "bg-black/20 border-yellow-300/40"
      }`}
    >
      <h2
        className={`text-4xl font-bold ${
          theme === "light" ? "text-[#3f6794]/80" : "text-white"
        } drop-shadow-lg pb-7`}
      >
        Despre Noi
      </h2>

      <p
        className={`mt-6 text-md leading-relaxed max-w-3xl mx-auto ${
          theme === "light" ? "text-[#274970]/50" : "text-white/90"
        }`}
      >
        La{" "}
        <span
          className={`${
            theme === "light" ? "text-blue-400" : "text-yellow-300"
          } font-medium`}
        >
          SkyPath
        </span>{" "}
        reinventăm modul în care planifici călătoriile folosind tehnologie de
        ultimă generație. Combinăm inteligența artificială, automatizările și
        datele live pentru a genera itinerarii rapide, precise și personalizate.
        Misiunea noastră este să oferim o experiență de planificare fluidă,
        inteligentă și adaptată fiecărui utilizator.
      </p>
    </section>
  );
};

import { Sun, Moon } from "lucide-react";
import { useTheme } from "../context/ThemeContext";

interface HeaderProps {
  onNewPlan: () => void;
  steps?: string[];
  currentStep?: number;
  showStepper?: boolean;
  hasGenerated?: boolean;
}

export function Header({
  onNewPlan,
  steps = [],
  currentStep = 0,
  showStepper = false,
  hasGenerated = false,
}: HeaderProps) {
  const { theme, toggleTheme } = useTheme();

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        theme === "light"
          ? "bg-white/10 backdrop-blur-md shadow-sm"
          : "bg-[#0F233C]/80 backdrop-blur-md shadow-lg shadow-blue-900/20"
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between gap-4">
        {/* Left: Logo */}
        <h1
          className={`text-xl font-bold transition-colors ${
            theme === "light" ? "text-yellow-300" : "text-white"
          }`}
          style={{ fontFamily: "Poppins, sans-serif" }}
        >
          SkyPath
        </h1>

        {/* Center: Compact Stepper */}
        {showStepper && steps.length > 0 && (
          <div className="flex items-center gap-1 md:gap-2 overflow-x-auto scrollbar-none px-2 py-1 rounded-xl bg-white/60 dark:bg-white/5 backdrop-blur-sm border border-blue-200/40 dark:border-cyan-700/40">
            {steps.map((step, index) => {
              const completed = index < currentStep || hasGenerated;
              const active = index === currentStep && !hasGenerated;
              return (
                <div key={step} className="flex items-center">
                  <div
                    className={`flex items-center gap-1 px-2 py-1 rounded-lg text-[10px] font-medium whitespace-nowrap transition-all border ${
                      completed
                        ? theme === "light"
                          ? "bg-green-100 border-green-300 text-green-700"
                          : "bg-yellow-300/10 border-yellow-400/40 text-yellow-300"
                        : active
                        ? theme === "light"
                          ? "bg-blue-100 border-blue-300 text-blue-700"
                          : "bg-blue-900/30 border-blue-600/40 text-blue-300"
                        : theme === "light"
                        ? "bg-transparent border-blue-200 text-gray-600"
                        : "bg-transparent border-blue-700/40 text-gray-300"
                    }`}
                  >
                    <span
                      className={`w-4 h-4 inline-flex items-center justify-center rounded-full text-[9px] font-bold ${
                        completed
                          ? theme === "light"
                            ? "bg-green-400 text-white"
                            : "bg-yellow-300/20 text-white pt-0.5"
                          : active
                          ? theme === "light"
                            ? "bg-blue-500 text-white"
                            : "bg-blue-300/30 text-white"
                          : theme === "light"
                          ? "bg-gray-200 text-gray-600"
                          : "bg-[#13273F] text-gray-400"
                      }`}
                    >
                      {completed ? "✓" : index + 1}
                    </span>
                    {step}
                  </div>
                  {index < steps.length - 1 && (
                    <span className="mx-1 text-[10px] opacity-40">›</span>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* Right: Actions */}
        <div className="flex items-center gap-2 md:gap-3">
          {showStepper && (
            <button
              onClick={onNewPlan}
              className={`hidden sm:inline px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                theme === "light"
                  ? "bg-blue-100 text-blue-700 hover:bg-blue-200"
                  : "bg-[#13273F] text-cyan-300 hover:bg-[#1d3857] border border-cyan-500/20"
              }`}
            >
              New Plan
            </button>
          )}
          <button
            onClick={toggleTheme}
            className={`p-2 rounded-full transition-all duration-500 ${
              theme === "light"
                ? "bg-white/20 text-yellow-500 hover:bg-blue-200/40 hover:text-blue-400 hover:rotate-180 shadow-lg shadow-blue-500/20"
                : "bg-[#13273F]  text-yellow-300 hover:text-yellow-600 hover:bg-[#1a3450] hover:rotate-180 shadow-lg shadow-cyan-500/20"
            }`}
            aria-label="Toggle theme"
          >
            {theme === "light" ? (
              <Sun className="w-4 h-4" />
            ) : (
              <Moon className="w-4 h-4" />
            )}
          </button>
        </div>
      </div>
    </header>
  );
}

export default Header;

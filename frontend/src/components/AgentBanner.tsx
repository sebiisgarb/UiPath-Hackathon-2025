/**
 * Agent Banner Component
 * Displays the currently active agent and processing step
 */

import { ProcessStep } from "../types/websocket";

interface AgentBannerProps {
  agent: string;
  step?: ProcessStep;
}

// Step display names in Romanian
const stepNames: Record<ProcessStep, string> = {
  initializing: "Inițializare",
  understanding_request: "Înțelegere cerere",
  analyzing_options: "Analizare opțiuni",
  delegating_to_agent: "Delegare către agent",
  searching_flights: "Căutare zboruri",
  optimizing_flights: "Optimizare preț",
  searching_hotels: "Căutare hoteluri",
  searching_activities: "Căutare activități",
  combining_results: "Procesare rezultate",
  generating_response: "Generare răspuns",
  completed: "Finalizat",
};

// Agent icons
const agentIcons: Record<string, string> = {
  "Agentul de Zboruri": "✈️",
  "Agentul Optimizator de Zboruri": "💰",
  "Agentul de Cazare": "🏨",
  "Agentul de Itinerar": "🎭",
  "Agentul de Planificare": "🗺️",
};

export const AgentBanner = ({ agent, step }: AgentBannerProps) => {
  const icon = agentIcons[agent] || "🤖";
  const stepName = step ? stepNames[step] : "";

  return (
    <div className="agent-banner animate-slide-down">
      <div className="agent-icon">{icon}</div>
      <div className="agent-info">
        <div className="agent-name">{agent}</div>
        {stepName && <div className="agent-status">{stepName}</div>}
      </div>

      <style>{`
        .agent-banner {
          display: flex;
          align-items: center;
          padding: 12px 16px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-radius: 8px;
          gap: 12px;
          margin-bottom: 16px;
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }

        .agent-icon {
          font-size: 32px;
          line-height: 1;
        }

        .agent-info {
          flex: 1;
        }

        .agent-name {
          font-weight: 600;
          font-size: 16px;
          margin-bottom: 2px;
        }

        .agent-status {
          font-size: 14px;
          opacity: 0.9;
        }

        @keyframes slide-down {
          from {
            transform: translateY(-100%);
            opacity: 0;
          }
          to {
            transform: translateY(0);
            opacity: 1;
          }
        }

        .animate-slide-down {
          animation: slide-down 0.3s ease-out;
        }
      `}</style>
    </div>
  );
};

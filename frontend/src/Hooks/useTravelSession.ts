import { useEffect, useState } from "react";
import axios from "axios";

const SESSION_KEY = "travel_session_id";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

export function useTravelSession() {
  const [session, setSession] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // Load sessionId from localStorage once
  const sessionId = localStorage.getItem(SESSION_KEY);

  // Fetch session state
  const loadSession = async () => {
    if (!sessionId) {
      setLoading(false);
      return;
    }
    try {
      const res = await api.get("/chat/", {
        params: { sessionId },
        headers: { "X-Session-Id": sessionId },
      });
      setSession(res.data);
    } catch {
      console.warn("No existing session");
    }
    setLoading(false);
  };

  const updateState = async (updates: any) => {
    if (!sessionId) return;

    const res = await api.post("/chat/state/", {
      sessionId,
      updates,
    });

    setSession((prev: any) => ({
      ...prev,
      state: { ...prev.state, ...updates },
    }));

    return res.data;
  };

  useEffect(() => {
    loadSession();
  }, []);

  return {
    session,
    loading,
    updateState,
  };
}

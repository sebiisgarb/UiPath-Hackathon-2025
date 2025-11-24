import axios from "axios";

export interface ChatResponse {
  reply: string;
  session_id: string;
  state: any;
  history: any[];
  data?: {
    flights?: any[];
    hotels?: any[];
    itinerary?: any[];
  };
}

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  withCredentials: false,
});

// 🔑 SESSION LOCAL STORAGE
const SESSION_KEY = "travel_session_id";

export const getSessionId = () => localStorage.getItem(SESSION_KEY);

export const saveSessionId = (id: string) =>
  localStorage.setItem(SESSION_KEY, id);

// ===============================================================
// 🔥 sendChatMessage — acceptă text SAU FormData
// ===============================================================
export const sendChatMessage = async (
  payload: string | FormData
): Promise<ChatResponse> => {
  let sessionId = getSessionId();

  const isForm = payload instanceof FormData;

  let body: any = undefined;

  if (isForm) {
    // 📌 FormData — îl trimitem direct
    payload.append("sessionId", sessionId || "");
    body = payload;
  } else {
    // 📌 Text — îl punem în JSON normal
    body = {
      message: payload,
      sessionId: sessionId || undefined,
    };
  }

  const res = await api.post("/chat/", body, {
    headers: {
      ...(isForm
        ? { "Content-Type": "multipart/form-data" }
        : { "Content-Type": "application/json" }),
      ...(sessionId ? { "X-Session-Id": sessionId } : {}),
    },
  });

  // First time → save sessionId
  if (!sessionId && res.data?.session_id) {
    saveSessionId(res.data.session_id);
  }

  return res.data;
};

// ===============================================================
// 🔍 fetchChatState — read entire session state from backend
// ===============================================================
export const fetchChatState = async () => {
  const sessionId = getSessionId();
  if (!sessionId) return null;

  const res = await api.get(`/chat/?sessionId=${sessionId}`, {
    headers: {
      "X-Session-Id": sessionId,
    },
  });

  return res.data;
};

// ===============================================================
// 🖼️ sendLocateImage — trimite imagine pentru identificarea orașului
// ===============================================================
export interface CityAnalysis {
  city: string | null;
  country: string | null;
  confidence: number | null;
  reasoning: string | null;
  fallback: boolean;
  raw_text?: string;
}

export const locateCity = async (
  file: File,
  hint?: string
): Promise<CityAnalysis> => {
  const form = new FormData();
  form.append("image", file);
  if (hint) form.append("hint", hint);
  const sessionId = getSessionId();
  if (sessionId) form.append("sessionId", sessionId);

  const res = await api.post("/chat/locate_city/", form, {
    headers: {
      "Content-Type": "multipart/form-data",
      ...(sessionId ? { "X-Session-Id": sessionId } : {}),
    },
  });
  return (
    res.data?.data || {
      city: null,
      country: null,
      confidence: null,
      reasoning: null,
      fallback: true,
    }
  );
};

import { useState } from "react";
import {
  ChatResponse,
  sendChatMessage,
  locateCity,
  CityAnalysis,
} from "../Service/ChatService";

export const useTravelChat = () => {
  const [loading, setLoading] = useState(false);
  const [reply, setReply] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const [imageLoading, setImageLoading] = useState(false);

  // ⬇ acceptă string SAU FormData
  const sendMessage = async (
    payload: string | FormData
  ): Promise<ChatResponse | null> => {
    try {
      setLoading(true);
      setError(null);

      // ChatService știe deja să detecteze FormData și să schimbe header-ele
      const data: ChatResponse = await sendChatMessage(payload);
      setReply(data.reply);

      return data;
    } catch (err: any) {
      setError(err.response?.data?.error || err.message || "Unexpected error");
      return null;
    } finally {
      setLoading(false);
    }
  };

  return {
    sendMessage,
    reply,
    loading,
    error,
    imageLoading,
    locateCity: async (
      file: File,
      hint?: string
    ): Promise<CityAnalysis | null> => {
      try {
        setImageLoading(true);
        setError(null);
        return await locateCity(file, hint);
      } catch (err: any) {
        setError(
          err.response?.data?.error || err.message || "Unexpected error"
        );
        return null;
      } finally {
        setImageLoading(false);
      }
    },
  };
};

import { useState, useEffect, useRef } from "react";
import {
  Sparkles,
  Send,
  BotMessageSquare,
  User2,
  Volume2,
  Mic,
  MicOff,
  ImagePlus,
  X,
} from "lucide-react";
import { useTheme } from "../context/ThemeContext";
import { useTravelChat } from "../Hooks/useChat";
import { textToSpeech } from "../Service/ttsService";
import { speechToText } from "../Service/sttService";
import { parseAIReply } from "../parseAIReply";
import React from "react";

/* ===========================================================
   🔥 ADVANCED FORMATTER – cu suport real pentru BOLD
=========================================================== */
const formatReply = (txt: string) => {
  if (!txt) return null;

  const lines = txt.split(/\n+/);

  return (
    <div className="space-y-2">
      {lines.map((line, i) => {
        let trimmed = line.trim();

        // ===== Bold converter first =====
        trimmed = trimmed.replace(
          /\*\*(.+?)\*\*/g,
          "<strong class='text-blue-300 font-semibold'>$1</strong>"
        );

        // ===== Headings (###) =====
        if (/^###\s*/.test(trimmed)) {
          return (
            <h3
              key={i}
              className="text-[15px] font-bold text-blue-300 mt-3 mb-1"
              dangerouslySetInnerHTML={{
                __html: trimmed.replace(/^###\s*/, ""),
              }}
            />
          );
        }

        // ===== Section titles "xxx:" =====
        if (/^[A-ZȘȚĂÎÂ].*:\s*$/.test(trimmed)) {
          return (
            <p
              key={i}
              className="font-semibold text-[14px] text-yellow-300 mt-2"
              dangerouslySetInnerHTML={{ __html: trimmed }}
            />
          );
        }

        // ===== Bullet list =====
        if (/^[-•*]\s+/.test(trimmed)) {
          return (
            <li
              key={i}
              className="ml-4 text-[14px] leading-relaxed"
              dangerouslySetInnerHTML={{
                __html: trimmed.replace(/^[-•*]\s+/, ""),
              }}
            />
          );
        }

        // ===== Numbered list =====
        if (/^\d+\.\s+/.test(trimmed)) {
          const num = trimmed.match(/^\d+\./)?.[0] ?? "";
          return (
            <p key={i} className="ml-2 text-[14px] leading-relaxed">
              <span className="font-bold text-blue-400">{num}</span>{" "}
              <span
                dangerouslySetInnerHTML={{
                  __html: trimmed.replace(/^\d+\.\s+/, ""),
                }}
              />
            </p>
          );
        }

        // ===== Links =====
        trimmed = trimmed.replace(
          /(https?:\/\/[^\s]+)/g,
          "<a href='$1' target='_blank' class='underline text-cyan-300'>$1</a>"
        );

        // ===== Default paragraph =====
        return (
          <p
            key={i}
            className="text-[14px] leading-relaxed whitespace-pre-wrap"
            dangerouslySetInnerHTML={{ __html: trimmed }}
          />
        );
      })}
    </div>
  );
};

/* ===========================================================
   COMPONENTĂ
=========================================================== */

interface InputCardProps {
  isMinimized: boolean;
  isLoading?: boolean;
  onCaptureDestination?: (value: string) => void;
  onCaptureDates?: (value: string) => void;

  onBackendComplete?: () => void;
  onBackendData?: (data?: {
    flights?: any[];
    hotels?: any[];
    itinerary?: any[];
  }) => void;

  flights?: any[];
  hotels?: any[];
  onSelectFlight?: (f: any) => void;
  onSelectHotel?: (h: any) => void;
}

export function InputCard({
  isMinimized,
  isLoading,
  onCaptureDestination,
  onCaptureDates,
  onBackendComplete,
  onBackendData,
  flights = [],
  hotels = [],
  onSelectFlight,
  onSelectHotel,
}: InputCardProps) {
  const { theme } = useTheme();
  const {
    sendMessage: sendChatMessage,
    loading: chatLoading,
    imageLoading,
    locateCity,
  } = useTravelChat();

  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<
    { id: number; role: "bot" | "user"; content: string }[]
  >([]);
  const [attachedImage, setAttachedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const imageInputRef = useRef<HTMLInputElement | null>(null);
  const [imageMode, setImageMode] = useState<
    "idle" | "pending" | "analyzing" | "done"
  >("idle");
  const [imageAnalysis, setImageAnalysis] = useState<{
    city: string | null;
    country: string | null;
    confidence: number | null;
    reasoning: string | null;
    fallback: boolean;
  } | null>(null);

  const [insights, setInsights] = useState({
    airports: [] as string[],
    dates: [] as string[],
    travelers: null as number | null,
    flightChoice: null as number | null,
    hotelChoice: null as number | null,
  });

  const listRef = useRef<HTMLDivElement | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const initialPrompt =
    "Salut! Spune-mi destinația ta și perioada aproximativă. Poți continua cu preferințe (zbor, cazare, buget). Când ai terminat scrie 'gata' sau 'finalizează'.";

  /* ===========================================================
     TTS
  =========================================================== */
  const playTTS = async (text: string) => {
    try {
      const audioBlob = await textToSpeech(text);
      const url = URL.createObjectURL(audioBlob);

      if (!audioRef.current) audioRef.current = new Audio();
      audioRef.current.src = url;
      audioRef.current.play();
    } catch (e) {
      console.error("TTS error:", e);
    }
  };

  /* ===========================================================
     STT
  =========================================================== */
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const [recording, setRecording] = useState(false);

  const toggleRecording = async () => {
    if (!recording) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        const recorder = new MediaRecorder(stream);
        mediaRecorderRef.current = recorder;
        audioChunksRef.current = [];

        recorder.ondataavailable = (e) => audioChunksRef.current.push(e.data);
        recorder.onstop = async () => {
          stream.getTracks().forEach((t) => t.stop());
          const audioBlob = new Blob(audioChunksRef.current, {
            type: "audio/webm",
          });
          try {
            const textResult = await speechToText(audioBlob);
            setInput((prev) => prev + (prev ? " " : "") + textResult);
          } catch (err) {
            console.error("STT error:", err);
          }
        };

        recorder.start();
        setRecording(true);
      } catch (err) {
        console.error("Microphone error:", err);
      }
    } else {
      mediaRecorderRef.current?.stop();
      setRecording(false);
    }
  };

  /* ===========================================================
     INITIAL MESSAGE
  =========================================================== */
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([{ id: Date.now(), role: "bot", content: initialPrompt }]);
    }
  }, []);

  useEffect(() => {
    listRef.current?.scrollTo({
      top: listRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  /* ===========================================================
     SEND MESSAGE + PARSING
  =========================================================== */
  const sendMessage = async () => {
    const text = input.trim();
    if (!text && !attachedImage) return;

    // SWITCH: If image attached and not yet analyzed -> analyze first
    if (attachedImage && imageMode === "pending") {
      const userDisplay = text || "[Imagine pentru analiză]";
      setMessages((p) => [
        ...p,
        { id: Date.now(), role: "user", content: userDisplay },
      ]);
      setImageMode("analyzing");
      try {
        const analysis = await locateCity(attachedImage, text || undefined);
        if (!analysis) {
          setMessages((p) => [
            ...p,
            {
              id: Date.now() + 1,
              role: "bot",
              content: "Eroare la analiza imaginii.",
            },
          ]);
          setImageMode("pending");
          return;
        }
        setImageAnalysis(analysis);
        setImageMode("done");
        let locateMsg = analysis.fallback
          ? "Nu am putut identifica orașul din imagine. Poți încerca cu o altă fotografie sau spune-mi în ce oraș dorești să călătorești."
          : `Văd că este ${analysis.city}${
              analysis.country ? ", " + analysis.country : ""
            }! 🌍`;
        // Don't show technical details like confidence and reasoning
        setMessages((p) => [
          ...p,
          { id: Date.now() + 1, role: "bot", content: locateMsg },
        ]);

        // If user provided text, auto-continue to chat
        if (text) {
          setImageMode("done");
          // Clear input and prepare enriched text
          setInput("");
          let enrichedText = text;
          if (!analysis.fallback) {
            enrichedText += `\n[Context imagine: oras=${analysis.city}, tara=${analysis.country}, confidence=${analysis.confidence}]`;
          }

          // Send to chat automatically
          try {
            const data = await sendChatMessage(enrichedText);
            if (!data || !data.reply)
              throw new Error("Empty response from backend");
            setMessages((p) => [
              ...p,
              { id: Date.now() + 3, role: "bot", content: data.reply },
            ]);
            const parsed = parseAIReply(data.reply);
            if (onBackendData && data.data) onBackendData(data.data);
            setInsights((prev) => ({
              airports: parsed.airports.length
                ? parsed.airports
                : prev.airports,
              dates: parsed.dates.length ? parsed.dates : prev.dates,
              travelers:
                parsed.travelers !== null ? parsed.travelers : prev.travelers,
              flightChoice:
                parsed.flightChoice !== null
                  ? parsed.flightChoice
                  : prev.flightChoice,
              hotelChoice:
                parsed.hotelChoice !== null
                  ? parsed.hotelChoice
                  : prev.hotelChoice,
            }));
            if (parsed.airports.length >= 2 && onCaptureDestination)
              onCaptureDestination(parsed.airports[1]);
            if (parsed.dates.length > 0 && onCaptureDates)
              onCaptureDates(parsed.dates[0]);
            if (parsed.flightChoice && flights.length > 0 && onSelectFlight) {
              const index = parsed.flightChoice - 1;
              if (flights[index]) onSelectFlight(flights[index]);
            }
            if (parsed.hotelChoice && hotels.length > 0 && onSelectHotel) {
              const index = parsed.hotelChoice - 1;
              if (hotels[index]) onSelectHotel(hotels[index]);
            }
          } catch (err) {
            setMessages((p) => [
              ...p,
              { id: Date.now() + 4, role: "bot", content: "Eroare la server." },
            ]);
          } finally {
            setAttachedImage(null);
            setImagePreview(null);
            setImageMode("idle");
            setImageAnalysis(null);
          }
        } else {
          // No text provided, wait for user to send message
          setMessages((p) => [
            ...p,
            {
              id: Date.now() + 2,
              role: "bot",
              content:
                "Apasă din nou pe trimite pentru a continua conversația cu contextul imaginii.",
            },
          ]);
          // Clear image preview immediately
          setAttachedImage(null);
          setImagePreview(null);
        }
      } catch (err) {
        setMessages((p) => [
          ...p,
          {
            id: Date.now() + 1,
            role: "bot",
            content: "Eroare la analiza imaginii.",
          },
        ]);
        setAttachedImage(null);
        setImagePreview(null);
        setImageMode("idle");
        setImageAnalysis(null);
      }
      return; // Stop here, don't send to /chat yet
    }

    // Normal chat send (with optional enriched context from image)
    const userDisplay = text || "[Fără text]";
    setMessages((p) => [
      ...p,
      { id: Date.now(), role: "user", content: userDisplay },
    ]);
    setInput("");
    let enrichedText = text;
    if (
      attachedImage &&
      imageMode === "done" &&
      imageAnalysis &&
      !imageAnalysis.fallback
    ) {
      enrichedText += `\n[Context imagine: oras=${imageAnalysis.city}, tara=${imageAnalysis.country}, confidence=${imageAnalysis.confidence}]`;
    }
    if (!enrichedText) enrichedText = "Mesaj fără text.";
    try {
      const data = await sendChatMessage(enrichedText);
      if (!data || !data.reply) throw new Error("Empty response from backend");
      setMessages((p) => [
        ...p,
        { id: Date.now() + 2, role: "bot", content: data.reply },
      ]);
      const parsed = parseAIReply(data.reply);
      if (onBackendData && data.data) onBackendData(data.data);
      setInsights((prev) => ({
        airports: parsed.airports.length ? parsed.airports : prev.airports,
        dates: parsed.dates.length ? parsed.dates : prev.dates,
        travelers:
          parsed.travelers !== null ? parsed.travelers : prev.travelers,
        flightChoice:
          parsed.flightChoice !== null
            ? parsed.flightChoice
            : prev.flightChoice,
        hotelChoice:
          parsed.hotelChoice !== null ? parsed.hotelChoice : prev.hotelChoice,
      }));
      if (parsed.airports.length >= 2 && onCaptureDestination)
        onCaptureDestination(parsed.airports[1]);
      if (parsed.dates.length > 0 && onCaptureDates)
        onCaptureDates(parsed.dates[0]);
      if (parsed.flightChoice && flights.length > 0 && onSelectFlight) {
        const index = parsed.flightChoice - 1;
        if (flights[index]) onSelectFlight(flights[index]);
      }
      if (parsed.hotelChoice && hotels.length > 0 && onSelectHotel) {
        const index = parsed.hotelChoice - 1;
        if (hotels[index]) onSelectHotel(hotels[index]);
      }
    } catch (err) {
      setMessages((p) => [
        ...p,
        { id: Date.now() + 3, role: "bot", content: "Eroare la server." },
      ]);
    } finally {
      if (attachedImage) {
        setAttachedImage(null);
        setImagePreview(null);
        setImageMode("idle");
        setImageAnalysis(null);
      }
    }
  };

  /* ===========================================================
     UI
  =========================================================== */
  const handleKey = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  /* ===========================================================
   🤖 LOADING BUBBLE (AI typing)
=========================================================== */
  const AILoadingBubble = () => {
    return (
      <div className="flex items-center gap-2">
        {/* Bot icon */}
        <BotMessageSquare className="w-6 h-6 text-yellow-300 opacity-70" />

        {/* Bubble */}
        <div className="bg-[#2b4363] text-white px-4 py-2 rounded-2xl flex gap-2 items-center">
          <span className="w-2 h-2 bg-white rounded-full animate-bounce [animation-delay:0ms]" />
          <span className="w-2 h-2 bg-white rounded-full animate-bounce [animation-delay:150ms]" />
          <span className="w-2 h-2 bg-white rounded-full animate-bounce [animation-delay:300ms]" />
        </div>
      </div>
    );
  };

  return (
    <div
      className={`${
        isMinimized ? "w-full md:w-[380px] fixed" : "w-full max-w-2xl"
      } rounded-3xl flex flex-col h-[70vh] md:h-[78vh] overflow-hidden border transition-colors duration-300 ${
        theme === "light"
          ? "bg-white/95 border-gray-200 shadow-lg"
          : "bg-gradient-to-b from-[#0f1e2b] to-[#1d3347] border-cyan-900/50 shadow-[0_0_0_1px_rgba(0,0,0,0.6)]"
      }`}
    >
      {/* HEADER */}
      <div
        className={`flex items-center gap-3 px-6 py-5 border-b ${
          theme === "light"
            ? "bg-gradient-to-r from-blue-50 to-white border-gray-200"
            : "bg-[#152536] border-cyan-900/40"
        }`}
      >
        <Sparkles className="w-6 h-6 text-blue-400" />
        <h2
          className={`text-lg font-semibold ${
            theme === "light" ? "text-gray-800" : "text-white"
          }`}
        >
          AI Travel Assistant
        </h2>
      </div>

      {/* CHAT MESSAGES */}
      <div ref={listRef} className="flex-1 px-6 py-4 space-y-6 overflow-y-auto">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`flex items-start gap-3 ${
              m.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            {/* BOT SIDE ICON */}
            {m.role === "bot" && (
              <div className="flex items-center gap-2 mt-1.5">
                <BotMessageSquare className="w-6 h-6 text-yellow-300" />
                <button
                  onClick={() => playTTS(m.content)}
                  className="p-1 rounded-full hover:bg-white/10"
                >
                  <Volume2 className="w-4 h-4 text-cyan-300" />
                </button>
              </div>
            )}

            <div
              className={`max-w-[70%] rounded-2xl px-4 py-3 text-sm ${
                m.role === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-[#2b4363] text-white"
              }`}
            >
              {m.role === "bot" ? formatReply(m.content) : m.content}
            </div>

            {/* USER ICON */}
            {m.role === "user" && (
              <User2 className="w-6 h-6 mt-1 text-blue-400" />
            )}
          </div>
        ))}

        {/* LOADING */}
        {(isLoading || chatLoading || imageLoading) && (
          <div className="mt-2">
            <AILoadingBubble />
          </div>
        )}

        {/* INSIGHTS PANEL */}
        {(insights.airports.length ||
          insights.dates.length ||
          insights.travelers !== null) && (
          <div
            className={`mt-4 p-4 rounded-2xl text-xs border ${
              theme === "light"
                ? "bg-white/70 border-blue-200"
                : "bg-[#1d3347]/70 border-cyan-800/40"
            } backdrop-blur-sm space-y-2`}
          >
            <p className="font-semibold text-[11px] uppercase tracking-wide opacity-70">
              Date extrase
            </p>

            {insights.airports.length > 0 && (
              <p>
                <span className="font-medium">Aeroport(e):</span>{" "}
                {insights.airports.join(", ")}
              </p>
            )}
            {insights.dates.length > 0 && (
              <p>
                <span className="font-medium">Data:</span>{" "}
                {insights.dates.join(" | ")}
              </p>
            )}
            {insights.travelers !== null && (
              <p>
                <span className="font-medium">Adulți:</span>{" "}
                {insights.travelers}
              </p>
            )}
            {insights.flightChoice !== null && (
              <p>
                <span className="font-medium">Zbor selectat:</span>{" "}
                {insights.flightChoice}
              </p>
            )}
            {insights.hotelChoice !== null && (
              <p>
                <span className="font-medium">Hotel selectat:</span>{" "}
                {insights.hotelChoice}
              </p>
            )}
          </div>
        )}
      </div>

      {/* INPUT BAR */}
      <div className="px-6 pb-6">
        {/* PREVIEW IMAGINE ATAȘATĂ */}
        {imagePreview && attachedImage && (
          <div
            className={`mb-3 flex items-center gap-3 p-2 rounded-xl border ${
              theme === "light"
                ? "bg-gray-100 border-gray-300"
                : "bg-[#23384d] border-gray-900/40"
            }`}
          >
            <img
              src={imagePreview}
              alt="preview"
              className="h-16 w-16 object-cover rounded-lg border border-white/20"
            />
            <div className="flex-1 text-xs truncate">
              <p className="font-medium">{attachedImage.name}</p>
              <p className="opacity-70">
                {(attachedImage.size / 1024).toFixed(1)} KB
              </p>
            </div>
            <button
              onClick={() => {
                setAttachedImage(null);
                setImagePreview(null);
                setImageMode("idle");
                setImageAnalysis(null);
              }}
              className="h-8 w-8 flex items-center justify-center rounded-full bg-red-500 text-white hover:bg-red-600"
              title="Elimină"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        )}
        <div
          className={`rounded-2xl flex items-end gap-3 p-3 border duration-300 ${
            theme === "light"
              ? "bg-gray-100 border-gray-300"
              : "bg-[#23384d] border-gray-900/40"
          }`}
        >
          {/* BUTON ATAȘARE IMAGINE */}
          <div className="flex flex-col items-center">
            <button
              onClick={() => imageInputRef.current?.click()}
              className={`h-10 w-10 flex items-center justify-center rounded-full ${
                theme === "light"
                  ? "bg-gray-200 text-gray-700 hover:bg-gray-300"
                  : "bg-[#35516e] text-white hover:bg-[#416789]"
              }`}
              title="Atașează imagine"
            >
              <ImagePlus />
            </button>
            <input
              type="file"
              accept="image/*"
              ref={imageInputRef}
              className="hidden"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (!file) return;
                setAttachedImage(file);
                setImageMode("pending");
                const reader = new FileReader();
                reader.onload = (ev) => {
                  setImagePreview(ev.target?.result as string);
                };
                reader.readAsDataURL(file);
              }}
            />
          </div>
          <button
            onClick={toggleRecording}
            className={`h-10 w-10 flex items-center justify-center rounded-full ${
              recording
                ? "bg-red-500 text-white"
                : theme === "light"
                ? "bg-gray-200 text-gray-700"
                : "bg-[#35516e] text-white"
            }`}
          >
            {recording ? <MicOff /> : <Mic />}
          </button>

          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKey}
            className={`flex-1 resize-none h-10 bg-transparent focus:outline-none placeholder-opacity-70 ${
              theme === "light"
                ? "text-gray-800 placeholder-gray-500"
                : "text-white placeholder-white placeholder-opacity-70"
            }`}
            placeholder="Scrie aici..."
          />

          <button
            onClick={sendMessage}
            disabled={!input.trim() && !attachedImage}
            className={`h-10 w-10 rounded-full flex items-center justify-center transition-colors duration-200 disabled:opacity-40 ${
              theme === "light"
                ? "bg-blue-600 hover:bg-blue-500 text-white"
                : "bg-[#35516e] hover:bg-white-500 text-white"
            }`}
            title={
              attachedImage && imageMode === "pending"
                ? "Analizează imaginea"
                : attachedImage && imageMode === "done"
                ? "Trimite cu context"
                : "Trimite mesaj"
            }
          >
            <Send />
          </button>
        </div>
        {attachedImage && (
          <div className="mt-2 text-xs opacity-70">
            {imageMode === "pending" &&
              "Mod analiză imagine: apasă trimite pentru identificare."}
            {imageMode === "analyzing" && "Se analizează imaginea..."}
            {imageMode === "done" &&
              "Imagine analizată: apasă trimite pentru a continua conversația."}
          </div>
        )}
      </div>
    </div>
  );
}

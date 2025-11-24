/**
 * React Hook for WebSocket-based Chat with Agent Tracking
 * Provides real-time updates on agent activity and processing steps
 */

import { useState, useEffect, useRef, useCallback } from "react";
import { WebSocketService } from "../Service/WebSocketService";
import {
  AnyWebSocketMessage,
  ProcessStep,
  FeedbackMessage,
  MessageCompleteMessage,
} from "../types/websocket";

export interface ChatMessage {
  id: number;
  role: "user" | "assistant" | "feedback";
  content: string;
  timestamp: string;
  agent?: string;
  step?: ProcessStep;
}

export interface UseWebSocketChatReturn {
  isConnected: boolean;
  messages: ChatMessage[];
  currentAgent: string | null;
  currentStep: ProcessStep | null;
  isProcessing: boolean;
  sendMessage: (message: string) => void;
  clearMessages: () => void;
  error: string | null;
}

export const useWebSocketChat = (sessionId: string): UseWebSocketChatReturn => {
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [currentAgent, setCurrentAgent] = useState<string | null>(null);
  const [currentStep, setCurrentStep] = useState<ProcessStep | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const wsServiceRef = useRef<WebSocketService | null>(null);

  // Initialize WebSocket connection
  useEffect(() => {
    const wsService = new WebSocketService(sessionId);
    wsServiceRef.current = wsService;

    wsService
      .connect()
      .then(() => {
        setIsConnected(true);
        setError(null);
      })
      .catch((err) => {
        console.error("WebSocket connection failed:", err);
        setError("Failed to connect to server");
        setIsConnected(false);
      });

    // Message handler
    const unsubscribeMessage = wsService.onMessage(handleWebSocketMessage);

    // Error handler
    const unsubscribeError = wsService.onError((err) => {
      console.error("WebSocket error:", err);
      setError("Connection error");
    });

    // Close handler
    const unsubscribeClose = wsService.onClose(() => {
      setIsConnected(false);
    });

    // Cleanup
    return () => {
      unsubscribeMessage();
      unsubscribeError();
      unsubscribeClose();
      wsService.disconnect();
    };
  }, [sessionId]);

  // Handle WebSocket messages
  const handleWebSocketMessage = useCallback((message: AnyWebSocketMessage) => {
    switch (message.type) {
      case "connection":
        console.log("✅ Connection confirmed:", message);
        break;

      case "processing_started":
        setIsProcessing(true);
        setCurrentStep("understanding_request");
        setError(null);
        break;

      case "feedback":
        handleFeedbackMessage(message as FeedbackMessage);
        break;

      case "message_complete":
        handleCompleteMessage(message as MessageCompleteMessage);
        break;

      case "error":
        setIsProcessing(false);
        setCurrentAgent(null);
        setError(message.error);
        console.error("❌ Server error:", message.error);
        break;

      default:
        console.log("Unknown message type:", message);
    }
  }, []);

  // Handle feedback messages
  const handleFeedbackMessage = (message: FeedbackMessage) => {
    // Update current agent if provided
    if (message.agent) {
      setCurrentAgent(message.agent);
    }

    // Update current step
    setCurrentStep(message.step);

    // Add feedback message to chat
    setMessages((prev) => [
      ...prev,
      {
        id: Date.now(),
        role: "feedback",
        content: message.message,
        timestamp: message.timestamp || new Date().toISOString(),
        agent: message.agent,
        step: message.step,
      },
    ]);
  };

  // Handle message complete
  const handleCompleteMessage = (message: MessageCompleteMessage) => {
    setIsProcessing(false);
    setCurrentAgent(null);
    setCurrentStep("completed");

    // Add assistant response to chat
    setMessages((prev) => [
      ...prev,
      {
        id: Date.now(),
        role: "assistant",
        content: message.reply,
        timestamp: message.timestamp || new Date().toISOString(),
      },
    ]);
  };

  // Send message
  const sendMessage = useCallback(
    (message: string) => {
      if (!wsServiceRef.current || !isConnected) {
        console.error("WebSocket not connected");
        setError("Not connected to server");
        return;
      }

      // Add user message to chat
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          role: "user",
          content: message,
          timestamp: new Date().toISOString(),
        },
      ]);

      // Send through WebSocket
      wsServiceRef.current.sendMessage(message);
    },
    [isConnected]
  );

  // Clear messages
  const clearMessages = useCallback(() => {
    setMessages([]);
    setCurrentAgent(null);
    setCurrentStep(null);
  }, []);

  return {
    isConnected,
    messages,
    currentAgent,
    currentStep,
    isProcessing,
    sendMessage,
    clearMessages,
    error,
  };
};

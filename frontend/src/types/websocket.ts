/**
 * WebSocket Message Types for Real-Time Agent Tracking
 */

export type WebSocketMessageType =
  | "connection"
  | "processing_started"
  | "feedback"
  | "message_complete"
  | "error";

export type ProcessStep =
  | "initializing"
  | "understanding_request"
  | "analyzing_options"
  | "delegating_to_agent"
  | "searching_flights"
  | "optimizing_flights"
  | "searching_hotels"
  | "searching_activities"
  | "combining_results"
  | "generating_response"
  | "completed";

export interface WebSocketMessage {
  type: WebSocketMessageType;
  timestamp?: string;
}

export interface ConnectionMessage extends WebSocketMessage {
  type: "connection";
  status: "connected" | "disconnected";
  session_id?: string;
  message?: string;
}

export interface ProcessingStartedMessage extends WebSocketMessage {
  type: "processing_started";
  message: string;
}

export interface FeedbackMessage extends WebSocketMessage {
  type: "feedback";
  step: ProcessStep;
  message: string;
  agent?: string;
  extra?: {
    agent_type?: string;
    task?: string;
    [key: string]: any;
  };
}

export interface MessageCompleteMessage extends WebSocketMessage {
  type: "message_complete";
  reply: string;
  state?: any;
  session_id?: string;
  data?: {
    flights?: any[];
    hotels?: any[];
    itinerary?: any[];
  };
}

export interface ErrorMessage extends WebSocketMessage {
  type: "error";
  error: string;
  details?: string;
}

export type AnyWebSocketMessage =
  | ConnectionMessage
  | ProcessingStartedMessage
  | FeedbackMessage
  | MessageCompleteMessage
  | ErrorMessage;

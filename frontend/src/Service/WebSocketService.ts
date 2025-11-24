/**
 * WebSocket Service for Real-Time Communication
 * Handles WebSocket connection, message sending, and event handling
 */

import { AnyWebSocketMessage } from "../types/websocket";

export type WebSocketEventHandler = (message: AnyWebSocketMessage) => void;
export type WebSocketErrorHandler = (error: Event) => void;
export type WebSocketCloseHandler = (event: CloseEvent) => void;

export class WebSocketService {
  private ws: WebSocket | null = null;
  private sessionId: string;
  private wsUrl: string;
  private messageHandlers: Set<WebSocketEventHandler> = new Set();
  private errorHandlers: Set<WebSocketErrorHandler> = new Set();
  private closeHandlers: Set<WebSocketCloseHandler> = new Set();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private isIntentionallyClosed = false;

  constructor(sessionId: string) {
    this.sessionId = sessionId;
    this.wsUrl = import.meta.env.VITE_WS_URL || "ws://localhost:8000";
  }

  /**
   * Connect to WebSocket server
   */
  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.isIntentionallyClosed = false;
        const url = `${this.wsUrl}/ws/chat/${this.sessionId}/`;
        console.log(`🔌 Connecting to WebSocket: ${url}`);

        this.ws = new WebSocket(url);

        this.ws.onopen = () => {
          console.log("✅ WebSocket connected");
          this.reconnectAttempts = 0;
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const message: AnyWebSocketMessage = JSON.parse(event.data);
            console.log("📨 WebSocket message:", message);
            this.messageHandlers.forEach((handler) => handler(message));
          } catch (error) {
            console.error("❌ Failed to parse WebSocket message:", error);
          }
        };

        this.ws.onerror = (error) => {
          console.error("❌ WebSocket error:", error);
          this.errorHandlers.forEach((handler) => handler(error));
          reject(error);
        };

        this.ws.onclose = (event) => {
          console.log("🔌 WebSocket closed", event);
          this.closeHandlers.forEach((handler) => handler(event));

          // Auto-reconnect if not intentionally closed
          if (!this.isIntentionallyClosed && this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(
              `🔄 Reconnecting... (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`
            );
            setTimeout(() => {
              this.connect().catch(console.error);
            }, this.reconnectDelay * this.reconnectAttempts);
          }
        };
      } catch (error) {
        console.error("❌ Failed to create WebSocket:", error);
        reject(error);
      }
    });
  }

  /**
   * Send a message through WebSocket
   */
  sendMessage(message: string): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      const payload = { message };
      console.log("📤 Sending message:", payload);
      this.ws.send(JSON.stringify(payload));
    } else {
      console.error("❌ WebSocket is not connected");
    }
  }

  /**
   * Add message event handler
   */
  onMessage(handler: WebSocketEventHandler): () => void {
    this.messageHandlers.add(handler);
    // Return unsubscribe function
    return () => {
      this.messageHandlers.delete(handler);
    };
  }

  /**
   * Add error event handler
   */
  onError(handler: WebSocketErrorHandler): () => void {
    this.errorHandlers.add(handler);
    return () => {
      this.errorHandlers.delete(handler);
    };
  }

  /**
   * Add close event handler
   */
  onClose(handler: WebSocketCloseHandler): () => void {
    this.closeHandlers.add(handler);
    return () => {
      this.closeHandlers.delete(handler);
    };
  }

  /**
   * Close WebSocket connection
   */
  disconnect(): void {
    this.isIntentionallyClosed = true;
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  /**
   * Check if WebSocket is connected
   */
  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
  }
}

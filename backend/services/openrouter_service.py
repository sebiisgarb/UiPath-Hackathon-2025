"""
OpenRouter Service for LLM Function Calling
Uses Claude Sonnet 4 via OpenRouter API with tool-calling support
"""

import os
import json
import httpx
from typing import List, Dict, Any, Optional


class OpenRouterService:
    """
    Service for interacting with OpenRouter API with function calling support.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenRouter service.
        
        Args:
            api_key: OpenRouter API key (defaults to env var OPENROUTER_API_KEY)
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OpenRouter API key not provided. Set OPENROUTER_API_KEY environment variable.")
        
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "anthropic/claude-sonnet-4"
    
    def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: str = "auto"
    ) -> Dict[str, Any]:
        """
        Send a chat completion request to OpenRouter with optional tools.
        
        Args:
            messages: List of message objects with role and content
            tools: Optional list of tool definitions in OpenAI format
            tool_choice: Tool choice strategy ('auto', 'none', or specific tool)
            
        Returns:
            OpenRouter API response
        """
        headers = {
            "Authorization": f"******
            "Content-Type": "application/json",
            "HTTP-Referer": "local",
            "X-Title": "Travel Chatbot"
        }
        
        payload = {
            "model": self.model,
            "messages": messages
        }
        
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = tool_choice
        
        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(self.base_url, headers=headers, json=payload)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"OpenRouter API error: {str(e)}")
    
    def extract_message(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract the assistant's message from the completion response.
        
        Args:
            response: OpenRouter API response
            
        Returns:
            Extracted message with content and tool_calls
        """
        if not response.get('choices') or len(response['choices']) == 0:
            raise Exception("No choices in OpenRouter response")
        
        message = response['choices'][0]['message']
        return {
            'role': message.get('role', 'assistant'),
            'content': message.get('content', ''),
            'tool_calls': message.get('tool_calls')
        }
    
    def has_tool_calls(self, message: Dict[str, Any]) -> bool:
        """
        Check if the message contains tool calls.
        
        Args:
            message: Extracted message object
            
        Returns:
            True if message has tool calls
        """
        return message.get('tool_calls') is not None and len(message.get('tool_calls', [])) > 0

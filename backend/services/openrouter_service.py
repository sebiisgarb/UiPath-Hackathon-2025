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
            "Authorization": f"Bearer {self.api_key}",
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

    # =============================================================
    # 🖼️ Multi-Modal: Identify city from an image using GPT-4o (Romanian prompt)
    # =============================================================
    def locate_city_from_image(
        self,
        image_bytes: bytes,
        user_hint: Optional[str] = None,
        model: str = "openai/gpt-4o"
    ) -> Dict[str, Any]:
        import base64, re
        b64 = base64.b64encode(image_bytes).decode('utf-8')
        mime = "image/jpeg"
        head = image_bytes[:10]
        if head.startswith(b"\x89PNG"):
            mime = "image/png"
        elif head.startswith(b"GIF"):
            mime = "image/gif"

        system_prompt = (
            "Ești un AI care recunoaște orașe. Analizează imaginea și identifică orașul și țara probabilă. "
            "Dacă nu ești măcar 60% sigur de predicția pe care o faci, răspunde EXACT cu: Nu am putut identifica orașul, încearcă cu o altă fotografie. "
            "Dacă ești suficient de sigur (≥0.60), răspunde STRICT DOAR în JSON cu cheile: city, country, confidence (0-1), reasoning."
        )
        user_text = user_hint or "Te rog identifică orașul din această fotografie." 

        messages = [
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
            {"role": "user", "content": [
                {"type": "text", "text": user_text},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}}
            ]}
        ]

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "local",
            "X-Title": "Travel Image Locator"
        }
        payload = {"model": model, "messages": messages}

        try:
            with httpx.Client(timeout=90.0) as client:
                resp = client.post(self.base_url, headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
        except httpx.HTTPError as e:
            raise Exception(f"OpenRouter image locate error: {e}")

        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        if isinstance(content, list):
            parts = []
            for part in content:
                if isinstance(part, str):
                    parts.append(part)
                elif isinstance(part, dict):
                    parts.append(part.get("text", ""))
            content = "\n".join(parts)

        fallback_phrase = "Nu am putut identifica orașul, încearcă cu o altă fotografie."
        if content.strip() == fallback_phrase:
            return {"parsed": None, "assistant_text": content, "fallback": True}

        match = re.search(r"\{[\s\S]*\}", content)
        parsed = None
        if match:
            try:
                parsed = json.loads(match.group(0))
            except Exception:
                parsed = None

        return {"parsed": parsed, "assistant_text": content, "fallback": parsed is None, "raw_response": data}

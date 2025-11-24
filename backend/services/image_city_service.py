from services.openrouter_service import OpenRouterService

FALLBACK_PHRASE = "Nu am putut identifica orașul, încearcă cu o altă fotografie."


class ImageCityService:
    def __init__(self, openrouter: OpenRouterService | None = None):
        self.openrouter = openrouter or OpenRouterService()

    def analyze(self, image_bytes: bytes, user_hint: str | None = None):
        result = self.openrouter.locate_city_from_image(image_bytes, user_hint=user_hint)
        parsed = result.get("parsed") or {}
        fallback = result.get("fallback", False)
        assistant_text = result.get("assistant_text", "")

        if fallback:
            return {
                "city": None,
                "country": None,
                "confidence": None,
                "reasoning": None,
                "fallback": True,
                "raw_text": assistant_text,
            }

        return {
            "city": parsed.get("city"),
            "country": parsed.get("country"),
            "confidence": parsed.get("confidence"),
            "reasoning": parsed.get("reasoning"),
            "fallback": False,
            "raw_text": assistant_text,
        }
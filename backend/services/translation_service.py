from openai import OpenAI
import logging
from typing import Dict
import time
import os

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self, openrouter_api_key: str = None):
        """Initialize OpenRouter client for translation using OpenAI SDK compatibility"""
        api_key = openrouter_api_key or os.getenv("OPENROUTER_API_KEY")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.model = "google/gemini-2.0-flash-exp:free"
        self.translation_cache: Dict[str, str] = {}
        self.cache_timestamps: Dict[str, float] = {}

    def translate_to_urdu(self, text: str, ttl: int = 3600) -> str:
        """Translate English text to Urdu with caching"""
        # Create cache key
        cache_key = f"en_to_ur_{hash(text)}"

        # Check if translation is in cache and not expired
        if cache_key in self.translation_cache:
            if time.time() - self.cache_timestamps.get(cache_key, 0) < ttl:
                logger.info("Returning cached translation")
                return self.translation_cache[cache_key]

        # Call OpenRouter API for translation using OpenAI SDK
        try:
            system_prompt = self._get_urdu_translation_system_prompt()

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=8000
            )

            translated_text = response.choices[0].message.content.strip()

            # Cache the translation
            self.translation_cache[cache_key] = translated_text
            self.cache_timestamps[cache_key] = time.time()

            logger.info(f"Translated text to Urdu (length: {len(translated_text)} chars)")
            return translated_text

        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            # Return a professional fallback response
            return f"Translation unavailable: {text[:100]}..."

    def _get_urdu_translation_system_prompt(self) -> str:
        """Get the system prompt for Urdu translation from spec contract"""
        return """You are a technical translator specializing in AI, robotics, and computer science education.
Translate the following English text to Urdu following these rules strictly:

TECHNICAL TERMS:
- Keep in English: ROS2, Python, API, HTTP, JSON, ML, AI, function, class, variable, loop, array
- Translate common words: robot → روبوٹ, computer → کمپیوٹر, network → نیٹ ورک
- Transliterate ambiguous terms: Sensor → سینسر (Sensor), Actuator → ایکچویٹر (Actuator)
- NEVER translate code identifiers (function names, variables, etc.)

FORMATTING:
- Preserve ALL markdown syntax (headings #, bold **, italic _, lists -, links [](url))
- Keep code blocks entirely in English (including comments): ```language ... ```
- Keep inline code in English: `variable_name`
- Keep LaTeX math unchanged: $equation$
- Translate link text but keep URLs: [ترجمہ شدہ متن](https://example.com)
- Translate image alt text but keep src: ![روبوٹ کی تصویر](robot.png)

TONE:
- Use formal educational tone (not conversational)
- Follow standard Urdu grammar rules
- Use proper Urdu punctuation (،؟ instead of ,?)
- Do not mix English and Urdu in same sentence except for technical terms listed above

Translate now:"""

    def translate_to_english(self, urdu_text: str, ttl: int = 3600) -> str:
        """Translate Urdu text back to English with caching"""
        # Create cache key
        cache_key = f"ur_to_en_{hash(urdu_text)}"

        # Check if translation is in cache and not expired
        if cache_key in self.translation_cache:
            if time.time() - self.cache_timestamps.get(cache_key, 0) < ttl:
                logger.info("Returning cached translation")
                return self.translation_cache[cache_key]

        # Call OpenRouter API for translation using OpenAI SDK
        try:
            system_prompt = self._get_english_translation_system_prompt()

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": urdu_text}
                ],
                temperature=0.3,
                max_tokens=8000
            )

            translated_text = response.choices[0].message.content.strip()

            # Cache the translation
            self.translation_cache[cache_key] = translated_text
            self.cache_timestamps[cache_key] = time.time()

            logger.info(f"Translated text to English (length: {len(translated_text)} chars)")
            return translated_text

        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            # Return a professional fallback response
            return f"Translation unavailable: {urdu_text[:100]}..."

    def _get_english_translation_system_prompt(self) -> str:
        """Get the system prompt for English translation"""
        return """You are a technical translator specializing in AI, robotics, and computer science education.
Translate the following Urdu text to English with precision and accuracy.

TRANSLATION REQUIREMENTS:
- Maintain technical accuracy for robotics/AI terminology
- Preserve the original meaning and context
- Apply appropriate formality level for educational content
- Ensure readability and flow in English
- Keep technical terms (ROS2, Python, API, etc.) in English
- Preserve markdown formatting and code blocks
- Do not add any commentary or explanations

Translate now:"""

    def clear_cache(self):
        """Clear the translation cache"""
        self.translation_cache.clear()
        self.cache_timestamps.clear()
        logger.info("Translation cache cleared")
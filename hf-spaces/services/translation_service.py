import google.generativeai as genai
import logging
from typing import Dict
import time

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self, gemini_api_key: str):
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
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

        # Call Gemini API for translation with improved prompt
        try:
            prompt = self._create_urdu_translation_prompt(text)

            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=min(len(text) * 3, 4000),  # Urdu text might be longer
                    temperature=0.2,
                    top_p=0.9,
                )
            )

            translated_text = self._format_translation_response(response.text)

            # Cache the translation
            self.translation_cache[cache_key] = translated_text
            self.cache_timestamps[cache_key] = time.time()

            logger.info(f"Translated text to Urdu (length: {len(translated_text)} chars)")
            return translated_text

        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            # Return a professional fallback response
            return f"Translation unavailable: {text[:100]}..."

    def _create_urdu_translation_prompt(self, text: str) -> str:
        """Create a professional Urdu translation prompt"""
        return f"""You are an elite professional translator specializing in technical and educational content. Translate the provided English text to Urdu with precision and cultural sensitivity.

TRANSLATION REQUIREMENTS:
• Maintain technical accuracy for robotics/AI terminology
• Use proper Urdu script and correct grammar
• Preserve the original meaning and context
• Apply appropriate formality level for educational content
• Ensure readability and flow in Urdu
• Do not add any commentary or explanations

SOURCE TEXT:
"{text}"

URDU TRANSLATION:"""

    def _format_translation_response(self, response_text: str) -> str:
        """Format the translation response for consistency"""
        # Clean up response
        formatted = response_text.strip()

        # Remove any unwanted prefixes or explanations
        if 'TRANSLATION:' in formatted:
            formatted = formatted.split('TRANSLATION:')[-1].strip()
        elif 'TRANSLATED TEXT:' in formatted:
            formatted = formatted.split('TRANSLATED TEXT:')[-1].strip()

        # Clean up extra whitespace
        formatted = ' '.join(formatted.split())

        return formatted

    def translate_to_english(self, urdu_text: str, ttl: int = 3600) -> str:
        """Translate Urdu text back to English with caching"""
        # Create cache key
        cache_key = f"ur_to_en_{hash(urdu_text)}"

        # Check if translation is in cache and not expired
        if cache_key in self.translation_cache:
            if time.time() - self.cache_timestamps.get(cache_key, 0) < ttl:
                logger.info("Returning cached translation")
                return self.translation_cache[cache_key]

        # Call Gemini API for translation with improved prompt
        try:
            prompt = self._create_english_translation_prompt(urdu_text)

            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=min(len(urdu_text) * 2, 4000),
                    temperature=0.2,
                    top_p=0.9,
                )
            )

            translated_text = self._format_translation_response(response.text)

            # Cache the translation
            self.translation_cache[cache_key] = translated_text
            self.cache_timestamps[cache_key] = time.time()

            logger.info(f"Translated text to English (length: {len(translated_text)} chars)")
            return translated_text

        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            # Return a professional fallback response
            return f"Translation unavailable: {urdu_text[:100]}..."

    def _create_english_translation_prompt(self, urdu_text: str) -> str:
        """Create a professional English translation prompt"""
        return f"""You are an elite professional translator specializing in technical and educational content. Translate the provided Urdu text to English with precision and accuracy.

TRANSLATION REQUIREMENTS:
• Maintain technical accuracy for robotics/AI terminology
• Preserve the original meaning and context
• Apply appropriate formality level for educational content
• Ensure readability and flow in English
• Do not add any commentary or explanations

SOURCE TEXT:
"{urdu_text}"

ENGLISH TRANSLATION:"""

    def clear_cache(self):
        """Clear the translation cache"""
        self.translation_cache.clear()
        self.cache_timestamps.clear()
        logger.info("Translation cache cleared")
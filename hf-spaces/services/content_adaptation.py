from typing import Dict, Any, Optional
import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

class ContentAdaptationService:
    def __init__(self, gemini_api_key: str):
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def adapt_content(self, content: str, user_background: str, experience_level: str, chapter_id: str) -> str:
        """Adapt content based on user background and experience level"""
        try:
            # Determine adaptation instructions based on user profile
            adaptation_instructions = self._get_adaptation_instructions(user_background, experience_level, chapter_id)

            # Call Gemini API to adapt the content
            prompt = f"""You are an educational content adapter for a Physical AI & Humanoid Robotics textbook. Adapt the provided content according to these instructions: {adaptation_instructions}. Maintain the core educational value while making it appropriate for the target audience.

Original content:
{content}

Adapted content:"""

            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=len(content) * 2,
                    temperature=0.4,
                )
            )

            adapted_content = response.text

            logger.info(f"Adapted content for background: {user_background}, level: {experience_level}")
            return adapted_content

        except Exception as e:
            logger.error(f"Error adapting content: {str(e)}")
            # Return original content if adaptation fails
            return content

    def _get_adaptation_instructions(self, user_background: str, experience_level: str, chapter_id: str) -> str:
        """Generate adaptation instructions based on user profile"""
        instructions = []

        # Add background-specific instructions
        if user_background and 'software' in user_background.lower():
            instructions.append("Include more code examples and programming concepts")
        elif user_background and 'hardware' in user_background.lower():
            instructions.append("Include more hardware specifications and physical implementations")
        else:
            instructions.append("Provide balanced content with both software and hardware aspects")

        # Add experience level-specific instructions
        if experience_level == 'beginner':
            instructions.append("Use simpler explanations, more examples, and step-by-step instructions")
        elif experience_level == 'intermediate':
            instructions.append("Provide moderate complexity with practical applications")
        elif experience_level == 'advanced':
            instructions.append("Include complex examples, optimization techniques, and advanced concepts")
        else:
            instructions.append("Use moderate complexity appropriate for mixed experience levels")

        # Add chapter-specific instructions if needed
        if 'ros2' in chapter_id.lower():
            instructions.append("Focus on ROS 2 concepts like nodes, topics, and URDF")
        elif 'gazebo' in chapter_id.lower() or 'unity' in chapter_id.lower():
            instructions.append("Emphasize simulation concepts, sensors, and environment modeling")
        elif 'nvidia' in chapter_id.lower() or 'isaac' in chapter_id.lower():
            instructions.append("Highlight perception, VSLAM, navigation, and Isaac-specific concepts")
        elif 'vla' in chapter_id.lower():
            instructions.append("Focus on voice, cognitive, and capstone project concepts")

        return "; ".join(instructions)

    def adapt_examples(self, examples: list, user_background: str, experience_level: str) -> list:
        """Adapt code or practical examples based on user profile"""
        try:
            adapted_examples = []
            for example in examples:
                prompt = f"""You are adapting educational examples for a Physical AI & Humanoid Robotics textbook. Adapt this example for a user with {user_background} background and {experience_level} experience level. Return the adapted example.

Original example:
{example}

Adapted example:"""

                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=1000,
                        temperature=0.3,
                    )
                )

                adapted_examples.append(response.text)

            logger.info(f"Adapted {len(examples)} examples for background: {user_background}, level: {experience_level}")
            return adapted_examples

        except Exception as e:
            logger.error(f"Error adapting examples: {str(e)}")
            return examples  # Return original examples if adaptation fails
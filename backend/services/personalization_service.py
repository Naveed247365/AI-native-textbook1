from typing import Dict, Any, Optional
from .content_adaptation import ContentAdaptationService
import logging

logger = logging.getLogger(__name__)

class PersonalizationService:
    def __init__(self, content_adaptation_service: ContentAdaptationService):
        self.content_adaptation_service = content_adaptation_service

    def get_personalized_content(self, content: str, user_profile: Dict[str, Any], chapter_id: str) -> str:
        """Get personalized content based on user profile"""
        try:
            # Determine the user's background and experience level
            software_background = user_profile.get('software_background', '')
            hardware_background = user_profile.get('hardware_background', '')
            experience_level = user_profile.get('experience_level', 'beginner')

            # Adapt content based on user profile
            adapted_content = self.content_adaptation_service.adapt_content(
                content=content,
                user_background=software_background or hardware_background,
                experience_level=experience_level,
                chapter_id=chapter_id
            )

            logger.info(f"Personalized content for user with background: {software_background}/{hardware_background}, level: {experience_level}")
            return adapted_content

        except Exception as e:
            logger.error(f"Error in personalization: {str(e)}")
            # Return original content if personalization fails
            return content

    def get_user_recommendations(self, user_profile: Dict[str, Any], current_chapter: str) -> Dict[str, Any]:
        """Get personalized recommendations for the user"""
        try:
            software_background = user_profile.get('software_background', '')
            hardware_background = user_profile.get('hardware_background', '')
            experience_level = user_profile.get('experience_level', 'beginner')

            recommendations = {
                'next_chapters': self._get_next_chapters(user_profile, current_chapter),
                'difficulty_level': experience_level,
                'focus_areas': self._get_focus_areas(software_background, hardware_background),
                'additional_resources': self._get_resources(experience_level)
            }

            logger.info(f"Generated recommendations for user")
            return recommendations

        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return {}

    def _get_next_chapters(self, user_profile: Dict[str, Any], current_chapter: str) -> list:
        """Determine next chapters based on user profile and current progress"""
        # This would be more sophisticated in a real implementation
        # For now, return a default sequence
        chapter_sequence = {
            '1-ros2': ['2-gazebo-unity', '3-nvidia-isaac'],
            '2-gazebo-unity': ['3-nvidia-isaac', '4-vla'],
            '3-nvidia-isaac': ['4-vla', 'capstone'],
            '4-vla': ['capstone'],
            'capstone': []
        }

        return chapter_sequence.get(current_chapter, [])

    def _get_focus_areas(self, software_background: str, hardware_background: str) -> list:
        """Determine focus areas based on user background"""
        focus_areas = []

        if software_background and 'software' in software_background.lower():
            focus_areas.append('code examples')
            focus_areas.append('programming concepts')
        elif hardware_background and 'hardware' in hardware_background.lower():
            focus_areas.append('hardware specifications')
            focus_areas.append('physical implementations')

        if not focus_areas:
            focus_areas.append('general concepts')

        return focus_areas

    def _get_resources(self, experience_level: str) -> list:
        """Get additional resources based on experience level"""
        if experience_level == 'beginner':
            return ['tutorials', 'basic examples', 'step-by-step guides']
        elif experience_level == 'intermediate':
            return ['advanced examples', 'practical applications']
        elif experience_level == 'advanced':
            return ['research papers', 'cutting-edge implementations', 'optimization techniques']
        else:
            return ['tutorials', 'examples']
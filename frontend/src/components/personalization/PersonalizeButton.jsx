import React, { useState, useEffect } from 'react';

const PersonalizeButton = ({ chapterId, content, onContentChange }) => {
  const [isPersonalized, setIsPersonalized] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [userProfile, setUserProfile] = useState(null);

  // Check if user is authenticated and get their profile
  useEffect(() => {
    const token = localStorage.getItem('user_token');
    if (token) {
      fetchUserProfile();
    }
  }, []);

  const fetchUserProfile = async () => {
    try {
      const response = await fetch('/api/auth/profile', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('user_token')}`
        }
      });

      if (response.ok) {
        const profile = await response.json();
        setUserProfile(profile);
      }
    } catch (error) {
      console.error('Error fetching user profile:', error);
    }
  };

  const handlePersonalize = async () => {
    if (!userProfile) {
      alert('Please log in to use personalization features.');
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch('/api/personalization/adapt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('user_token')}`
        },
        body: JSON.stringify({
          content: content,
          user_profile: userProfile,
          chapter_id: chapterId
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Update the content with personalized version
      if (onContentChange) {
        onContentChange(data.personalized_content);
      }

      setIsPersonalized(true);
      alert('Content has been personalized based on your background!');
    } catch (error) {
      console.error('Error personalizing content:', error);
      alert('Failed to personalize content. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    // Reset to original content
    if (onContentChange) {
      onContentChange(content);
    }
    setIsPersonalized(false);
  };

  return (
    <div className="personalize-container">
      {userProfile ? (
        <div className="personalize-controls">
          <button
            onClick={isPersonalized ? handleReset : handlePersonalize}
            disabled={isLoading}
            className={`personalize-button ${isPersonalized ? 'reset' : 'personalize'}`}
          >
            {isLoading ? (
              'Processing...'
            ) : isPersonalized ? (
              'Reset to Original'
            ) : (
              'Personalize Content'
            )}
          </button>
          <div className="user-profile-info">
            <small>
              Based on: {userProfile.software_background || userProfile.hardware_background || 'General'}
              ({userProfile.experience_level || 'Unknown'} level)
            </small>
          </div>
        </div>
      ) : (
        <div className="personalize-prompt">
          <p>
            <small>
              <a href="#" onClick={(e) => {
                e.preventDefault();
                alert('Please log in to access personalization features.');
              }}>
                Log in to personalize content
              </a> based on your background
            </small>
          </p>
        </div>
      )}
    </div>
  );
};

export default PersonalizeButton;
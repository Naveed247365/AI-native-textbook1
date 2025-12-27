/**
 * FeedbackButton Component
 *
 * Purpose: Allow users to report translation quality issues
 * Visibility: Only shown when viewing Urdu translation (isUrdu === true)
 */

import React, { useState } from 'react';
import styles from './UrduTranslationButton.module.css';

const FeedbackButton = ({ translationId, onFeedbackSubmit }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [issueDescription, setIssueDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null); // 'success' | 'error' | null

  const handleOpenModal = () => {
    setIsModalOpen(true);
    setSubmitStatus(null);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setIssueDescription('');
    setSubmitStatus(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (issueDescription.trim().length < 10) {
      alert('Please provide at least 10 characters describing the issue.');
      return;
    }

    setIsSubmitting(true);
    setSubmitStatus(null);

    try {
      // Get auth token from localStorage
      const authToken = localStorage.getItem('authToken');

      if (!authToken) {
        throw new Error('Authentication required. Please login.');
      }

      // Call feedback API
      const response = await fetch('/api/translate/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify({
          translation_id: translationId,
          issue_description: issueDescription.trim()
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to submit feedback');
      }

      const data = await response.json();
      console.log('✅ Feedback submitted:', data);

      setSubmitStatus('success');
      setIssueDescription('');

      // Notify parent component
      if (onFeedbackSubmit) {
        onFeedbackSubmit(data);
      }

      // Auto-close after 2 seconds
      setTimeout(() => {
        handleCloseModal();
      }, 2000);

    } catch (error) {
      console.error('❌ Feedback submission failed:', error);
      setSubmitStatus('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      {/* Feedback Button */}
      <button
        className={`${styles['translation-button']} ${styles['feedback-button']}`}
        onClick={handleOpenModal}
        title="Report translation quality issue"
      >
        <span className={styles['button-icon']}>⚠️</span>
        Report Issue
      </button>

      {/* Feedback Modal */}
      {isModalOpen && (
        <div className={styles['modal-overlay']} onClick={handleCloseModal}>
          <div className={styles['modal-content']} onClick={(e) => e.stopPropagation()}>
            <div className={styles['modal-header']}>
              <h3>Report Translation Issue</h3>
              <button
                className={styles['modal-close']}
                onClick={handleCloseModal}
                aria-label="Close modal"
              >
                ×
              </button>
            </div>

            <form onSubmit={handleSubmit} className={styles['feedback-form']}>
              <label htmlFor="issue-description" className={styles['form-label']}>
                Describe the issue (e.g., "Technical term incorrectly translated"):
              </label>
              <textarea
                id="issue-description"
                className={styles['form-textarea']}
                value={issueDescription}
                onChange={(e) => setIssueDescription(e.target.value)}
                placeholder="Example: The term 'ROS2' was translated to Urdu, but it should remain in English as per technical guidelines."
                rows={6}
                minLength={10}
                maxLength={2000}
                required
                disabled={isSubmitting || submitStatus === 'success'}
              />
              <p className={styles['char-count']}>
                {issueDescription.length} / 2000 characters
              </p>

              {/* Success Message */}
              {submitStatus === 'success' && (
                <div className={styles['success-message']}>
                  ✅ Thank you! Your feedback has been submitted successfully.
                </div>
              )}

              {/* Error Message */}
              {submitStatus === 'error' && (
                <div className={styles['error-message']}>
                  ❌ Failed to submit feedback. Please try again.
                </div>
              )}

              {/* Submit Button */}
              <div className={styles['modal-actions']}>
                <button
                  type="button"
                  className={`${styles['modal-button']} ${styles['button-secondary']}`}
                  onClick={handleCloseModal}
                  disabled={isSubmitting}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className={`${styles['modal-button']} ${styles['button-primary']}`}
                  disabled={isSubmitting || submitStatus === 'success'}
                >
                  {isSubmitting ? 'Submitting...' : 'Submit Feedback'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
};

export default FeedbackButton;

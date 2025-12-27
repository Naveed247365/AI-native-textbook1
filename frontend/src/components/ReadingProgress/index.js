import React, { useState, useEffect } from 'react';
import './styles.css';

export default function ReadingProgress() {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const updateProgress = () => {
      // Request animation frame for smooth updates (<50ms latency)
      requestAnimationFrame(() => {
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;
        const scrollTop = window.scrollY;

        // Calculate progress percentage
        const scrollableHeight = documentHeight - windowHeight;
        const scrolled = (scrollTop / scrollableHeight) * 100;

        setProgress(Math.min(100, Math.max(0, scrolled)));
      });
    };

    // Update on scroll with debouncing via RAF
    window.addEventListener('scroll', updateProgress);

    // Initial calculation
    updateProgress();

    return () => window.removeEventListener('scroll', updateProgress);
  }, []);

  return (
    <div className="reading-progress-container">
      <div
        className="reading-progress-bar"
        style={{ width: `${progress}%` }}
        role="progressbar"
        aria-valuenow={Math.round(progress)}
        aria-valuemin="0"
        aria-valuemax="100"
        aria-label="Reading progress"
      />
    </div>
  );
}

import React from 'react';
import Link from '@docusaurus/Link';
import { useDoc } from '@docusaurus/theme-common/internal';
import './styles.css';

export default function ChapterNavigation() {
  const { metadata } = useDoc();
  const { previous, next } = metadata;

  // Don't render if no previous or next chapters
  if (!previous && !next) {
    return null;
  }

  return (
    <nav className="chapter-navigation" aria-label="Chapter navigation">
      <div className="chapter-nav-container">
        {previous && (
          <Link
            to={previous.permalink}
            className="chapter-nav-link chapter-nav-prev"
          >
            <span className="chapter-nav-arrow">←</span>
            <div className="chapter-nav-content">
              <span className="chapter-nav-label">Previous</span>
              <span className="chapter-nav-title">{previous.title}</span>
            </div>
          </Link>
        )}
        {next && (
          <Link
            to={next.permalink}
            className="chapter-nav-link chapter-nav-next"
          >
            <div className="chapter-nav-content">
              <span className="chapter-nav-label">Next</span>
              <span className="chapter-nav-title">{next.title}</span>
            </div>
            <span className="chapter-nav-arrow">→</span>
          </Link>
        )}
      </div>
    </nav>
  );
}

import React, { useState, useEffect } from 'react';
import Content from '@theme-original/DocItem/Content';
import PersonalizeButton from '@site/src/components/personalization/PersonalizeButton';
import UrduTranslationButton from '@site/src/components/translation/UrduTranslationButton';
import ReadingProgress from '@site/src/components/ReadingProgress';
import ChapterNavigation from '@site/src/components/ChapterNavigation';
import { useDoc } from '@docusaurus/plugin-content-docs/client';

export default function ContentWrapper(props) {
  const { frontMatter, metadata } = useDoc();
  const chapterId = frontMatter.chapter_id || metadata.id;
  const [translatedContent, setTranslatedContent] = useState(null);
  const [isUrdu, setIsUrdu] = useState(false);

  // Listen for translation events
  useEffect(() => {
    const handleTranslationChange = (event) => {
      console.log('Translation event received:', event.detail);
      setTranslatedContent(event.detail.content);
      setIsUrdu(event.detail.isUrdu);
    };

    window.addEventListener('translationChanged', handleTranslationChange);
    return () => window.removeEventListener('translationChanged', handleTranslationChange);
  }, []);

  return (
    <>
      {/* Reading progress bar at top */}
      <ReadingProgress />

      {/* Inject PersonalizeButton and UrduTranslationButton at the top of chapter content */}
      {chapterId && (
        <div style={{ marginBottom: '2rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <PersonalizeButton chapterId={chapterId} />
          <UrduTranslationButton chapterId={chapterId} />
        </div>
      )}

      {/* Show translated content if available */}
      {isUrdu && translatedContent ? (
        <div style={{
          direction: 'rtl',
          textAlign: 'right',
          fontFamily: "'Jameel Noori Nastaleeq', 'Noto Nastaliq Urdu', serif",
          lineHeight: '2',
          fontSize: '1.1rem',
          whiteSpace: 'pre-wrap',
          padding: '1rem',
          backgroundColor: '#f9fafb',
          borderRadius: '8px',
          border: '1px solid #e5e7eb'
        }}>
          {translatedContent}
        </div>
      ) : (
        <Content {...props} />
      )}

      {/* Chapter navigation at bottom */}
      <ChapterNavigation />
    </>
  );
}

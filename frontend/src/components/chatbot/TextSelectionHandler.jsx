import { useEffect, useState, useCallback } from 'react';

const TextSelectionHandler = ({ children }) => {
  const [selectedText, setSelectedText] = useState('');

  const handleSelection = useCallback(() => {
    // Use a small timeout to ensure the selection is complete
    setTimeout(() => {
      const selection = window.getSelection();
      const text = selection.toString().trim();

      if (text && text.length > 0) {
        // Validate the selected text
        if (text.length > 5000) {
          alert(`Selected text is too long (${text.length} characters). Please select less than 5000 characters.`);
          return;
        }

        setSelectedText(text);
      }
    }, 0);
  }, []);

  useEffect(() => {
    // Add event listeners for text selection
    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    // Cleanup event listeners
    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, [handleSelection]);

  const clearSelection = () => {
    window.getSelection().removeAllRanges();
    setSelectedText('');
  };

  return (
    <>
      {children({ selectedText, clearSelection })}
    </>
  );
};

export default TextSelectionHandler;
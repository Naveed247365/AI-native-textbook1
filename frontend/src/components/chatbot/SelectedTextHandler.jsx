import { useEffect, useState } from 'react';

const SelectedTextHandler = ({ onTextSelected }) => {
  const [selectedText, setSelectedText] = useState('');

  useEffect(() => {
    const handleSelection = () => {
      // Use a small timeout to ensure the selection is complete
      setTimeout(() => {
        const selection = window.getSelection();
        const text = selection.toString().trim();

        if (text) {
          setSelectedText(text);
          // Notify parent component about the selected text
          if (onTextSelected) {
            onTextSelected(text);
          }
        }
      }, 0);
    };

    // Add event listeners for text selection
    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    // Cleanup event listeners
    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, [onTextSelected]);

  const validateSelectedText = (text) => {
    // Check if text is not empty and not too long (per requirement TC-002)
    if (!text) return false;
    if (text.length > 5000) {
      alert(`Selected text is too long (${text.length} characters). Please select less than 5000 characters.`);
      return false;
    }
    return true;
  };

  const getSelectedText = () => {
    const selection = window.getSelection();
    const text = selection.toString().trim();

    if (validateSelectedText(text)) {
      return text;
    }
    return '';
  };

  const clearSelection = () => {
    window.getSelection().removeAllRanges();
    setSelectedText('');
    if (onTextSelected) {
      onTextSelected('');
    }
  };

  return (
    <div style={{ display: 'none' }}>
      {/* This component runs in the background to handle text selection */}
      {/* It doesn't render any visible UI but provides text selection functionality */}
    </div>
  );
};

export default SelectedTextHandler;
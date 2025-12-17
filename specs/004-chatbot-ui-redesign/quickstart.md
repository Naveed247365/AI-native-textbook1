# Quickstart Guide: Premium AI Chatbot UI Redesign

## Overview
This guide provides a quick path to implement the redesigned Premium AI Chatbot UI with futuristic AI/robotics design, smooth animations, and enhanced functionality.

## Prerequisites
- Node.js 18+ installed
- Docusaurus project set up (existing project)
- Access to OpenRouter API key for backend
- Qdrant vector database configured

## Installation Steps

### 1. Update Chatbot Component
Replace the existing EnhancedChatbot.jsx with the redesigned version:

```bash
# Navigate to the components directory
cd frontend/src/components/chatbot/

# The EnhancedChatbot.jsx file will be updated with the new design
# (Implementation details covered in the next sections)
```

### 2. Add New Stylesheet
Create the new CSS file with futuristic design:

```bash
# Create the new stylesheet
touch EnhancedChatbot.css
```

## Implementation Steps

### 1. Core Functionality Update
Update EnhancedChatbot.jsx with proper state management:

```javascript
// EnhancedChatbot.jsx
import React, { useState, useEffect, useRef } from 'react';
import './EnhancedChatbot.css'; // New stylesheet

const EnhancedChatbot = ({ selectedText = '', onTextSelected }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentSelectedText, setCurrentSelectedText] = useState(selectedText);
  const [animationState, setAnimationState] = useState('idle');
  const chatbotRef = useRef(null);
  const inputRef = useRef(null);

  // Enhanced close functionality
  useEffect(() => {
    const handleEscKey = (e) => {
      if (e.key === 'Escape' && isOpen) {
        handleClose();
      }
    };

    const handleOutsideClick = (e) => {
      if (chatbotRef.current && !chatbotRef.current.contains(e.target) && isOpen) {
        handleClose();
      }
    };

    document.addEventListener('keydown', handleEscKey);
    document.addEventListener('mousedown', handleOutsideClick);

    return () => {
      document.removeEventListener('keydown', handleEscKey);
      document.removeEventListener('mousedown', handleOutsideClick);
    };
  }, [isOpen]);

  // Handle selected text updates
  useEffect(() => {
    if (selectedText && selectedText.trim() !== '') {
      setCurrentSelectedText(selectedText);
      setInputValue(`Selected text:\n"${selectedText}"\n\nAsk a question about this text...`);

      setTimeout(() => {
        if (inputRef.current) {
          inputRef.current.focus();
          inputRef.current.setSelectionRange(inputValue.length, inputValue.length);
        }
      }, 100);
    }
  }, [selectedText]);

  const handleClose = () => {
    setAnimationState('closing');
    setTimeout(() => {
      setIsOpen(false);
      setAnimationState('idle');
      setMessages([]);
      setInputValue('');
    }, 200); // Match CSS animation duration
  };

  // ... rest of component implementation
};
```

### 2. Create Futuristic Stylesheet
Create EnhancedChatbot.css with the new design:

```css
/* EnhancedChatbot.css */

/* Floating Chatbot Container */
.chatbot-popup {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 480px;
  max-width: calc(100vw - 40px);
  height: 600px;
  max-height: 70vh;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  background: rgba(11, 15, 25, 0.9); /* #0B0F19 with transparency */
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow:
    0 4px 20px rgba(0, 0, 0, 0.15),
    0 0 20px rgba(0, 255, 255, 0.1); /* Neon glow effect */
  border: 1px solid rgba(0, 255, 255, 0.2);
  overflow: hidden;
  animation: slideIn 0.2s ease-in-out;
}

/* Animation for opening/closing */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes slideOut {
  from {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
  to {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }
}

.chatbot-popup.closing {
  animation: slideOut 0.2s ease-in-out forwards;
}

/* Header with futuristic design */
.chatbot-header {
  padding: 20px;
  background: rgba(26, 31, 46, 0.8); /* #1A1F2E with transparency */
  border-bottom: 1px solid rgba(0, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chatbot-title h3 {
  margin: 0;
  color: #FFFFFF;
  font-family: 'Inter', sans-serif;
  font-size: 16px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 10px;
}

.chatbot-title h3::before {
  content: "🤖";
  display: inline-block;
}

.close-button {
  background: transparent;
  border: none;
  color: #B0B0B0;
  font-size: 24px;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-button:hover {
  background: rgba(0, 255, 255, 0.1);
  color: #00FFFF;
  transform: scale(1.1);
}

/* Messages container with futuristic styling */
.chatbot-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: rgba(11, 15, 25, 0.5);
}

.message {
  max-width: 85%;
  padding: 14px 18px;
  border-radius: 18px;
  animation: fadeIn 0.2s ease-out;
  line-height: 1.5;
  position: relative;
}

.message::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(0, 206, 209, 0.05));
  z-index: -1;
}

.user-message {
  align-self: flex-end;
  background: linear-gradient(135deg, #00FFFF, #00CED1);
  color: #0B0F19;
  border-bottom-right-radius: 4px;
}

.bot-message {
  align-self: flex-start;
  background: rgba(26, 31, 46, 0.8);
  color: #FFFFFF;
  border: 1px solid rgba(0, 255, 255, 0.1);
  border-bottom-left-radius: 4px;
}

/* Input area with futuristic design */
.chatbot-input-area {
  padding: 20px;
  background: rgba(26, 31, 46, 0.8);
  border-top: 1px solid rgba(0, 255, 255, 0.1);
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.chatbot-input {
  flex: 1;
  padding: 14px 18px;
  border: 2px solid rgba(0, 255, 255, 0.2);
  border-radius: 18px;
  resize: none;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  line-height: 1.4;
  outline: none;
  transition: all 0.2s ease;
  max-height: 120px;
  min-height: 46px;
  background: rgba(11, 15, 25, 0.5);
  color: #FFFFFF;
  backdrop-filter: blur(4px);
}

.chatbot-input:focus {
  border-color: #00FFFF;
  box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.2);
}

.send-button {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #00FFFF, #00CED1);
  color: #0B0F19;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  transition: all 0.2s ease;
  box-shadow: 0 4px 15px rgba(0, 255, 255, 0.3);
}

.send-button:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(0, 255, 255, 0.4);
}

.send-button:disabled {
  background: #495057;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Floating effect */
.chatbot-popup:hover {
  box-shadow:
    0 6px 25px rgba(0, 0, 0, 0.2),
    0 0 30px rgba(0, 255, 255, 0.2); /* Enhanced glow on hover */
  transform: translateY(-2px);
}

/* Responsive design */
@media (max-width: 768px) {
  .chatbot-popup {
    width: calc(100vw - 40px);
    height: 70vh;
    bottom: 20px;
    right: 20px;
    left: 20px;
    border-radius: 16px;
  }

  .message {
    max-width: 90%;
  }
}

@media (max-width: 480px) {
  .chatbot-popup {
    width: calc(100vw - 32px);
    height: 60vh;
    bottom: 16px;
    right: 16px;
    left: 16px;
    border-radius: 12px;
  }

  .chatbot-header,
  .chatbot-input-area {
    padding: 16px;
  }
}
```

### 3. Update Text Selection Handler
Ensure proper integration with the existing TextSelectionHandler:

```javascript
// TextSelectionHandler.jsx (enhanced)
const TextSelectionHandler = ({ children }) => {
  // Existing functionality with additional close handling
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
```

## Testing the Implementation

### 1. Basic Functionality Test
1. Select text in the textbook content
2. Verify chatbot appears near selection with proper styling
3. Check that selected text appears in input field
4. Test close functionality (× button, outside click, ESC key)

### 2. Visual Design Verification
1. Confirm futuristic AI/robotics theme is applied
2. Verify dark glassmorphism effect
3. Check neon accents and proper color scheme
4. Test responsive design on different screen sizes

### 3. Animation Quality
1. Verify smooth fade-in/out animations (200ms)
2. Check scale transformations (0.9 to 1.0)
3. Confirm animations maintain 60fps performance

## Integration with Backend

The redesigned UI maintains full compatibility with existing backend API:

```javascript
// API integration remains unchanged
fetch('http://localhost:8001/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: questionText,           // User's question
    selected_text: selectedText,     // Selected text context
    user_id: localStorage.getItem('user_id') || null
  }),
});
```

## Accessibility Features

1. **Keyboard Navigation**: Full ESC key and Tab navigation support
2. **Focus Indicators**: 2px solid #00FFFF focus rings
3. **ARIA Labels**: Proper semantic markup
4. **Contrast Ratios**: Meet WCAG 2.1 AA standards

## Performance Optimization

1. **Hardware Acceleration**: Use CSS transforms and opacity for animations
2. **Contain Property**: Optimize rendering with CSS containment
3. **Virtual Scrolling**: For large message histories (future enhancement)

## Troubleshooting

### Common Issues:
- **Blurry text**: Ensure proper font rendering settings
- **Animation jank**: Check for layout thrashing in React components
- **Close button not working**: Verify event listeners are properly attached
- **Mobile responsiveness**: Check viewport meta tag in HTML

### Browser Compatibility:
- Chrome 90+, Firefox 75+, Safari 14+, Edge 90+
- Fallbacks provided for backdrop-filter support

## Next Steps

1. Deploy the updated UI to staging environment
2. Conduct user acceptance testing
3. Monitor performance metrics
4. Iterate based on user feedback
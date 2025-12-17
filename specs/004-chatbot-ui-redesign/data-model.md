# Data Model: Premium AI Chatbot UI Redesign

## 1. Component State Model

### 1.1 EnhancedChatbot State Properties
```javascript
{
  isOpen: boolean,                    // Controls visibility of chatbot popup
  messages: Array<Message>,           // Conversation history
  inputValue: string,                 // Current input field value
  isLoading: boolean,                 // Loading state for API requests
  currentSelectedText: string,        // Currently selected text from content
  animationState: "idle" | "opening" | "closing",  // Animation state for transitions
  position: {                         // Position coordinates (for positioning near selection)
    x: number,
    y: number
  }
}
```

### 1.2 Message Entity
```javascript
{
  id: string | number,                // Unique identifier for the message
  text: string,                       // Message content
  sender: "user" | "bot",             // Message sender type
  timestamp: Date,                    // When the message was created
  status: "sent" | "delivered" | "read" | "error"  // Message delivery status (optional)
}
```

## 2. UI Configuration Model

### 2.1 Theme Configuration
```javascript
{
  colors: {
    primaryBackground: "#0B0F19",     // Dark background
    secondaryBackground: "#1A1F2E",   // Secondary dark background
    accentNeonBlue: "#00FFFF",        // Neon blue accent
    accentCyan: "#00CED1",            // Cyan accent
    textPrimary: "#FFFFFF",           // Primary text
    textSecondary: "#B0B0B0"          // Secondary text
  },
  typography: {
    fontFamily: "Inter",              // Primary font family
    fontSize: {
      heading: "16px",                // Heading font size
      body: "14px"                    // Body font size
    },
    lineHeight: {
      heading: 1.5,                   // Heading line height
      body: 1.4                       // Body line height
    }
  },
  spacing: [4, 8, 12, 16, 24, 32, 40], // Spacing scale in pixels
  shadows: {
    level1: "0 1px 3px rgba(0,0,0,0.12)",  // Light shadow
    level2: "0 4px 20px rgba(0,0,0,0.15)"  // Medium shadow
  }
}
```

### 2.2 Animation Configuration
```javascript
{
  durations: {
    fadeIn: 200,                      // Fade in duration in ms
    fadeOut: 200,                     // Fade out duration in ms
    scaleIn: 200,                     // Scale in duration in ms
    scaleOut: 200                     // Scale out duration in ms
  },
  easings: {
    inOut: "ease-in-out",             // Standard easing
    in: "ease-in",                    // Ease in
    out: "ease-out"                   // Ease out
  },
  transforms: {
    scaleFrom: 0.9,                   // Starting scale for entrance
    scaleTo: 1.0                      // Ending scale for entrance
  }
}
```

## 3. API Communication Model

### 3.1 Request Payload
```javascript
{
  message: string,                    // User's question/message
  selected_text: string,              // Text selected by the user from content
  user_id?: string                    // Optional user identifier
}
```

### 3.2 Response Payload
```javascript
{
  answer: string                       // AI-generated response
}
```

## 4. Event Model

### 4.1 User Interaction Events
```javascript
{
  type: "text_selection" | "message_send" | "chatbot_close" | "input_change",
  payload: {
    // Based on type:
    // text_selection: { selectedText: string, position: {x, y} }
    // message_send: { message: string, selectedText: string }
    // chatbot_close: { closeMethod: "button" | "outside_click" | "esc_key" }
    // input_change: { newValue: string }
  },
  timestamp: Date
}
```

### 4.2 System Events
```javascript
{
  type: "animation_start" | "animation_end" | "api_request" | "api_response",
  payload: {
    // Based on type:
    // animation_start: { animationType: string, target: string }
    // animation_end: { animationType: string, target: string }
    // api_request: { endpoint: string, payload: object }
    // api_response: { endpoint: string, response: object, status: number }
  },
  timestamp: Date
}
```

## 5. Accessibility Model

### 5.1 ARIA Attributes
```javascript
{
  chatbot: {
    role: "dialog",
    "aria-modal": true,
    "aria-labelledby": "chatbot-title",
    "aria-describedby": "chatbot-description"
  },
  input: {
    role: "textbox",
    "aria-label": "Chat input",
    "aria-multiline": true
  },
  button: {
    role: "button",
    "aria-label": "Close chatbot"  // For close button
  }
}
```

### 5.2 Focus Management
```javascript
{
  focusOrder: [
    "chatbot-header",
    "chat-messages",
    "chat-input",
    "send-button"
  ],
  focusIndicators: {
    width: "2px",
    style: "solid",
    color: "#00FFFF"  // Neon blue focus ring
  }
}
```

## 6. Responsive Design Model

### 6.1 Breakpoint Configuration
```javascript
{
  breakpoints: {
    mobile: {
      maxWidth: 480,
      properties: {
        width: "calc(100vw - 32px)",
        height: "70vh",
        borderRadius: "12px"
      }
    },
    tablet: {
      maxWidth: 768,
      properties: {
        width: "480px",
        height: "60vh",
        borderRadius: "16px"
      }
    },
    desktop: {
      minWidth: 769,
      properties: {
        width: "480px",
        height: "600px",
        borderRadius: "20px"
      }
    }
  }
}
```

## 7. Error Handling Model

### 7.1 Error Types
```javascript
{
  api_errors: {
    type: "api_error",
    code: "REQUEST_FAILED" | "PARSE_ERROR" | "NETWORK_ERROR",
    message: string,
    timestamp: Date
  },
  ui_errors: {
    type: "ui_error",
    code: "ANIMATION_FAILED" | "STATE_MISMATCH" | "INVALID_INPUT",
    message: string,
    timestamp: Date
  }
}
```

### 7.2 Error Recovery
```javascript
{
  retryStrategy: {
    maxRetries: 3,
    backoff: "linear" | "exponential",
    interval: 1000  // ms
  },
  fallbacks: {
    animationFallback: "opacity_only",  // If complex animations fail
    themeFallback: "light_theme"        // If dark theme fails
  }
}
```

## 8. Entity Relationships

### 8.1 Component Hierarchy
```
EnhancedChatbot (Parent)
├── ChatHeader (Child)
│   ├── ChatTitle (Grandchild)
│   └── CloseButton (Grandchild)
├── ChatMessages (Child)
│   └── Message (Grandchild) [multiple]
├── ChatInputArea (Child)
│   ├── TextInput (Grandchild)
│   └── SendButton (Grandchild)
└── AnimationController (Internal)
```

### 8.2 State Flow
```
TextSelectionHandler → EnhancedChatbot.state.currentSelectedText
EnhancedChatbot.state.inputValue → API Request
API Response → EnhancedChatbot.state.messages
EnhancedChatbot.state.isOpen → UI Visibility
EnhancedChatbot.state.animationState → Animation Controller
```

This data model ensures proper state management, accessibility compliance, responsive design, and clear relationships between all components and data flows in the redesigned chatbot UI.
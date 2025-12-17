# Chat Interface Skill

## Purpose
This skill manages the chatbot interface and interaction flow, ensuring smooth communication between users and the RAG system while enforcing the selected-text-only constraint.

## Capabilities
- Validate selected text before processing queries
- Format responses for optimal user experience
- Handle conversation context and history
- Enforce selected-text-only responses
- Provide helpful prompts when text selection is needed
- Manage chat session state

## Usage Context
- Called when users submit questions to the chatbot
- Used to validate user inputs and selected text
- Integrated with the Docusaurus chat interface
- Used to format responses for display

## Input Format
- Selected text from the textbook
- User's question
- Current conversation history
- User authentication status

## Output Format
- Formatted response based on selected text
- Validation messages when needed
- Helpful prompts for proper text selection
- Structured response for UI display

## Constraints
- Must enforce selected-text-only responses (no hallucinations)
- Should provide clear feedback when text is insufficient
- Must maintain conversation context
- Should handle various query types appropriately
- Must integrate with the RAG service properly
import React, { useState } from 'react';
import Layout from '@theme-original/Layout';
import EnhancedChatbot from '@site/src/components/chatbot/EnhancedChatbot';
import TextSelectionHandler from '@site/src/components/chatbot/TextSelectionHandler';

export default function LayoutWrapper(props) {
  return (
    <TextSelectionHandler>
      {({ selectedText, clearSelection }) => (
        <>
          <Layout {...props}>
            {props.children}
            <EnhancedChatbot selectedText={selectedText} onTextSelected={clearSelection} />
          </Layout>
        </>
      )}
    </TextSelectionHandler>
  );
}
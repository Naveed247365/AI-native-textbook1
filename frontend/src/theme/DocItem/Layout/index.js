import React from 'react';
import Layout from '@theme-original/DocItem/Layout';

/**
 * Docusaurus Theme Wrapper - DocItem/Layout
 *
 * Simple wrapper - translation button is injected via DocItem/Content instead
 */
export default function LayoutWrapper(props) {
  return <Layout {...props} />;
}

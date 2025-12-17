// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  // Manual sidebar for the Physical AI & Humanoid Robotics textbook
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      items: ['intro'],
    },
    {
      type: 'category',
      label: 'Modules',
      items: [
        {
          type: 'category',
          label: '1. ROS2',
          items: ['modules/ros2/fundamentals'],
        },
        {
          type: 'category',
          label: '2. Gazebo/Unity',
          items: ['modules/gazebo-unity/intro', 'simulation-environments'],
        },
        {
          type: 'category',
          label: '3. NVIDIA Isaac',
          items: ['modules/nvidia-isaac/intro', 'nvidia-isaac-ecosystem'],
        },
        {
          type: 'category',
          label: '4. VLA',
          items: ['modules/vla/intro', 'vision-language-action-models'],
        },
      ],
    },
    {
      type: 'category',
      label: 'Weekly Plan',
      items: ['weekly-plan'],
    },
    {
      type: 'category',
      label: 'Hardware Specs',
      items: ['hardware-specifications'],
    },
    {
      type: 'category',
      label: 'Capstone Project',
      items: ['capstone-project'],
    },
  ],
};

export default sidebars;

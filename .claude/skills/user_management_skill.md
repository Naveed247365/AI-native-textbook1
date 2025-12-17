# User Management Skill

## Purpose
This skill handles user registration, profile management, and authentication processes, including the collection of background information for personalization.

## Capabilities
- Manage user registration with background questions
- Store and retrieve user profile information
- Handle authentication and session management
- Capture software/hardware background information
- Manage user preferences and settings
- Track learning progress and achievements

## Usage Context
- Called during user registration process
- Used when users update their profiles
- Integrated with the authentication system
- Called when personalization features are accessed
- Used for progress tracking across modules

## Input Format
- User registration information
- Profile update requests
- Authentication credentials
- Background information (software/hardware experience)
- User preferences and settings

## Output Format
- User profile data
- Authentication tokens
- Registration confirmation
- Profile update confirmations
- Progress tracking information

## Constraints
- Must follow data privacy and security requirements
- Should collect all required background information
- Must integrate with Neon Postgres database
- Should support various background types (Software Engineer, Hardware Engineer, Student, etc.)
- Must maintain data consistency and integrity
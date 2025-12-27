# Frontend - Docusaurus Site

Static site generator for the Physical AI & Humanoid Robotics textbook.

## Setup

```bash
npm install
```

## Development

```bash
npm start  # Starts dev server on http://localhost:3000
```

## Build

```bash
npm run build  # Generates static files in build/
npm run serve  # Serves build/ locally
```

## Environment Variables

Create `.env.local` (gitignored):

```env
REACT_APP_API_URL=http://localhost:8001  # Backend URL
```

## Project Structure

- `/docs` - Markdown content (book chapters)
- `/src/components` - React components (chatbot, auth, personalization, translation)
- `/src/theme` - Swizzled Docusaurus components
- `/src/pages` - Custom pages (login, signup, homepage)
- `/src/css` - Custom styles and theme
- `/static` - Static assets (images, fonts)

## Swizzled Components

- `DocItem/Content` - Document page wrapper (buttons integration)
- `DocItem/Layout` - Site layout wrapper
- `Footer` - Custom footer (no Docusaurus branding)
- `Navbar` - Custom navigation
- `TOC` - Enhanced table of contents

## Features

- RAG-powered chatbot
- User authentication (login/signup)
- Content personalization based on user background
- Dynamic Urdu translation
- Reading progress bar
- Estimated reading time
- Chapter navigation (Previous/Next)
- Professional Humanoid Robotics theme

## Deployment

See [DEPLOYMENT.md](../DEPLOYMENT.md) for Vercel deployment instructions.

## Troubleshooting

**Build fails**: Check Node version (must be >=18.0)
```bash
node --version  # Should be v18.x or higher
```

**API calls fail**: Verify `REACT_APP_API_URL` in `.env.local`

**Theme not applying**: Clear cache and rebuild
```bash
rm -rf .docusaurus build node_modules/.cache
npm install
npm start
```

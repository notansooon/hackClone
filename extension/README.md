# PinkVanity Chrome Extension

> Shop by Specs, Not Stereotypes.

Chrome Extension that helps users avoid the Pink Tax and find better-fitting clothes by cross-referencing men's products.

## Features

- **Fair Price Engine**: Automatically finds cheaper men's equivalents for women's personal care products
- **Universal Fit Decoder**: AI-powered size chart reading for clothing recommendations
- **Savings Dashboard**: Track your lifetime savings

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Build the extension
npm run build

# Or watch for changes during development
npm run dev
```

### Load in Chrome

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `extension` folder

## Project Structure

```
extension/
├── manifest.json         # Extension manifest (MV3)
├── popup.html           # Popup UI
├── options.html         # Settings page
├── src/
│   ├── content-script.ts   # Injected into product pages
│   ├── background.ts       # Service worker
│   ├── popup.ts           # Popup logic
│   ├── options.ts         # Settings logic
│   ├── api.ts             # Backend API client
│   ├── scrapers.ts        # Site-specific scrapers
│   ├── overlay.ts         # In-page UI
│   └── types.ts           # TypeScript types
├── styles/
│   ├── overlay.css        # In-page overlay styles
│   ├── popup.css          # Popup styles
│   └── options.css        # Settings page styles
└── icons/                 # Extension icons
```

## Supported Sites

- Target
- Uniqlo
- H&M
- Zara
- American Eagle

## Backend

The extension requires the PinkVanity backend to be running. See `/backend/README.md` for setup instructions.

Default API URL: `http://localhost:8000`

## Development

```bash
# Watch mode - rebuilds on file changes
npm run dev

# One-time build
npm run build
```

After making changes, click the refresh button on `chrome://extensions/` to reload the extension.

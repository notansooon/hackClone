# PinkVanity

> **Shop by Specs, Not Stereotypes.**

A Chrome Extension that fights the **Pink Tax** and solves **Vanity Sizing** by helping users find cheaper, better-fitting alternatives in the men's section.

## The Problem

1. **The Pink Tax**: Women pay 13% more for personal care products and 8% more for clothing compared to identical men's products
2. **Vanity Sizing**: Women's sizes are arbitrary labels while men's sizes use actual measurements

## The Solution

PinkVanity is like *Honey* but for gendered pricing. It automatically:

- **Fair Price Engine**: Finds men's equivalents using ingredient/material similarity (Jaccard Similarity)
- **Universal Fit Decoder**: Uses AI (GPT-4o) to read size charts and calculate the right men's size for your body

## Quick Start

### 1. Start the Backend

```bash
cd backend
pip install -r requirements.txt
python run.py
```

API available at `http://localhost:8000`

### 2. Build the Extension

```bash
cd extension
npm install
npm run build
```

### 3. Load in Chrome

1. Go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" and select the `extension` folder

## Demo Endpoints

For hackathon demos, use these pre-recorded responses:

```bash
# Gillette Venus Razor - 25% savings
curl http://localhost:8000/api/v1/demo/razor

# Skintimate Shave Gel - 50% savings
curl http://localhost:8000/api/v1/demo/shave-gel

# H&M Boyfriend Hoodie - 44% savings with size recommendation
curl http://localhost:8000/api/v1/demo/hoodie
```

## Tech Stack

- **Backend**: Python, FastAPI, OpenAI API (GPT-4o)
- **Extension**: TypeScript, Chrome Manifest V3, esbuild
- **Matching**: Jaccard Similarity on ingredients/materials
- **Sizing**: AI-powered OCR for size chart images

## Project Structure

```
pinkvanity/
├── backend/                 # FastAPI server
│   ├── app/
│   │   ├── main.py         # API routes
│   │   ├── models.py       # Pydantic models
│   │   ├── mock_data.py    # Demo product database
│   │   └── services/
│   │       ├── matching.py # Jaccard similarity engine
│   │       └── sizing.py   # GPT-4o size chart OCR
│   ├── requirements.txt
│   └── run.py
│
└── extension/              # Chrome Extension
    ├── manifest.json
    ├── src/
    │   ├── content-script.ts
    │   ├── background.ts
    │   ├── popup.ts
    │   └── ...
    └── styles/
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/match` | POST | Find men's equivalent for a product |
| `/api/v1/match/quick` | GET | Quick match via query params |
| `/api/v1/clothing/match` | POST | Find clothing match with size |
| `/api/v1/demo/razor` | GET | Demo: Razor comparison |
| `/api/v1/demo/hoodie` | GET | Demo: Hoodie with sizing |

## Golden Examples

| Women's Product | Men's Equivalent | Savings |
|----------------|------------------|---------|
| Gillette Venus ($15.99) | Gillette Fusion5 ($11.99) | 25% |
| Skintimate Shave Gel ($3.99) | Barbasol ($1.99) | 50% |
| H&M Boyfriend Hoodie ($45) | H&M Men's Hoodie ($24.99) | 44% |
| Secret Deodorant ($6.49) | Old Spice ($4.99) | 23% |

## Hackathon Track

**Female Empowerment / Economic Equity**

---

*Built for [Hackathon Name] 2026*

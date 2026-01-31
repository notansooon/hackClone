# PinkVanity Backend API

> Shop by Specs, Not Stereotypes.

FastAPI backend for the PinkVanity Chrome Extension.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run the server
python run.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Key Endpoints

### Pink Tax Matching (Feature A)

```bash
# Find men's equivalent for a women's product
curl -X POST http://localhost:8000/api/v1/match \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Gillette Venus Razor",
    "price": 15.99,
    "category": "personal_care"
  }'

# Quick match via GET
curl "http://localhost:8000/api/v1/match/quick?title=Gillette+Venus&price=15.99"
```

### Universal Fit Decoder (Feature B)

```bash
# Get size recommendation
curl -X POST http://localhost:8000/api/v1/clothing/match \
  -G \
  -d "womens_product_title=H%26M+Women%27s+Boyfriend+Hoodie" \
  -d "waist=28" \
  -d "hip=40" \
  -d "chest=34"
```

### Demo Endpoints (Hackathon)

Pre-recorded responses for reliable demos:

```bash
curl http://localhost:8000/api/v1/demo/razor
curl http://localhost:8000/api/v1/demo/shave-gel
curl http://localhost:8000/api/v1/demo/hoodie
```

## Architecture

```
backend/
├── app/
│   ├── main.py           # FastAPI app & routes
│   ├── models.py         # Pydantic models
│   ├── mock_data.py      # Demo product database
│   └── services/
│       ├── matching.py   # Jaccard similarity engine
│       └── sizing.py     # GPT-4o size chart OCR
├── requirements.txt
├── run.py
└── .env.example
```

## Mock Data

The backend includes "Golden Examples" for demo purposes:

| Women's Product | Men's Equivalent | Savings |
|----------------|------------------|---------|
| Gillette Venus ($15.99) | Gillette Fusion5 ($11.99) | 25% |
| Skintimate Shave Gel ($3.99) | Barbasol ($1.99) | 50% |
| H&M Boyfriend Hoodie ($45) | H&M Men's Hoodie ($24.99) | 44% |

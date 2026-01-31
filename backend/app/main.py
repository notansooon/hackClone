"""
PinkVanity Backend API
Shop by Specs, Not Stereotypes.

FastAPI server providing:
- Pink Tax matching (find men's equivalents for women's products)
- Universal Fit Decoder (AI-powered size chart reading)
- Savings tracking
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .models import (
    ProductMatchRequest, SizeMatchRequest, MatchResponse, SizeResponse,
    SavingsStats, ProductCategory, UserMeasurements
)
from .services.matching import find_mens_equivalent, search_products_by_title, check_first_three_match
from .services.sizing import get_size_recommendation, find_mens_clothing_equivalent
from .mock_data import get_all_womens_products, get_all_mens_products, GOLDEN_PAIRS

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    print("PinkVanity API starting up...")
    print(f"Loaded {len(get_all_womens_products())} women's products")
    print(f"Loaded {len(get_all_mens_products())} men's products")
    print(f"Loaded {len(GOLDEN_PAIRS)} pre-verified pairs")
    yield
    print("PinkVanity API shutting down...")


app = FastAPI(
    title="PinkVanity API",
    description="Backend API for the PinkVanity Chrome Extension - Fight the Pink Tax with AI",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "chrome-extension://*",  # Chrome extensions
        "http://localhost:*",     # Local development
        "http://127.0.0.1:*",
        "*"  # For hackathon demo - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Health Check
# =============================================================================

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "PinkVanity API",
        "version": "1.0.0",
        "tagline": "Shop by Specs, Not Stereotypes"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "womens_products_loaded": len(get_all_womens_products()),
        "mens_products_loaded": len(get_all_mens_products()),
        "golden_pairs_loaded": len(GOLDEN_PAIRS),
        "openai_configured": bool(os.getenv("OPENAI_API_KEY"))
    }


# =============================================================================
# Pink Tax Matching API (Feature A)
# =============================================================================

@app.post("/api/v1/match", response_model=MatchResponse, tags=["Pink Tax"])
async def find_product_match(request: ProductMatchRequest):
    """
    Find a men's equivalent for a women's product.

    This is the main endpoint for the "Fair Price" Engine feature.
    It searches for functionally equivalent products in the men's section
    that may be priced lower.

    **Example:**
    - Input: "Gillette Venus Razor" at $15.99
    - Output: "Gillette Fusion5" at $11.99 (25% savings)
    """
    match = find_mens_equivalent(
        womens_title=request.title,
        womens_price=request.price,
        category=request.category,
        ingredients=request.ingredients,
        brand=request.brand
    )

    if match:
        return MatchResponse(
            found_match=True,
            original_product=request.title,
            original_price=request.price,
            match=match,
            message=f"Found equivalent! Save ${match.savings_amount:.2f} ({match.savings_percent:.0f}%)"
        )
    else:
        return MatchResponse(
            found_match=False,
            original_product=request.title,
            original_price=request.price,
            match=None,
            message="No cheaper men's equivalent found for this product."
        )


@app.get("/api/v1/match/quick", response_model=MatchResponse, tags=["Pink Tax"])
async def quick_match(title: str, price: float, category: str = "personal_care"):
    """
    Quick match endpoint using query parameters.

    Useful for simple GET requests from the Chrome Extension.
    """
    try:
        cat = ProductCategory(category)
    except ValueError:
        cat = ProductCategory.PERSONAL_CARE

    match = find_mens_equivalent(
        womens_title=title,
        womens_price=price,
        category=cat
    )

    if match:
        return MatchResponse(
            found_match=True,
            original_product=title,
            original_price=price,
            match=match,
            message=f"Found equivalent! Save ${match.savings_amount:.2f} ({match.savings_percent:.0f}%)"
        )
    else:
        return MatchResponse(
            found_match=False,
            original_product=title,
            original_price=price,
            match=None,
            message="No cheaper men's equivalent found."
        )


# =============================================================================
# Universal Fit Decoder API (Feature B)
# =============================================================================

@app.post("/api/v1/size", response_model=SizeResponse, tags=["Sizing"])
async def get_size(request: SizeMatchRequest):
    """
    Get size recommendation for a men's clothing item.

    Accepts either:
    - A size chart image URL (uses GPT-4o Vision to OCR)
    - Pre-parsed size chart data

    Returns the recommended men's size based on user measurements.
    """
    recommendation = await get_size_recommendation(
        product_title=request.product_title,
        user_measurements=request.user_measurements,
        size_chart_url=request.size_chart_url,
        size_chart_data=request.size_chart_data
    )

    if recommendation:
        return SizeResponse(
            found_recommendation=True,
            recommendation=recommendation,
            message=f"Recommended size: {recommendation.recommended_size}"
        )
    else:
        return SizeResponse(
            found_recommendation=False,
            recommendation=None,
            message="Could not determine size recommendation. Please check the size chart manually."
        )


@app.post("/api/v1/clothing/match", tags=["Sizing"])
async def match_clothing_with_size(
    womens_product_title: str,
    waist: float,
    hip: float,
    chest: float = None
):
    """
    Complete clothing match: find men's equivalent AND the right size.

    This combines:
    1. Finding the cheaper men's version of a women's clothing item
    2. Calculating the correct size based on user measurements

    **Example:**
    - Input: "H&M Women's Boyfriend Hoodie", waist=28", hip=40"
    - Output: "H&M Men's Hoodie" in size S, saves $20
    """
    measurements = UserMeasurements(
        waist_inches=waist,
        hip_inches=hip,
        chest_inches=chest
    )

    mens_product, size_rec = find_mens_clothing_equivalent(
        womens_product_title,
        measurements
    )

    if not mens_product:
        raise HTTPException(
            status_code=404,
            detail="No men's equivalent found for this clothing item"
        )

    # Get women's product for comparison
    from .mock_data import WOMENS_CLOTHING, find_matching_key
    womens_key = find_matching_key(womens_product_title, WOMENS_CLOTHING)
    womens_product = WOMENS_CLOTHING.get(womens_key, {})
    womens_price = womens_product.get("price", 0)

    savings = womens_price - mens_product["price"] if womens_price else 0
    savings_pct = (savings / womens_price * 100) if womens_price > 0 else 0

    return {
        "found_match": True,
        "original_product": womens_product_title,
        "original_price": womens_price,
        "mens_equivalent": {
            "title": mens_product["title"],
            "price": mens_product["price"],
            "savings_amount": round(savings, 2),
            "savings_percent": round(savings_pct, 1)
        },
        "size_recommendation": {
            "size": size_rec.recommended_size if size_rec else "Unknown",
            "fit_notes": size_rec.fit_notes if size_rec else [],
            "measurements": size_rec.measurements_comparison if size_rec else {}
        },
        "message": f"Buy Men's {size_rec.recommended_size if size_rec else 'Unknown'} - Save ${savings:.2f}!"
    }


# =============================================================================
# Product Catalog API
# =============================================================================

@app.get("/api/v1/products/womens", tags=["Catalog"])
async def list_womens_products(category: str = None):
    """List all women's products in the database."""
    products = get_all_womens_products()

    if category:
        products = {k: v for k, v in products.items() if v.get("category") == category}

    return {
        "count": len(products),
        "products": list(products.values())
    }


@app.get("/api/v1/products/mens", tags=["Catalog"])
async def list_mens_products(category: str = None):
    """List all men's products in the database."""
    products = get_all_mens_products()

    if category:
        products = {k: v for k, v in products.items() if v.get("category") == category}

    return {
        "count": len(products),
        "products": list(products.values())
    }


@app.get("/api/v1/products/search", tags=["Catalog"])
async def search_products(q: str, category: str = None):
    """Search products by title."""
    try:
        cat = ProductCategory(category) if category else None
    except ValueError:
        cat = None

    results = search_products_by_title(q, cat)

    return {
        "query": q,
        "count": len(results),
        "results": results
    }


@app.get("/api/v1/pairs", tags=["Catalog"])
async def list_golden_pairs():
    """
    List all pre-verified product pairs.

    These are the "Golden Examples" with manually verified
    similarity scores and match reasons.
    """
    return {
        "count": len(GOLDEN_PAIRS),
        "pairs": GOLDEN_PAIRS
    }


# =============================================================================
# Savings Tracking API
# =============================================================================

# In-memory savings tracker (would use Supabase in production)
user_savings = {}


@app.post("/api/v1/savings/record", tags=["Savings"])
async def record_savings(user_id: str, amount: float, category: str, product_title: str):
    """
    Record a savings transaction.

    Called when a user follows a PinkVanity recommendation.
    """
    if user_id not in user_savings:
        user_savings[user_id] = []

    user_savings[user_id].append({
        "amount": amount,
        "category": category,
        "product": product_title
    })

    total = sum(s["amount"] for s in user_savings[user_id])

    return {
        "recorded": True,
        "transaction_amount": amount,
        "lifetime_total": round(total, 2),
        "transaction_count": len(user_savings[user_id])
    }


@app.get("/api/v1/savings/{user_id}", response_model=SavingsStats, tags=["Savings"])
async def get_savings_stats(user_id: str):
    """
    Get lifetime savings statistics for a user.

    Used to power the "Lifetime Savings Dashboard" in the extension popup.
    """
    if user_id not in user_savings or not user_savings[user_id]:
        return SavingsStats(
            total_saved=0,
            total_transactions=0,
            avg_savings_percent=0,
            top_categories=[]
        )

    transactions = user_savings[user_id]
    total = sum(t["amount"] for t in transactions)

    # Calculate category breakdown
    categories = {}
    for t in transactions:
        cat = t["category"]
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += t["amount"]

    top_categories = [
        {"category": k, "amount": round(v, 2)}
        for k, v in sorted(categories.items(), key=lambda x: -x[1])
    ][:5]

    return SavingsStats(
        total_saved=round(total, 2),
        total_transactions=len(transactions),
        avg_savings_percent=25.0,  # Mock average
        top_categories=top_categories
    )


# =============================================================================
# Demo Endpoints (Pre-recorded responses for hackathon)
# =============================================================================

@app.get("/api/v1/demo/razor", tags=["Demo"])
async def demo_razor():
    """
    Pre-recorded demo response for Gillette Venus Razor.

    Use this endpoint during the hackathon presentation
    to ensure a consistent, impressive demo.
    """
    return {
        "found_match": True,
        "original_product": "Gillette Venus Original Razor",
        "original_price": 15.99,
        "match": {
            "title": "Gillette Fusion5 ProGlide Razor",
            "price": 11.99,
            "savings_amount": 4.00,
            "savings_percent": 25.0,
            "similarity_score": 0.87,
            "match_reasons": [
                "Same blade count (5 blades)",
                "Both have aloe moisture strips",
                "Both have pivoting heads",
                "Same brand quality (Gillette)"
            ],
            "image_url": "https://example.com/fusion5.jpg"
        },
        "pink_tax_info": {
            "category": "Personal Care - Razors",
            "avg_pink_tax": "13%",
            "this_product_tax": "25%",
            "annual_impact": "$48/year if purchased monthly"
        },
        "message": "Swap & Save $4.00 (25%)!"
    }


@app.get("/api/v1/demo/shave-gel", tags=["Demo"])
async def demo_shave_gel():
    """Pre-recorded demo for shave gel comparison."""
    return {
        "found_match": True,
        "original_product": "Skintimate Raspberry Rain Shave Gel",
        "original_price": 3.99,
        "match": {
            "title": "Barbasol Soothing Aloe Shave Cream",
            "price": 1.99,
            "savings_amount": 2.00,
            "savings_percent": 50.0,
            "similarity_score": 0.91,
            "match_reasons": [
                "Identical first 3 active ingredients",
                "Both contain aloe vera",
                "Both designed for sensitive skin",
                "Men's version is actually LARGER (10oz vs 7oz)"
            ]
        },
        "pink_tax_info": {
            "category": "Personal Care - Shaving",
            "avg_pink_tax": "13%",
            "this_product_tax": "50%",
            "annual_impact": "$24/year if purchased monthly",
            "bonus": "Men's version gives you 43% MORE product!"
        },
        "message": "Identical utility found! Save 50% AND get more product!"
    }


@app.get("/api/v1/demo/hoodie", tags=["Demo"])
async def demo_hoodie():
    """Pre-recorded demo for hoodie with sizing."""
    return {
        "found_match": True,
        "original_product": "H&M Women's Boyfriend Fit Hoodie",
        "original_price": 45.00,
        "mens_equivalent": {
            "title": "H&M Men's Regular Fit Hoodie",
            "price": 24.99,
            "savings_amount": 20.01,
            "savings_percent": 44.5
        },
        "size_recommendation": {
            "size": "S",
            "fit_notes": [
                "Waist fits well with 2\" ease",
                "Body length: 27 inches (1 inch longer than women's)",
                "Chest has comfortable 4\" ease for relaxed fit"
            ],
            "measurements": {
                "waist": {"garment": 30, "user": 28, "diff": 2},
                "chest": {"garment": 36, "user": 32, "diff": 4},
                "length": {"garment": 27}
            }
        },
        "pink_tax_info": {
            "category": "Clothing - Hoodies",
            "avg_pink_tax": "8%",
            "this_product_tax": "44%",
            "annual_impact": "$40/year if bought twice",
            "sizing_note": "Women's 'Boyfriend Fit' is literally the men's cut at 80% markup"
        },
        "message": "Buy Men's Size S. Save $20 (44%)! Fits your measurements perfectly."
    }


@app.get("/api/v1/demo/deodorant", tags=["Demo"])
async def demo_deodorant():
    """Pre-recorded demo for deodorant comparison."""
    return {
        "found_match": True,
        "original_product": "Degree Women UltraClear Antiperspirant - Pure Rain",
        "original_price": 6.99,
        "match": {
            "title": "Degree Men UltraClear Antiperspirant",
            "price": 5.49,
            "savings_amount": 1.50,
            "savings_percent": 21.5,
            "similarity_score": 0.96,
            "match_reasons": [
                "Same brand (Degree)",
                "Identical active ingredient formula",
                "Same 48-hour protection claim",
                "Men's version has MORE product (2.7oz vs 2.6oz)"
            ]
        },
        "pink_tax_info": {
            "category": "Personal Care - Deodorant",
            "avg_pink_tax": "13%",
            "this_product_tax": "21.5%",
            "annual_impact": "$18/year if purchased monthly"
        },
        "message": "Same protection, more product, less money!"
    }


@app.get("/api/v1/demo/jeans", tags=["Demo"])
async def demo_jeans():
    """Pre-recorded demo for jeans with sizing translation."""
    return {
        "found_match": True,
        "original_product": "American Eagle Women's Mom Jeans (Size 8)",
        "original_price": 59.95,
        "mens_equivalent": {
            "title": "American Eagle Men's Original Straight Jeans",
            "price": 49.95,
            "savings_amount": 10.00,
            "savings_percent": 16.7
        },
        "size_recommendation": {
            "size": "28x30",
            "fit_notes": [
                "Women's Size 8 = 28\" waist measurement",
                "Hip fits well - Men's 28 has 36\" hip",
                "Consider 28x32 for longer inseam"
            ],
            "measurements": {
                "waist": {"garment": 28, "user": 28, "diff": 0},
                "hip": {"garment": 36, "user": 38, "diff": -2},
                "inseam": {"garment": 30}
            }
        },
        "sizing_education": {
            "problem": "Women's Size 8 is meaningless - it's varied by 6 inches since the 1950s",
            "solution": "Men's jeans use actual measurements: 28x30 = 28 inch waist, 30 inch inseam",
            "tip": "Always measure yourself - don't trust arbitrary size numbers"
        },
        "message": "Buy Men's 28x30. Save $10 and know exactly what you're getting!"
    }


# =============================================================================
# Batch Operations (For efficient extension use)
# =============================================================================

@app.post("/api/v1/match/batch", tags=["Pink Tax"])
async def batch_match(products: list[dict]):
    """
    Find matches for multiple products at once.

    Useful for analyzing a shopping cart or wishlist.

    Example input:
    [
        {"title": "Gillette Venus Razor", "price": 15.99, "category": "personal_care"},
        {"title": "Skintimate Shave Gel", "price": 3.99, "category": "personal_care"}
    ]
    """
    results = []
    total_potential_savings = 0

    for product in products:
        try:
            cat = ProductCategory(product.get("category", "personal_care"))
        except ValueError:
            cat = ProductCategory.PERSONAL_CARE

        match = find_mens_equivalent(
            womens_title=product.get("title", ""),
            womens_price=product.get("price", 0),
            category=cat,
            ingredients=product.get("ingredients"),
            brand=product.get("brand")
        )

        if match:
            total_potential_savings += match.savings_amount
            results.append({
                "original": product.get("title"),
                "original_price": product.get("price"),
                "match": {
                    "title": match.title,
                    "price": match.price,
                    "savings": match.savings_amount,
                    "similarity": match.similarity_score
                }
            })
        else:
            results.append({
                "original": product.get("title"),
                "original_price": product.get("price"),
                "match": None
            })

    return {
        "products_analyzed": len(products),
        "matches_found": len([r for r in results if r["match"]]),
        "total_potential_savings": round(total_potential_savings, 2),
        "results": results
    }


# =============================================================================
# Lifetime Savings Dashboard
# =============================================================================

@app.get("/api/v1/dashboard/{user_id}", tags=["Savings"])
async def get_dashboard(user_id: str):
    """
    Get comprehensive dashboard data for the extension popup.

    Returns lifetime savings, recent transactions, category breakdown,
    and motivational stats for the "Wow" factor.
    """
    if user_id not in user_savings or not user_savings[user_id]:
        # Return demo data for new users
        return {
            "user_id": user_id,
            "lifetime_stats": {
                "total_saved": 0,
                "transactions": 0,
                "avg_savings_percent": 0,
                "estimated_annual_savings": 0
            },
            "category_breakdown": [],
            "recent_transactions": [],
            "achievements": [
                {"id": "first_swap", "name": "First Swap", "unlocked": False, "description": "Make your first PinkVanity swap"},
                {"id": "ten_saved", "name": "$10 Club", "unlocked": False, "description": "Save $10 total"},
                {"id": "fifty_saved", "name": "Savvy Shopper", "unlocked": False, "description": "Save $50 total"}
            ],
            "pink_tax_facts": {
                "avg_lifetime_cost": "$82,000",
                "annual_impact": "$1,351",
                "most_taxed_category": "Personal Care (13% average)"
            },
            "message": "Start shopping to see your savings grow!"
        }

    transactions = user_savings[user_id]
    total = sum(t["amount"] for t in transactions)

    # Category breakdown
    categories = {}
    for t in transactions:
        cat = t.get("category", "other")
        if cat not in categories:
            categories[cat] = {"count": 0, "amount": 0}
        categories[cat]["count"] += 1
        categories[cat]["amount"] += t["amount"]

    category_breakdown = [
        {"category": k, "count": v["count"], "amount": round(v["amount"], 2)}
        for k, v in sorted(categories.items(), key=lambda x: -x[1]["amount"])
    ]

    # Recent transactions (last 10)
    recent = transactions[-10:][::-1]

    # Achievements
    achievements = [
        {"id": "first_swap", "name": "First Swap", "unlocked": len(transactions) >= 1, "description": "Make your first PinkVanity swap"},
        {"id": "ten_saved", "name": "$10 Club", "unlocked": total >= 10, "description": "Save $10 total"},
        {"id": "fifty_saved", "name": "Savvy Shopper", "unlocked": total >= 50, "description": "Save $50 total"},
        {"id": "hundred_saved", "name": "Century Saver", "unlocked": total >= 100, "description": "Save $100 total"},
        {"id": "five_swaps", "name": "Regular Swapper", "unlocked": len(transactions) >= 5, "description": "Complete 5 swaps"}
    ]

    avg_savings = sum(t.get("savings_percent", 25) for t in transactions) / len(transactions) if transactions else 0

    return {
        "user_id": user_id,
        "lifetime_stats": {
            "total_saved": round(total, 2),
            "transactions": len(transactions),
            "avg_savings_percent": round(avg_savings, 1),
            "estimated_annual_savings": round(total * 12 / max(len(transactions), 1), 2)
        },
        "category_breakdown": category_breakdown,
        "recent_transactions": recent,
        "achievements": achievements,
        "pink_tax_facts": {
            "avg_lifetime_cost": "$82,000",
            "annual_impact": "$1,351",
            "most_taxed_category": "Personal Care (13% average)",
            "your_contribution": f"You've fought back ${total:.2f} of the Pink Tax!"
        },
        "message": f"You've saved ${total:.2f} so far. Keep going!"
    }


@app.post("/api/v1/analyze/ingredients", tags=["Analysis"])
async def analyze_ingredients(womens_ingredients: list[str], mens_ingredients: list[str]):
    """
    Analyze ingredient similarity between two products.

    This is useful for debugging and understanding
    why products are (or aren't) matched.
    """
    result = check_first_three_match(womens_ingredients, mens_ingredients)

    # Also compute full similarity
    from .services.matching import ingredient_similarity
    full_similarity = ingredient_similarity(womens_ingredients, mens_ingredients)

    return {
        "first_three_analysis": result,
        "full_similarity_score": round(full_similarity, 3),
        "recommendation": "Match" if result["matches"] and full_similarity > 0.5 else "No Match",
        "explanation": (
            "Products are functionally equivalent - first 3 ingredients match"
            if result["matches"]
            else "Products have different formulations"
        )
    }


@app.get("/api/v1/demo/all", tags=["Demo"])
async def demo_all_products():
    """
    Get all demo products for presentation.

    Returns a curated list of the best Pink Tax examples
    for the hackathon demo.
    """
    return {
        "golden_examples": [
            {
                "category": "Razors",
                "womens": {"title": "Gillette Venus", "price": 15.99},
                "mens": {"title": "Gillette Fusion5", "price": 11.99},
                "savings": {"amount": 4.00, "percent": 25},
                "highlight": "Same blade count, same brand, just different marketing"
            },
            {
                "category": "Shave Gel",
                "womens": {"title": "Skintimate Raspberry", "price": 3.99},
                "mens": {"title": "Barbasol Aloe", "price": 1.99},
                "savings": {"amount": 2.00, "percent": 50},
                "highlight": "Men's version is 43% LARGER and 50% cheaper"
            },
            {
                "category": "Hoodie",
                "womens": {"title": "H&M Boyfriend Hoodie", "price": 45.00},
                "mens": {"title": "H&M Regular Hoodie", "price": 24.99},
                "savings": {"amount": 20.01, "percent": 44},
                "highlight": "'Boyfriend fit' is literally the men's cut at 80% markup"
            },
            {
                "category": "Deodorant",
                "womens": {"title": "Degree Women UltraClear", "price": 6.99},
                "mens": {"title": "Degree Men UltraClear", "price": 5.49},
                "savings": {"amount": 1.50, "percent": 21.5},
                "highlight": "Identical formula, only fragrance differs"
            },
            {
                "category": "Jeans",
                "womens": {"title": "AE Mom Jeans (Size 8)", "price": 59.95},
                "mens": {"title": "AE Straight Jeans (28x30)", "price": 49.95},
                "savings": {"amount": 10.00, "percent": 16.7},
                "highlight": "Men's uses real measurements, women's uses arbitrary numbers"
            }
        ],
        "total_annual_savings_potential": "$1,351 (average woman)",
        "categories_covered": ["Razors", "Shaving", "Deodorant", "Clothing", "Skincare"],
        "message": "These examples demonstrate the Pink Tax across multiple product categories"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )

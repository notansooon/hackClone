"""
Universal Fit Decoder - AI-powered size chart reading and translation.

Uses GPT-4o Vision to OCR size charts and translates women's sizing to men's measurements.
"""
import os
import json
import httpx
from typing import Optional
from ..models import UserMeasurements, SizeRecommendation
from ..mock_data import MENS_CLOTHING, WOMENS_CLOTHING, find_matching_key


# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


async def ocr_size_chart_with_gpt4o(image_url: str) -> dict:
    """
    Use GPT-4o Vision to extract size chart data from an image.

    Args:
        image_url: URL to the size chart image

    Returns:
        Dictionary mapping sizes to measurements
        e.g., {"S": {"chest": 36, "waist": 30, "length": 27}, ...}
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not configured")

    prompt = """Analyze this size chart image and extract all size measurements.

Return a JSON object where:
- Keys are the size labels (XS, S, M, L, XL, etc. OR measurements like 28x30, 32x32)
- Values are objects containing measurements in INCHES

Expected measurements to extract (if visible):
- chest: Chest/bust measurement
- waist: Waist measurement
- hip: Hip measurement
- length: Body/torso length
- inseam: Inseam length (for pants)
- shoulder: Shoulder width

Example output format:
{
    "S": {"chest": 36, "waist": 30, "length": 27},
    "M": {"chest": 38, "waist": 32, "length": 28},
    "L": {"chest": 40, "waist": 34, "length": 29}
}

If a measurement is in centimeters, convert to inches (divide by 2.54).
Only return the JSON, no other text."""

    async with httpx.AsyncClient() as client:
        response = await client.post(
            OPENAI_API_URL,
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url}
                            }
                        ]
                    }
                ],
                "max_tokens": 1000
            },
            timeout=30.0
        )

        if response.status_code != 200:
            raise Exception(f"OpenAI API error: {response.text}")

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        # Parse JSON from response (handle markdown code blocks)
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]

        return json.loads(content.strip())


def find_best_size(
    user_measurements: UserMeasurements,
    size_chart: dict,
    garment_type: str = "top"
) -> tuple[str, dict]:
    """
    Find the best fitting size based on user measurements.

    Args:
        user_measurements: User's body measurements
        size_chart: Size chart data {size: {measurement: value}}
        garment_type: "top" for shirts/hoodies, "bottom" for pants/jeans

    Returns:
        Tuple of (recommended_size, fit_analysis)
    """
    best_size = None
    best_score = float('inf')
    best_comparison = {}

    for size, measurements in size_chart.items():
        score = 0
        comparison = {}

        if garment_type == "bottom":
            # For pants, prioritize waist and hip fit
            if "waist" in measurements:
                waist_diff = measurements["waist"] - user_measurements.waist_inches
                # Allow 1-2 inches of ease for comfort
                if waist_diff >= 0 and waist_diff <= 2:
                    score += waist_diff
                else:
                    score += abs(waist_diff) * 2  # Penalize poor fit
                comparison["waist"] = {
                    "garment": measurements["waist"],
                    "user": user_measurements.waist_inches,
                    "diff": round(waist_diff, 1)
                }

            if "hip" in measurements and user_measurements.hip_inches:
                hip_diff = measurements["hip"] - user_measurements.hip_inches
                # Hips need more room
                if hip_diff >= 0 and hip_diff <= 3:
                    score += hip_diff * 0.5
                else:
                    score += abs(hip_diff) * 1.5
                comparison["hip"] = {
                    "garment": measurements["hip"],
                    "user": user_measurements.hip_inches,
                    "diff": round(hip_diff, 1)
                }
        else:
            # For tops, prioritize chest fit
            if "chest" in measurements and user_measurements.chest_inches:
                chest_diff = measurements["chest"] - user_measurements.chest_inches
                # Allow 2-4 inches of ease for tops
                if chest_diff >= 2 and chest_diff <= 4:
                    score += chest_diff - 2
                else:
                    score += abs(chest_diff - 3) * 2
                comparison["chest"] = {
                    "garment": measurements["chest"],
                    "user": user_measurements.chest_inches,
                    "diff": round(chest_diff, 1)
                }

            if "waist" in measurements:
                waist_diff = measurements["waist"] - user_measurements.waist_inches
                # Tops are more forgiving at waist
                score += abs(waist_diff) * 0.3
                comparison["waist"] = {
                    "garment": measurements["waist"],
                    "user": user_measurements.waist_inches,
                    "diff": round(waist_diff, 1)
                }

        # Track length for fit notes
        if "length" in measurements:
            comparison["length"] = {
                "garment": measurements["length"],
                "diff_note": "See fit notes"
            }

        if score < best_score:
            best_score = score
            best_size = size
            best_comparison = comparison

    return best_size, best_comparison


def generate_fit_notes(comparison: dict, garment_type: str) -> list[str]:
    """Generate human-readable fit notes from measurement comparison."""
    notes = []

    for measurement, data in comparison.items():
        if "diff" not in data:
            continue

        diff = data["diff"]

        if measurement == "waist":
            if diff > 2:
                notes.append(f"Waist will be loose by {diff:.0f} inches - consider sizing down")
            elif diff < 0:
                notes.append(f"Waist may be snug by {abs(diff):.0f} inch(es)")
            else:
                notes.append(f"Waist fits well with {diff:.0f}\" ease")

        elif measurement == "hip":
            if diff > 4:
                notes.append(f"Hip area will be very loose")
            elif diff < 0:
                notes.append(f"Hip area may be tight - consider sizing up")
            else:
                notes.append(f"Hip fit looks good")

        elif measurement == "chest":
            if diff > 5:
                notes.append(f"Chest will be oversized by {diff:.0f} inches")
            elif diff < 2:
                notes.append(f"Chest may be fitted/snug")
            else:
                notes.append(f"Chest has comfortable {diff:.0f}\" ease")

        elif measurement == "length":
            notes.append(f"Body length: {data.get('garment', 'unknown')} inches")

    return notes


async def get_size_recommendation(
    product_title: str,
    user_measurements: UserMeasurements,
    size_chart_url: Optional[str] = None,
    size_chart_data: Optional[dict] = None
) -> Optional[SizeRecommendation]:
    """
    Get a size recommendation for a men's clothing item.

    Args:
        product_title: Title of the men's product
        user_measurements: User's body measurements
        size_chart_url: Optional URL to size chart image (uses GPT-4o OCR)
        size_chart_data: Optional pre-parsed size chart data

    Returns:
        SizeRecommendation if successful, None otherwise
    """
    # Get size chart data
    chart_data = None

    if size_chart_data:
        chart_data = size_chart_data
    elif size_chart_url:
        try:
            chart_data = await ocr_size_chart_with_gpt4o(size_chart_url)
        except Exception as e:
            print(f"OCR failed: {e}")
            # Fall back to mock data

    # If no external data, try to find in our mock database
    if not chart_data:
        product_key = find_matching_key(product_title, MENS_CLOTHING)
        if product_key and product_key in MENS_CLOTHING:
            chart_data = MENS_CLOTHING[product_key].get("size_chart")

    if not chart_data:
        return None

    # Determine garment type
    title_lower = product_title.lower()
    if any(word in title_lower for word in ["jeans", "pants", "shorts", "trousers"]):
        garment_type = "bottom"
    else:
        garment_type = "top"

    # Find best size
    recommended_size, comparison = find_best_size(
        user_measurements,
        chart_data,
        garment_type
    )

    if not recommended_size:
        return None

    # Generate fit notes
    fit_notes = generate_fit_notes(comparison, garment_type)

    return SizeRecommendation(
        recommended_size=recommended_size,
        fit_notes=fit_notes,
        measurements_comparison=comparison
    )


def find_mens_clothing_equivalent(
    womens_product_title: str,
    user_measurements: UserMeasurements
) -> tuple[Optional[dict], Optional[SizeRecommendation]]:
    """
    Find a men's clothing equivalent and the right size for the user.

    This is the main function for the "Universal Fit Decoder" feature.

    Returns:
        Tuple of (mens_product_info, size_recommendation)
    """
    # Find the women's product
    womens_key = find_matching_key(womens_product_title, WOMENS_CLOTHING)
    if not womens_key:
        return None, None

    womens_product = WOMENS_CLOTHING[womens_key]

    # Find matching men's product
    mens_product = None
    for mens_key, product in MENS_CLOTHING.items():
        # Match by brand and subcategory
        if (product.get("brand") == womens_product.get("brand") and
            product.get("subcategory") == womens_product.get("subcategory")):
            mens_product = product
            break

    if not mens_product:
        return None, None

    # Get size recommendation
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    size_rec = loop.run_until_complete(
        get_size_recommendation(
            mens_product["title"],
            user_measurements,
            size_chart_data=mens_product.get("size_chart")
        )
    )

    return mens_product, size_rec

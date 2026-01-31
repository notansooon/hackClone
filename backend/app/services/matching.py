"""
Pink Tax Matching Engine - Find men's equivalents for women's products.

Uses Jaccard Similarity on ingredient lists and fuzzy matching on product attributes.
"""
import re
from typing import Optional
from ..models import ProductMatch, ProductCategory
from ..mock_data import (
    WOMENS_PRODUCTS, MENS_PRODUCTS,
    WOMENS_CLOTHING, MENS_CLOTHING,
    get_golden_pair, get_all_womens_products, get_all_mens_products
)


def normalize_ingredient(ingredient: str) -> str:
    """Normalize an ingredient string for comparison."""
    # Lowercase, remove extra whitespace, remove common filler words
    normalized = ingredient.lower().strip()
    normalized = re.sub(r'\s+', ' ', normalized)
    # Remove percentages and numbers
    normalized = re.sub(r'\d+%?\s*', '', normalized)
    return normalized


def jaccard_similarity(set1: set, set2: set) -> float:
    """
    Calculate Jaccard Similarity between two sets.

    Jaccard Index = |A ∩ B| / |A ∪ B|
    Returns a value between 0 (no overlap) and 1 (identical).
    """
    if not set1 or not set2:
        return 0.0

    intersection = len(set1 & set2)
    union = len(set1 | set2)

    return intersection / union if union > 0 else 0.0


def ingredient_similarity(ingredients1: list[str], ingredients2: list[str]) -> float:
    """
    Calculate similarity between two ingredient lists.

    Uses Jaccard Similarity on normalized ingredients.
    Also gives bonus weight to matching first 3 ingredients (most important).

    The "First 3 Rule": In cosmetics/personal care, the first 3 ingredients
    typically make up 70-80% of the product formula. If these match,
    the products are functionally equivalent.
    """
    if not ingredients1 or not ingredients2:
        return 0.0

    # Normalize all ingredients
    norm1 = {normalize_ingredient(i) for i in ingredients1}
    norm2 = {normalize_ingredient(i) for i in ingredients2}

    # Base Jaccard similarity
    base_similarity = jaccard_similarity(norm1, norm2)

    # First 3 ingredients check (critical for Pink Tax detection)
    first_3_1 = [normalize_ingredient(i) for i in ingredients1[:3]]
    first_3_2 = [normalize_ingredient(i) for i in ingredients2[:3]]

    # Check exact positional matches (most stringent)
    positional_matches = sum(1 for a, b in zip(first_3_1, first_3_2) if a == b)

    # Check set overlap (more lenient)
    first_3_set_1 = set(first_3_1)
    first_3_set_2 = set(first_3_2)
    first_3_overlap = jaccard_similarity(first_3_set_1, first_3_set_2)

    # Weighted scoring:
    # - 40% base Jaccard (overall formula similarity)
    # - 35% first-3 set overlap (same key ingredients)
    # - 25% positional bonus (same order = same formulation)
    positional_bonus = positional_matches / 3.0

    return (base_similarity * 0.40) + (first_3_overlap * 0.35) + (positional_bonus * 0.25)


def check_first_three_match(ingredients1: list[str], ingredients2: list[str]) -> dict:
    """
    Check if the first 3 ingredients match between two products.

    This is the core of the Pink Tax detection - if the first 3 active
    ingredients match, the products are functionally identical.

    Returns:
        dict with match status, count, and details
    """
    if not ingredients1 or not ingredients2:
        return {"matches": False, "count": 0, "details": []}

    first_3_1 = [normalize_ingredient(i) for i in ingredients1[:3]]
    first_3_2 = [normalize_ingredient(i) for i in ingredients2[:3]]

    matches = []
    for i, (ing1, ing2) in enumerate(zip(first_3_1, first_3_2)):
        if ing1 == ing2:
            matches.append({
                "position": i + 1,
                "ingredient": ingredients1[i],
                "exact_match": True
            })
        elif ing1 in ing2 or ing2 in ing1:
            matches.append({
                "position": i + 1,
                "ingredient1": ingredients1[i],
                "ingredient2": ingredients2[i],
                "partial_match": True
            })

    return {
        "matches": len(matches) >= 2,  # At least 2 of 3 must match
        "count": len(matches),
        "threshold": 2,
        "details": matches,
        "verdict": "Functionally equivalent" if len(matches) >= 2 else "Different formulation"
    }


def attribute_similarity(attrs1: dict, attrs2: dict) -> float:
    """
    Calculate similarity between product attributes.

    Compares numeric and boolean attributes.
    """
    if not attrs1 or not attrs2:
        return 0.5  # Neutral if no attributes

    common_keys = set(attrs1.keys()) & set(attrs2.keys())
    if not common_keys:
        return 0.5

    matches = 0
    total = len(common_keys)

    for key in common_keys:
        val1, val2 = attrs1[key], attrs2[key]

        if isinstance(val1, bool) and isinstance(val2, bool):
            if val1 == val2:
                matches += 1
        elif isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            # For numeric values, consider them similar if within 20%
            if val1 == 0 and val2 == 0:
                matches += 1
            elif val1 != 0:
                ratio = abs(val1 - val2) / max(abs(val1), abs(val2))
                if ratio <= 0.2:
                    matches += 1
                else:
                    matches += max(0, 1 - ratio)
        elif val1 == val2:
            matches += 1

    return matches / total if total > 0 else 0.5


def title_similarity(title1: str, title2: str) -> float:
    """
    Calculate similarity between product titles using word overlap.
    """
    # Extract meaningful words (remove common filler words)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'for', 'with', 'in', 'of', 'to'}

    words1 = {w.lower() for w in re.findall(r'\w+', title1) if w.lower() not in stop_words}
    words2 = {w.lower() for w in re.findall(r'\w+', title2) if w.lower() not in stop_words}

    return jaccard_similarity(words1, words2)


def find_matching_key(title: str, products_dict: dict) -> Optional[str]:
    """Find the best matching product key based on title."""
    title_lower = title.lower()

    # First try exact key match
    for key in products_dict:
        if key in title_lower or title_lower in key:
            return key

    # Then try word overlap
    best_match = None
    best_score = 0

    for key, product in products_dict.items():
        score = title_similarity(title, product.get("title", key))
        if score > best_score and score > 0.3:
            best_score = score
            best_match = key

    return best_match


def find_mens_equivalent(
    womens_title: str,
    womens_price: float,
    category: ProductCategory,
    ingredients: Optional[list[str]] = None,
    brand: Optional[str] = None
) -> Optional[ProductMatch]:
    """
    Find the best men's equivalent for a women's product.

    Args:
        womens_title: Title of the women's product
        womens_price: Price of the women's product
        category: Product category
        ingredients: List of ingredients/materials (if available)
        brand: Product brand (if known)

    Returns:
        ProductMatch if a suitable equivalent is found, None otherwise
    """
    # Determine which product databases to use
    if category == ProductCategory.CLOTHING:
        womens_db = WOMENS_CLOTHING
        mens_db = MENS_CLOTHING
    else:
        womens_db = WOMENS_PRODUCTS
        mens_db = MENS_PRODUCTS

    # Try to find the women's product in our database
    womens_key = find_matching_key(womens_title, womens_db)
    womens_product = womens_db.get(womens_key) if womens_key else None

    # Check for pre-computed golden pair
    if womens_product:
        golden_pair = get_golden_pair(womens_product["id"])
        if golden_pair:
            # Find the men's product from the golden pair
            for mens_key, mens_product in mens_db.items():
                if mens_product["id"] == golden_pair["mens_id"]:
                    savings = womens_price - mens_product["price"]
                    savings_pct = (savings / womens_price) * 100 if womens_price > 0 else 0

                    return ProductMatch(
                        title=mens_product["title"],
                        price=mens_product["price"],
                        savings_amount=round(savings, 2),
                        savings_percent=round(savings_pct, 1),
                        similarity_score=golden_pair["similarity_score"],
                        match_reasons=golden_pair["match_reasons"],
                        product_url=None,
                        image_url=mens_product.get("image_url")
                    )

    # Fall back to dynamic matching
    best_match = None
    best_score = 0

    for mens_key, mens_product in mens_db.items():
        # Skip if different subcategory
        if womens_product and womens_product.get("subcategory") != mens_product.get("subcategory"):
            continue

        # Calculate similarity scores
        scores = []

        # 1. Title similarity (weight: 20%)
        title_sim = title_similarity(womens_title, mens_product["title"])
        scores.append(("title", title_sim, 0.2))

        # 2. Ingredient similarity (weight: 50%)
        mens_ingredients = mens_product.get("ingredients") or mens_product.get("materials", [])
        womens_ingredients = ingredients or (womens_product.get("ingredients") if womens_product else None)

        if womens_ingredients and mens_ingredients:
            ing_sim = ingredient_similarity(womens_ingredients, mens_ingredients)
            scores.append(("ingredients", ing_sim, 0.5))

        # 3. Attribute similarity (weight: 20%)
        if womens_product and "attributes" in womens_product and "attributes" in mens_product:
            attr_sim = attribute_similarity(womens_product["attributes"], mens_product["attributes"])
            scores.append(("attributes", attr_sim, 0.2))

        # 4. Brand match bonus (weight: 10%)
        brand_match = 0
        if brand:
            brand_match = 1.0 if brand.lower() == mens_product.get("brand", "").lower() else 0
        elif womens_product:
            brand_match = 1.0 if womens_product.get("brand") == mens_product.get("brand") else 0
        scores.append(("brand", brand_match, 0.1))

        # Calculate weighted average
        total_weight = sum(s[2] for s in scores)
        weighted_score = sum(s[1] * s[2] for s in scores) / total_weight if total_weight > 0 else 0

        # Only consider if price is lower and similarity is reasonable
        if mens_product["price"] < womens_price and weighted_score > best_score and weighted_score > 0.4:
            best_score = weighted_score
            best_match = (mens_key, mens_product, scores)

    if best_match:
        mens_key, mens_product, scores = best_match
        savings = womens_price - mens_product["price"]
        savings_pct = (savings / womens_price) * 100 if womens_price > 0 else 0

        # Generate compelling match reasons for demo
        match_reasons = []

        # Check first 3 ingredients specifically
        mens_ingredients = mens_product.get("ingredients") or mens_product.get("materials", [])
        womens_ing = ingredients or (womens_product.get("ingredients") if womens_product else None)
        if womens_ing and mens_ingredients:
            first_3_check = check_first_three_match(womens_ing, mens_ingredients)
            if first_3_check["matches"]:
                match_reasons.append(f"First {first_3_check['count']} of 3 key ingredients match")

        for score_name, score_val, _ in scores:
            if score_val > 0.7:
                if score_name == "ingredients" and not any("ingredient" in r.lower() for r in match_reasons):
                    match_reasons.append("Highly similar ingredient formula")
                elif score_name == "brand":
                    match_reasons.append(f"Same brand ({mens_product.get('brand', 'Unknown')})")
                elif score_name == "attributes":
                    # Get specific attribute matches
                    if womens_product and "attributes" in womens_product:
                        w_attrs = womens_product["attributes"]
                        m_attrs = mens_product.get("attributes", {})
                        if w_attrs.get("blade_count") == m_attrs.get("blade_count"):
                            match_reasons.append(f"Same blade count ({w_attrs['blade_count']} blades)")
                        if w_attrs.get("size_oz") and m_attrs.get("size_oz"):
                            if m_attrs["size_oz"] > w_attrs["size_oz"]:
                                match_reasons.append(f"Men's is LARGER ({m_attrs['size_oz']}oz vs {w_attrs['size_oz']}oz)")
                        if w_attrs.get("protection_hours") == m_attrs.get("protection_hours"):
                            match_reasons.append(f"Same {w_attrs['protection_hours']}-hour protection")
                    else:
                        match_reasons.append("Similar product specifications")

        if not match_reasons:
            match_reasons.append("Functionally equivalent product")

        # Add savings highlight
        if savings_pct >= 40:
            match_reasons.append(f"Exceptional savings opportunity ({savings_pct:.0f}%)")
        elif savings_pct >= 25:
            match_reasons.append(f"Significant Pink Tax markup ({savings_pct:.0f}%)")

        return ProductMatch(
            title=mens_product["title"],
            price=mens_product["price"],
            savings_amount=round(savings, 2),
            savings_percent=round(savings_pct, 1),
            similarity_score=round(best_score, 2),
            match_reasons=match_reasons,
            product_url=None,
            image_url=mens_product.get("image_url")
        )

    return None


def search_products_by_title(query: str, category: Optional[ProductCategory] = None) -> list[dict]:
    """
    Search for products by title query.

    Returns a list of matching products from both women's and men's databases.
    """
    results = []
    query_lower = query.lower()

    all_products = {**get_all_womens_products(), **get_all_mens_products()}

    for key, product in all_products.items():
        # Filter by category if specified
        if category:
            prod_cat = product.get("category", "")
            if category == ProductCategory.CLOTHING and prod_cat != "clothing":
                continue
            elif category == ProductCategory.PERSONAL_CARE and prod_cat != "personal_care":
                continue

        # Check if query matches
        if query_lower in key or query_lower in product.get("title", "").lower():
            results.append(product)

    return results

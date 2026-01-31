"""Pydantic models for PinkVanity API."""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ProductCategory(str, Enum):
    PERSONAL_CARE = "personal_care"
    CLOTHING = "clothing"
    ACCESSORIES = "accessories"


class UserMeasurements(BaseModel):
    """User body measurements for size matching."""
    waist_inches: float = Field(..., ge=20, le=60, description="Waist measurement in inches")
    hip_inches: float = Field(..., ge=25, le=70, description="Hip measurement in inches")
    chest_inches: Optional[float] = Field(None, ge=25, le=60, description="Chest measurement in inches")
    height_inches: Optional[float] = Field(None, ge=48, le=84, description="Height in inches")


class ProductMatchRequest(BaseModel):
    """Request to find a men's equivalent for a women's product."""
    title: str = Field(..., min_length=1, description="Women's product title")
    price: float = Field(..., gt=0, description="Women's product price")
    category: ProductCategory = Field(..., description="Product category")
    ingredients: Optional[list[str]] = Field(None, description="List of ingredients/materials")
    brand: Optional[str] = Field(None, description="Product brand")
    retailer: Optional[str] = Field(None, description="Retailer name (e.g., Target, Uniqlo)")


class SizeMatchRequest(BaseModel):
    """Request to find correct men's size for a clothing item."""
    product_title: str = Field(..., description="Product title")
    user_measurements: UserMeasurements
    size_chart_url: Optional[str] = Field(None, description="URL to size chart image")
    size_chart_data: Optional[dict] = Field(None, description="Pre-parsed size chart data")


class ProductMatch(BaseModel):
    """A matched men's product equivalent."""
    title: str
    price: float
    savings_amount: float
    savings_percent: float
    similarity_score: float = Field(..., ge=0, le=1, description="0-1 similarity score")
    match_reasons: list[str]
    product_url: Optional[str] = None
    image_url: Optional[str] = None


class SizeRecommendation(BaseModel):
    """Size recommendation for a clothing item."""
    recommended_size: str
    fit_notes: list[str]
    measurements_comparison: dict[str, dict]


class MatchResponse(BaseModel):
    """Response containing product match results."""
    found_match: bool
    original_product: str
    original_price: float
    match: Optional[ProductMatch] = None
    message: str


class SizeResponse(BaseModel):
    """Response containing size recommendation."""
    found_recommendation: bool
    recommendation: Optional[SizeRecommendation] = None
    message: str


class SavingsStats(BaseModel):
    """User's lifetime savings statistics."""
    total_saved: float
    total_transactions: int
    avg_savings_percent: float
    top_categories: list[dict]

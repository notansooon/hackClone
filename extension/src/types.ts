/**
 * PinkVanity Types
 */

export interface UserMeasurements {
  waist_inches: number;
  hip_inches: number;
  chest_inches?: number;
  height_inches?: number;
}

export interface ProductMatch {
  title: string;
  price: number;
  savings_amount: number;
  savings_percent: number;
  similarity_score: number;
  match_reasons: string[];
  product_url?: string;
  image_url?: string;
}

export interface MatchResponse {
  found_match: boolean;
  original_product: string;
  original_price: number;
  match?: ProductMatch;
  message: string;
}

export interface SizeRecommendation {
  recommended_size: string;
  fit_notes: string[];
  measurements_comparison: Record<string, Record<string, number | string>>;
}

export interface ClothingMatchResponse {
  found_match: boolean;
  original_product: string;
  original_price: number;
  mens_equivalent: {
    title: string;
    price: number;
    savings_amount: number;
    savings_percent: number;
  };
  size_recommendation: {
    size: string;
    fit_notes: string[];
    measurements: Record<string, Record<string, number>>;
  };
  message: string;
}

export interface SavingsStats {
  total_saved: number;
  total_transactions: number;
  avg_savings_percent: number;
  top_categories: Array<{ category: string; amount: number }>;
}

export interface ScrapedProduct {
  title: string;
  price: number;
  category: 'personal_care' | 'clothing';
  ingredients?: string[];
  brand?: string;
  retailer: string;
  url: string;
}

export type SupportedSite = 'target' | 'uniqlo' | 'hm' | 'zara' | 'ae' | 'walmart';

export interface StorageData {
  measurements?: UserMeasurements;
  savings?: SavingsStats;
  enabled?: boolean;
  apiUrl?: string;
}

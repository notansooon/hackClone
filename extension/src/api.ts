/**
 * PinkVanity API Client
 */

import type { MatchResponse, ClothingMatchResponse, SavingsStats, UserMeasurements } from './types';

const DEFAULT_API_URL = 'http://localhost:8000';

async function getApiUrl(): Promise<string> {
  return new Promise((resolve) => {
    chrome.storage.sync.get(['apiUrl'], (result) => {
      resolve(result.apiUrl || DEFAULT_API_URL);
    });
  });
}

/**
 * Find a men's equivalent for a women's product (Pink Tax feature)
 */
export async function findProductMatch(
  title: string,
  price: number,
  category: 'personal_care' | 'clothing' = 'personal_care',
  ingredients?: string[]
): Promise<MatchResponse> {
  const apiUrl = await getApiUrl();

  const response = await fetch(`${apiUrl}/api/v1/match`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title,
      price,
      category,
      ingredients
    })
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

/**
 * Quick match using GET request
 */
export async function quickMatch(
  title: string,
  price: number,
  category: string = 'personal_care'
): Promise<MatchResponse> {
  const apiUrl = await getApiUrl();
  const params = new URLSearchParams({ title, price: String(price), category });

  const response = await fetch(`${apiUrl}/api/v1/match/quick?${params}`);

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

/**
 * Find clothing match with size recommendation
 */
export async function findClothingMatch(
  title: string,
  measurements: UserMeasurements
): Promise<ClothingMatchResponse> {
  const apiUrl = await getApiUrl();
  const params = new URLSearchParams({
    womens_product_title: title,
    waist: String(measurements.waist_inches),
    hip: String(measurements.hip_inches)
  });

  if (measurements.chest_inches) {
    params.append('chest', String(measurements.chest_inches));
  }

  const response = await fetch(`${apiUrl}/api/v1/clothing/match?${params}`, {
    method: 'POST'
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

/**
 * Record savings transaction
 */
export async function recordSavings(
  userId: string,
  amount: number,
  category: string,
  productTitle: string
): Promise<void> {
  const apiUrl = await getApiUrl();
  const params = new URLSearchParams({
    user_id: userId,
    amount: String(amount),
    category,
    product_title: productTitle
  });

  await fetch(`${apiUrl}/api/v1/savings/record?${params}`, {
    method: 'POST'
  });
}

/**
 * Get user's savings statistics
 */
export async function getSavingsStats(userId: string): Promise<SavingsStats> {
  const apiUrl = await getApiUrl();

  const response = await fetch(`${apiUrl}/api/v1/savings/${userId}`);

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

/**
 * Get demo response for hackathon (pre-recorded)
 */
export async function getDemoResponse(type: 'razor' | 'shave-gel' | 'hoodie'): Promise<any> {
  const apiUrl = await getApiUrl();

  const response = await fetch(`${apiUrl}/api/v1/demo/${type}`);

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

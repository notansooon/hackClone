/**
 * Product Scrapers for Supported Sites
 *
 * Each scraper extracts product information from a specific retailer's page.
 */

import type { ScrapedProduct, SupportedSite } from './types';

/**
 * Detect which supported site we're on
 */
export function detectSite(): SupportedSite | null {
  const hostname = window.location.hostname.toLowerCase();

  if (hostname.includes('target.com')) return 'target';
  if (hostname.includes('uniqlo.com')) return 'uniqlo';
  if (hostname.includes('hm.com')) return 'hm';
  if (hostname.includes('zara.com')) return 'zara';
  if (hostname.includes('ae.com')) return 'ae';
  if (hostname.includes('walmart.com')) return 'walmart';

  return null;
}

/**
 * Detect if the current page is a women's product page
 */
export function isWomensProduct(): boolean {
  const url = window.location.href.toLowerCase();
  const pageText = document.body.innerText.toLowerCase();

  // Check URL patterns
  const urlPatterns = [
    '/women', '/womens', '/female', '/ladies',
    'gender=female', 'gender=women',
    '/beauty/', '/personal-care/', '/skincare/'
  ];

  if (urlPatterns.some(pattern => url.includes(pattern))) {
    return true;
  }

  // Check page content for women's product indicators
  const womenIndicators = [
    'women\'s', 'womens', 'for her', 'ladies',
    'feminine', 'venus', 'skintimate', 'secret deodorant'
  ];

  const menIndicators = [
    'men\'s', 'mens', 'for him', 'masculine'
  ];

  const womenScore = womenIndicators.filter(i => pageText.includes(i)).length;
  const menScore = menIndicators.filter(i => pageText.includes(i)).length;

  return womenScore > menScore;
}

/**
 * Detect product category
 */
export function detectCategory(): 'personal_care' | 'clothing' {
  const url = window.location.href.toLowerCase();
  const pageText = document.body.innerText.toLowerCase();

  const clothingIndicators = [
    'clothing', 'apparel', 'fashion', 'hoodie', 'shirt',
    't-shirt', 'jeans', 'pants', 'dress', 'skirt', 'jacket',
    'size chart', 'xs', 'small', 'medium', 'large'
  ];

  const personalCareIndicators = [
    'razor', 'shave', 'deodorant', 'body wash', 'soap',
    'shampoo', 'lotion', 'cream', 'beauty', 'skincare',
    'ingredients', 'blade', 'moisturizer'
  ];

  const clothingScore = clothingIndicators.filter(i =>
    url.includes(i) || pageText.includes(i)
  ).length;

  const careScore = personalCareIndicators.filter(i =>
    url.includes(i) || pageText.includes(i)
  ).length;

  return clothingScore > careScore ? 'clothing' : 'personal_care';
}

// ============================================================================
// Site-Specific Scrapers
// ============================================================================

/**
 * Target.com scraper
 */
function scrapeTarget(): ScrapedProduct | null {
  try {
    // Product title
    const titleEl = document.querySelector('[data-test="product-title"]') ||
                    document.querySelector('h1[class*="Title"]') ||
                    document.querySelector('h1');
    const title = titleEl?.textContent?.trim() || '';

    // Price
    const priceEl = document.querySelector('[data-test="product-price"]') ||
                    document.querySelector('span[data-test="current-price"]') ||
                    document.querySelector('[class*="Price"]');
    const priceText = priceEl?.textContent || '';
    const price = parseFloat(priceText.replace(/[^0-9.]/g, '')) || 0;

    // Ingredients (for personal care)
    const ingredients: string[] = [];
    const ingredientsSection = document.querySelector('[data-test="item-details-description"]');
    if (ingredientsSection) {
      const text = ingredientsSection.textContent || '';
      const match = text.match(/ingredients?:?\s*([^.]+)/i);
      if (match) {
        ingredients.push(...match[1].split(',').map(i => i.trim()));
      }
    }

    if (!title || price === 0) return null;

    return {
      title,
      price,
      category: detectCategory(),
      ingredients: ingredients.length > 0 ? ingredients : undefined,
      retailer: 'target',
      url: window.location.href
    };
  } catch (e) {
    console.error('Target scraper error:', e);
    return null;
  }
}

/**
 * Uniqlo.com scraper
 */
function scrapeUniqlo(): ScrapedProduct | null {
  try {
    const titleEl = document.querySelector('.pdp-product-name') ||
                    document.querySelector('h1[class*="product"]');
    const title = titleEl?.textContent?.trim() || '';

    const priceEl = document.querySelector('.pdp-product-price') ||
                    document.querySelector('[class*="price"]');
    const priceText = priceEl?.textContent || '';
    const price = parseFloat(priceText.replace(/[^0-9.]/g, '')) || 0;

    if (!title || price === 0) return null;

    return {
      title,
      price,
      category: 'clothing',
      retailer: 'uniqlo',
      url: window.location.href
    };
  } catch (e) {
    console.error('Uniqlo scraper error:', e);
    return null;
  }
}

/**
 * H&M scraper
 */
function scrapeHM(): ScrapedProduct | null {
  try {
    const titleEl = document.querySelector('h1.ProductName') ||
                    document.querySelector('h1[class*="product"]') ||
                    document.querySelector('h1');
    const title = titleEl?.textContent?.trim() || '';

    const priceEl = document.querySelector('.ProductPrice') ||
                    document.querySelector('[class*="price"]');
    const priceText = priceEl?.textContent || '';
    const price = parseFloat(priceText.replace(/[^0-9.]/g, '')) || 0;

    if (!title || price === 0) return null;

    return {
      title,
      price,
      category: 'clothing',
      retailer: 'hm',
      url: window.location.href
    };
  } catch (e) {
    console.error('H&M scraper error:', e);
    return null;
  }
}

/**
 * Zara.com scraper
 */
function scrapeZara(): ScrapedProduct | null {
  try {
    const titleEl = document.querySelector('h1[class*="product-name"]') ||
                    document.querySelector('h1');
    const title = titleEl?.textContent?.trim() || '';

    const priceEl = document.querySelector('[class*="price__amount"]') ||
                    document.querySelector('[class*="price"]');
    const priceText = priceEl?.textContent || '';
    const price = parseFloat(priceText.replace(/[^0-9.]/g, '')) || 0;

    if (!title || price === 0) return null;

    return {
      title,
      price,
      category: 'clothing',
      retailer: 'zara',
      url: window.location.href
    };
  } catch (e) {
    console.error('Zara scraper error:', e);
    return null;
  }
}

/**
 * American Eagle scraper
 */
function scrapeAE(): ScrapedProduct | null {
  try {
    const titleEl = document.querySelector('h1[class*="product-name"]') ||
                    document.querySelector('h1');
    const title = titleEl?.textContent?.trim() || '';

    const priceEl = document.querySelector('[class*="product-price"]') ||
                    document.querySelector('[class*="price"]');
    const priceText = priceEl?.textContent || '';
    const price = parseFloat(priceText.replace(/[^0-9.]/g, '')) || 0;

    if (!title || price === 0) return null;

    return {
      title,
      price,
      category: 'clothing',
      retailer: 'ae',
      url: window.location.href
    };
  } catch (e) {
    console.error('AE scraper error:', e);
    return null;
  }
}

/**
 * Main scrape function - routes to appropriate scraper
 */
export function scrapeProduct(): ScrapedProduct | null {
  const site = detectSite();

  if (!site) {
    console.log('PinkVanity: Unsupported site');
    return null;
  }

  console.log(`PinkVanity: Scraping ${site}...`);

  switch (site) {
    case 'target':
      return scrapeTarget();
    case 'uniqlo':
      return scrapeUniqlo();
    case 'hm':
      return scrapeHM();
    case 'zara':
      return scrapeZara();
    case 'ae':
      return scrapeAE();
    default:
      return null;
  }
}

/**
 * PinkVanity Content Script
 *
 * Runs on supported retailer websites to detect women's products
 * and show potential savings from men's alternatives.
 */

import { detectSite, isWomensProduct, scrapeProduct, detectCategory } from './scrapers';
import { showLoading, showProductMatch, showClothingMatch, showError, hideOverlay } from './overlay';
import { findProductMatch, findClothingMatch } from './api';
import type { UserMeasurements } from './types';

// Debounce timer for page changes
let debounceTimer: ReturnType<typeof setTimeout> | null = null;

/**
 * Get user measurements from storage
 */
async function getUserMeasurements(): Promise<UserMeasurements | null> {
  return new Promise((resolve) => {
    chrome.storage.sync.get(['measurements'], (result) => {
      resolve(result.measurements || null);
    });
  });
}

/**
 * Check if extension is enabled
 */
async function isEnabled(): Promise<boolean> {
  return new Promise((resolve) => {
    chrome.storage.sync.get(['enabled'], (result) => {
      resolve(result.enabled !== false); // Default to enabled
    });
  });
}

/**
 * Main function - analyze the current page
 */
async function analyzePage(): Promise<void> {
  // Check if enabled
  if (!(await isEnabled())) {
    console.log('PinkVanity: Extension disabled');
    return;
  }

  // Detect site
  const site = detectSite();
  if (!site) {
    console.log('PinkVanity: Unsupported site');
    return;
  }

  // Check if this is a women's product
  if (!isWomensProduct()) {
    console.log('PinkVanity: Not a women\'s product page');
    hideOverlay();
    return;
  }

  console.log('PinkVanity: Women\'s product detected!');

  // Scrape product info
  const product = scrapeProduct();
  if (!product) {
    console.log('PinkVanity: Could not scrape product info');
    return;
  }

  console.log('PinkVanity: Scraped product:', product);

  // Show loading state
  showLoading();

  try {
    if (product.category === 'clothing') {
      // For clothing, we need user measurements
      const measurements = await getUserMeasurements();

      if (!measurements) {
        showError('Please set your measurements in the extension options to get size recommendations.');
        return;
      }

      const result = await findClothingMatch(product.title, measurements);
      showClothingMatch(result);
    } else {
      // Personal care - just find price match
      const result = await findProductMatch(
        product.title,
        product.price,
        product.category,
        product.ingredients
      );
      showProductMatch(result);
    }
  } catch (error) {
    console.error('PinkVanity: API error', error);
    showError('Could not connect to PinkVanity. Please try again later.');
  }
}

/**
 * Debounced page analysis (for SPA navigation)
 */
function debouncedAnalyze(): void {
  if (debounceTimer) {
    clearTimeout(debounceTimer);
  }

  debounceTimer = setTimeout(() => {
    analyzePage();
  }, 1000); // Wait 1 second for page to settle
}

/**
 * Initialize the content script
 */
function init(): void {
  console.log('PinkVanity: Content script loaded');

  // Run initial analysis
  debouncedAnalyze();

  // Watch for SPA navigation (URL changes without page reload)
  let lastUrl = location.href;
  new MutationObserver(() => {
    if (location.href !== lastUrl) {
      lastUrl = location.href;
      console.log('PinkVanity: URL changed, re-analyzing...');
      debouncedAnalyze();
    }
  }).observe(document, { subtree: true, childList: true });

  // Listen for messages from popup/background
  chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
    if (message.type === 'ANALYZE_PAGE') {
      analyzePage().then(() => sendResponse({ success: true }));
      return true; // Async response
    }

    if (message.type === 'GET_PRODUCT_INFO') {
      const product = scrapeProduct();
      sendResponse({ product });
      return false;
    }
  });
}

// Start!
init();

/**
 * PinkVanity Overlay UI
 *
 * Injects a floating card into the page showing product match results.
 */

import type { MatchResponse, ClothingMatchResponse } from './types';

const OVERLAY_ID = 'pinkvanity-overlay';

/**
 * Create and inject the overlay container
 */
function createOverlay(): HTMLElement {
  // Remove existing overlay if present
  const existing = document.getElementById(OVERLAY_ID);
  if (existing) {
    existing.remove();
  }

  const overlay = document.createElement('div');
  overlay.id = OVERLAY_ID;
  overlay.innerHTML = `
    <div class="pv-card">
      <div class="pv-header">
        <span class="pv-logo">PinkVanity</span>
        <button class="pv-close" aria-label="Close">&times;</button>
      </div>
      <div class="pv-content">
        <div class="pv-loading">
          <div class="pv-spinner"></div>
          <p>Searching for savings...</p>
        </div>
      </div>
    </div>
  `;

  document.body.appendChild(overlay);

  // Add close handler
  overlay.querySelector('.pv-close')?.addEventListener('click', () => {
    overlay.classList.add('pv-hidden');
  });

  return overlay;
}

/**
 * Show loading state
 */
export function showLoading(): void {
  const overlay = createOverlay();
  overlay.classList.remove('pv-hidden');

  const content = overlay.querySelector('.pv-content');
  if (content) {
    content.innerHTML = `
      <div class="pv-loading">
        <div class="pv-spinner"></div>
        <p>Searching for savings...</p>
      </div>
    `;
  }
}

/**
 * Show product match result (Pink Tax)
 */
export function showProductMatch(result: MatchResponse): void {
  const overlay = document.getElementById(OVERLAY_ID) || createOverlay();
  overlay.classList.remove('pv-hidden');

  const content = overlay.querySelector('.pv-content');
  if (!content) return;

  if (!result.found_match) {
    content.innerHTML = `
      <div class="pv-no-match">
        <p class="pv-icon">&#128269;</p>
        <p>No cheaper men's equivalent found.</p>
        <p class="pv-subtext">This product appears to be fairly priced!</p>
      </div>
    `;
    return;
  }

  const match = result.match!;
  const savingsClass = match.savings_percent >= 30 ? 'pv-big-savings' : '';

  content.innerHTML = `
    <div class="pv-match ${savingsClass}">
      <div class="pv-savings-badge">
        Save ${match.savings_percent.toFixed(0)}%
      </div>

      <div class="pv-comparison">
        <div class="pv-original">
          <span class="pv-label">You're viewing:</span>
          <span class="pv-product-name">${result.original_product}</span>
          <span class="pv-price">$${result.original_price.toFixed(2)}</span>
        </div>

        <div class="pv-arrow">&#8594;</div>

        <div class="pv-alternative">
          <span class="pv-label">Swap to:</span>
          <span class="pv-product-name">${match.title}</span>
          <span class="pv-price pv-price-better">$${match.price.toFixed(2)}</span>
        </div>
      </div>

      <div class="pv-savings-amount">
        You save: <strong>$${match.savings_amount.toFixed(2)}</strong>
      </div>

      <div class="pv-match-reasons">
        <p class="pv-reasons-title">Why it's equivalent:</p>
        <ul>
          ${match.match_reasons.map(r => `<li>${r}</li>`).join('')}
        </ul>
      </div>

      <div class="pv-similarity">
        Similarity Score: ${(match.similarity_score * 100).toFixed(0)}%
      </div>

      <button class="pv-swap-btn">Swap & Save!</button>
    </div>
  `;

  // Add swap button handler
  content.querySelector('.pv-swap-btn')?.addEventListener('click', () => {
    // Record the savings
    chrome.runtime.sendMessage({
      type: 'RECORD_SAVINGS',
      amount: match.savings_amount,
      category: 'personal_care',
      product: match.title
    });

    // TODO: Navigate to men's product page
    alert(`Great choice! You're saving $${match.savings_amount.toFixed(2)}!`);
  });
}

/**
 * Show clothing match result (with sizing)
 */
export function showClothingMatch(result: ClothingMatchResponse): void {
  const overlay = document.getElementById(OVERLAY_ID) || createOverlay();
  overlay.classList.remove('pv-hidden');

  const content = overlay.querySelector('.pv-content');
  if (!content) return;

  if (!result.found_match) {
    content.innerHTML = `
      <div class="pv-no-match">
        <p class="pv-icon">&#128085;</p>
        <p>No men's equivalent found for this item.</p>
      </div>
    `;
    return;
  }

  const { mens_equivalent: equiv, size_recommendation: size } = result;

  content.innerHTML = `
    <div class="pv-match pv-clothing-match">
      <div class="pv-savings-badge">
        Save ${equiv.savings_percent.toFixed(0)}%
      </div>

      <div class="pv-comparison">
        <div class="pv-original">
          <span class="pv-label">You're viewing:</span>
          <span class="pv-product-name">${result.original_product}</span>
          <span class="pv-price">$${result.original_price.toFixed(2)}</span>
        </div>

        <div class="pv-arrow">&#8594;</div>

        <div class="pv-alternative">
          <span class="pv-label">Swap to:</span>
          <span class="pv-product-name">${equiv.title}</span>
          <span class="pv-price pv-price-better">$${equiv.price.toFixed(2)}</span>
        </div>
      </div>

      <div class="pv-size-recommendation">
        <div class="pv-size-badge">
          Buy Size: <strong>${size.size}</strong>
        </div>

        <div class="pv-fit-notes">
          <p class="pv-fit-title">Fit Notes:</p>
          <ul>
            ${size.fit_notes.map(note => `<li>${note}</li>`).join('')}
          </ul>
        </div>
      </div>

      <div class="pv-savings-amount">
        You save: <strong>$${equiv.savings_amount.toFixed(2)}</strong>
      </div>

      <button class="pv-swap-btn">Swap & Save!</button>
    </div>
  `;
}

/**
 * Show error state
 */
export function showError(message: string): void {
  const overlay = document.getElementById(OVERLAY_ID) || createOverlay();
  overlay.classList.remove('pv-hidden');

  const content = overlay.querySelector('.pv-content');
  if (content) {
    content.innerHTML = `
      <div class="pv-error">
        <p class="pv-icon">&#9888;</p>
        <p>${message}</p>
        <button class="pv-retry-btn">Retry</button>
      </div>
    `;
  }
}

/**
 * Hide the overlay
 */
export function hideOverlay(): void {
  const overlay = document.getElementById(OVERLAY_ID);
  if (overlay) {
    overlay.classList.add('pv-hidden');
  }
}

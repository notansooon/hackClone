/**
 * PinkVanity Popup Script
 *
 * Handles the extension popup UI - shows savings dashboard.
 */

import { getDemoResponse } from './api';

interface Stats {
  totalSaved: number;
  transactions: Array<{
    amount: number;
    category: string;
    product: string;
    timestamp: number;
  }>;
}

/**
 * Get savings stats from background
 */
async function getStats(): Promise<Stats> {
  return new Promise((resolve) => {
    chrome.runtime.sendMessage({ type: 'GET_STATS' }, (response) => {
      resolve(response || { totalSaved: 0, transactions: [] });
    });
  });
}

/**
 * Format currency
 */
function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount);
}

/**
 * Update the dashboard display
 */
async function updateDashboard(): Promise<void> {
  const stats = await getStats();

  // Update total saved
  const totalEl = document.getElementById('total-saved');
  if (totalEl) {
    totalEl.textContent = formatCurrency(stats.totalSaved);
  }

  // Update transaction count
  const countEl = document.getElementById('transaction-count');
  if (countEl) {
    countEl.textContent = `${stats.transactions.length} swaps`;
  }

  // Update recent transactions
  const listEl = document.getElementById('recent-transactions');
  if (listEl) {
    if (stats.transactions.length === 0) {
      listEl.innerHTML = `
        <div class="empty-state">
          <p>No savings yet!</p>
          <p class="hint">Browse women's products to find savings opportunities.</p>
        </div>
      `;
    } else {
      const recent = stats.transactions.slice(-5).reverse();
      listEl.innerHTML = recent.map(t => `
        <div class="transaction">
          <span class="product">${truncate(t.product, 30)}</span>
          <span class="amount">+${formatCurrency(t.amount)}</span>
        </div>
      `).join('');
    }
  }
}

/**
 * Truncate string
 */
function truncate(str: string, maxLength: number): string {
  return str.length > maxLength ? str.substring(0, maxLength) + '...' : str;
}

/**
 * Test API connection
 */
async function testApiConnection(): Promise<boolean> {
  try {
    const response = await fetch('http://localhost:8000/health');
    return response.ok;
  } catch {
    return false;
  }
}

/**
 * Initialize popup
 */
async function init(): Promise<void> {
  // Update dashboard
  await updateDashboard();

  // Check API connection
  const statusEl = document.getElementById('api-status');
  if (statusEl) {
    const connected = await testApiConnection();
    statusEl.className = `status ${connected ? 'connected' : 'disconnected'}`;
    statusEl.textContent = connected ? 'API Connected' : 'API Offline';
  }

  // Analyze current page button
  document.getElementById('analyze-btn')?.addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab.id) {
      chrome.tabs.sendMessage(tab.id, { type: 'ANALYZE_PAGE' });
    }
  });

  // Options button
  document.getElementById('options-btn')?.addEventListener('click', () => {
    chrome.runtime.openOptionsPage();
  });

  // Demo buttons (for hackathon)
  document.getElementById('demo-razor')?.addEventListener('click', async () => {
    const result = await getDemoResponse('razor');
    console.log('Demo result:', result);
    alert(`Demo: ${result.message}\nSave $${result.match.savings_amount}!`);
  });

  document.getElementById('demo-hoodie')?.addEventListener('click', async () => {
    const result = await getDemoResponse('hoodie');
    console.log('Demo result:', result);
    alert(`Demo: ${result.message}`);
  });
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', init);

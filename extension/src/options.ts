/**
 * PinkVanity Options Page Script
 *
 * Handles user preferences and measurement input.
 */

import type { UserMeasurements } from './types';

/**
 * Load saved options
 */
async function loadOptions(): Promise<void> {
  chrome.storage.sync.get(['enabled', 'apiUrl', 'measurements'], (result) => {
    // Enabled toggle
    const enabledEl = document.getElementById('enabled') as HTMLInputElement;
    if (enabledEl) {
      enabledEl.checked = result.enabled !== false;
    }

    // API URL
    const apiUrlEl = document.getElementById('api-url') as HTMLInputElement;
    if (apiUrlEl) {
      apiUrlEl.value = result.apiUrl || 'http://localhost:8000';
    }

    // Measurements
    if (result.measurements) {
      const m = result.measurements as UserMeasurements;

      const waistEl = document.getElementById('waist') as HTMLInputElement;
      if (waistEl && m.waist_inches) waistEl.value = String(m.waist_inches);

      const hipEl = document.getElementById('hip') as HTMLInputElement;
      if (hipEl && m.hip_inches) hipEl.value = String(m.hip_inches);

      const chestEl = document.getElementById('chest') as HTMLInputElement;
      if (chestEl && m.chest_inches) chestEl.value = String(m.chest_inches);

      const heightEl = document.getElementById('height') as HTMLInputElement;
      if (heightEl && m.height_inches) heightEl.value = String(m.height_inches);
    }
  });
}

/**
 * Save options
 */
function saveOptions(): void {
  const enabledEl = document.getElementById('enabled') as HTMLInputElement;
  const apiUrlEl = document.getElementById('api-url') as HTMLInputElement;
  const waistEl = document.getElementById('waist') as HTMLInputElement;
  const hipEl = document.getElementById('hip') as HTMLInputElement;
  const chestEl = document.getElementById('chest') as HTMLInputElement;
  const heightEl = document.getElementById('height') as HTMLInputElement;

  const measurements: UserMeasurements = {
    waist_inches: parseFloat(waistEl?.value) || 0,
    hip_inches: parseFloat(hipEl?.value) || 0,
    chest_inches: parseFloat(chestEl?.value) || undefined,
    height_inches: parseFloat(heightEl?.value) || undefined
  };

  chrome.storage.sync.set({
    enabled: enabledEl?.checked ?? true,
    apiUrl: apiUrlEl?.value || 'http://localhost:8000',
    measurements: measurements.waist_inches > 0 ? measurements : undefined
  }, () => {
    showStatus('Settings saved!', 'success');
  });
}

/**
 * Show status message
 */
function showStatus(message: string, type: 'success' | 'error'): void {
  const statusEl = document.getElementById('status');
  if (statusEl) {
    statusEl.textContent = message;
    statusEl.className = `status ${type}`;
    statusEl.style.display = 'block';

    setTimeout(() => {
      statusEl.style.display = 'none';
    }, 3000);
  }
}

/**
 * Test API connection
 */
async function testConnection(): Promise<void> {
  const apiUrlEl = document.getElementById('api-url') as HTMLInputElement;
  const url = apiUrlEl?.value || 'http://localhost:8000';

  try {
    const response = await fetch(`${url}/health`);
    if (response.ok) {
      const data = await response.json();
      showStatus(`Connected! ${data.womens_products_loaded} products loaded.`, 'success');
    } else {
      showStatus('API returned an error', 'error');
    }
  } catch (error) {
    showStatus('Could not connect to API', 'error');
  }
}

/**
 * Clear all data
 */
function clearData(): void {
  if (confirm('Are you sure you want to clear all PinkVanity data? This cannot be undone.')) {
    chrome.storage.sync.clear();
    chrome.storage.local.clear();
    showStatus('All data cleared', 'success');
    loadOptions(); // Reload defaults
  }
}

/**
 * Initialize options page
 */
function init(): void {
  // Load saved options
  loadOptions();

  // Save button
  document.getElementById('save-btn')?.addEventListener('click', saveOptions);

  // Test connection button
  document.getElementById('test-btn')?.addEventListener('click', testConnection);

  // Clear data button
  document.getElementById('clear-btn')?.addEventListener('click', clearData);

  // Auto-save on input change (for enabled toggle)
  document.getElementById('enabled')?.addEventListener('change', saveOptions);
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', init);

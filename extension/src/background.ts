/**
 * PinkVanity Background Service Worker
 *
 * Handles cross-tab communication, storage, and badge updates.
 */

// Generate unique user ID for savings tracking
async function getUserId(): Promise<string> {
  return new Promise((resolve) => {
    chrome.storage.sync.get(['userId'], (result) => {
      if (result.userId) {
        resolve(result.userId);
      } else {
        const newId = 'pv_' + Math.random().toString(36).substring(2, 15);
        chrome.storage.sync.set({ userId: newId });
        resolve(newId);
      }
    });
  });
}

// Update extension badge with savings info
async function updateBadge(): Promise<void> {
  const { totalSaved } = await chrome.storage.local.get(['totalSaved']);

  if (totalSaved && totalSaved > 0) {
    chrome.action.setBadgeText({ text: `$${Math.floor(totalSaved)}` });
    chrome.action.setBadgeBackgroundColor({ color: '#e91e8c' });
  } else {
    chrome.action.setBadgeText({ text: '' });
  }
}

// Listen for messages from content scripts and popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'RECORD_SAVINGS') {
    // Record a new savings transaction
    chrome.storage.local.get(['totalSaved', 'transactions'], (result) => {
      const totalSaved = (result.totalSaved || 0) + message.amount;
      const transactions = result.transactions || [];

      transactions.push({
        amount: message.amount,
        category: message.category,
        product: message.product,
        timestamp: Date.now()
      });

      chrome.storage.local.set({
        totalSaved,
        transactions
      }, () => {
        updateBadge();
        sendResponse({ success: true, totalSaved });
      });
    });

    return true; // Async response
  }

  if (message.type === 'GET_STATS') {
    chrome.storage.local.get(['totalSaved', 'transactions'], (result) => {
      sendResponse({
        totalSaved: result.totalSaved || 0,
        transactions: result.transactions || []
      });
    });

    return true;
  }

  if (message.type === 'GET_USER_ID') {
    getUserId().then(userId => sendResponse({ userId }));
    return true;
  }
});

// Update badge on startup
updateBadge();

// Log installation
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('PinkVanity installed!');

    // Set default options
    chrome.storage.sync.set({
      enabled: true,
      apiUrl: 'http://localhost:8000'
    });

    // Open options page for initial setup
    chrome.runtime.openOptionsPage();
  }
});

console.log('PinkVanity background service worker started');

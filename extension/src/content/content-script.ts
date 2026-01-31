import { getSupportedSiteFromLocation } from './sites';
import { mountWidget } from './widget/mount-widget';

async function main(): Promise<void> {
  const supportedSite = getSupportedSiteFromLocation(window.location);
  if (!supportedSite) return;

  // Avoid double-inject during SPA navigations.
  if (document.getElementById('pinkvanity-root')) return;

  await mountWidget(supportedSite);
}

void main();


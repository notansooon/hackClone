# PinkVanity
Shopping app for women!

## Chrome extension (hackathon MVP)

Targets:
- American Eagle (`www.ae.com`)
- ZARA (`www.zara.com`)
- H&M (`www2.hm.com`)

### Build

```bash
npm install
npm run build
```

### Dev (auto rebuild on save)

```bash
npm run dev
```

Then:
- `chrome://extensions` → your extension → **Reload**
- Refresh the shopping tab to re-inject the content script

### Load in Chrome

- Open `chrome://extensions`
- Enable **Developer mode**
- Click **Load unpacked**
- Select the `extension/` folder

### Quick test

- Visit a product page on American Eagle / ZARA / H&M
- You should see a small **PinkVanity (MVP)** overlay in the top-right
- Click **Options** to set measurements (stored locally)

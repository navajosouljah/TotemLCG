# Totem Vendor Financing Explainer Video

A ~71 second motion graphics explainer built with Remotion. It tells the origin story of a Totem transaction:

1. Disclaimer open (required, 6 seconds on screen)
2. Amazon submits a legally contracted purchase order to a vendor
3. The vendor's capital is already deployed across multiple active purchase orders and he cannot fund the new one
4. He messages Totem, which is where the business begins
5. Totem members fund the purchase order of necessity
6. Member terms: fixed 5% origination fee, 90 day cycle, insurance structured into the transaction with an A-rated global carrier, no separate personal policy
7. Close with the Totem wordmark and the general disclaimer

## This folder is isolated from the site

The site itself (`index.html` at the repo root) remains a zero dependency static file. This folder has its own `package.json` and is never deployed by Vercel; nothing at the repo root references it. Do not move a build step to the root.

## Rendering

```
cd video
npm install
npm run render
```

Output lands at `video/out/totem-vendor-financing.mp4` (1920x1080, 30 fps). The Remotion config points at the container's pre-installed Chromium; on a normal machine, delete the `setBrowserExecutable` line in `remotion.config.ts` and Remotion will provision its own headless browser.

## Compliance

See `COMPLIANCE.md`. The copy in the video already passed the Totem compliance screen with rewrites applied, but the video scores Red (it contains a fee percentage and insurance references) and requires Legal Counsel review before public release.

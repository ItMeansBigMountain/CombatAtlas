# Unified Commerce Launch Plan

- **Project:** TikTok Shop / Shopify Commerce
- **Created:** 2026-05-03
- **Runner:** Heartbeat
- **Goal:** Build a simple, staged commerce operating foundation across Shopify, TikTok Shop, Instagram Shop, POD, stocked products, affiliate promotion, SPO, election/seasonal products, experimental products, and dropshipping tests.

## Current source checks

Official/current setup notes used for this plan:

- Shopify TikTok Shop docs: TikTok Shop can sync catalog, inventory, fulfillment, and orders between Shopify and TikTok Shop. Shopify lists store requirements including a verifiable location address, supported country, online store, and TikTok for Business account. Source: https://help.shopify.com/en/manual/online-sales-channels/tiktok/setup
- Shopify Facebook and Instagram by Meta docs: Meta channel syncs products to Facebook/Instagram catalog and supports Facebook Shop, Instagram Shopping, and Meta marketing. Source: https://help.shopify.com/en/manual/online-sales-channels/facebook-instagram-by-meta
- Shopify Meta requirements docs: Shopify store must not be password-protected; sender email must be valid; business needs Facebook Page, business portfolio, proper permissions, and Meta commerce eligibility. Source: https://help.shopify.com/en/manual/online-sales-channels/facebook-instagram-by-meta/requirements-and-considerations
- Instagram Help / Commerce Manager: shops are created/managed through Commerce Manager; Instagram visibility needs an Instagram business account in the business portfolio. Source: https://www.facebook.com/help/instagram/1187859655048322/

## Launch sequence

| Phase | Track | Purpose | Output | Approval-sensitive? |
|---|---|---|---|---|
| 0 | Foundation | Define brand, products, fulfillment rules, policies, tax/shipping assumptions | Store launch checklist + product shortlist | Yes for business/tax/legal decisions |
| 1 | Shopify Core | Make Shopify the source of truth for products, inventory, orders, and checkout | Working Shopify catalog and policies | Yes for store billing, domain, payments |
| 2 | POD Track | Launch low-risk print-on-demand items first | 3-5 POD SKUs with mockups and pricing | Yes for provider connection/payment |
| 3 | Stock/Fulfillment Track | Add any physical inventory only after POD flow is clear | Stock SKU sheet, COGS, reorder rules | Yes for purchasing inventory |
| 4 | TikTok Shop | Connect TikTok sales channel and test product sync | TikTok Shop channel connected, 1-3 eligible SKUs synced | Yes for TikTok account connection and public shop setup |
| 5 | Instagram/Facebook Shop | Connect Meta channel and catalog | Meta catalog synced, Instagram Shop review started | Yes for Facebook/Instagram login and publishing |
| 6 | Content + Affiliate | Promote with short-form content and affiliate links | Weekly content calendar + affiliate disclosure pattern | Yes for public posting and affiliate terms |
| 7 | SPO / Offer Experiments | Test special product offers/bundles | 2 offer concepts with margins and landing-page copy | Yes before public launch |
| 8 | Election/Seasonal Products | Keep separate because policy/reputational risk is higher | Compliance-reviewed seasonal product shortlist | Yes; manual review required before publishing |
| 9 | Dropshipping Tests | Only test after core store is stable | 1-2 supplier/product experiments with risk score | Yes for supplier/payment/app installs |

## Track separation

### Sales channels

1. **Shopify Online Store**
   - Role: system of record and checkout hub.
   - First validation: one product can be created, priced, categorized, and purchased/test-checked without public launch surprises.

2. **TikTok Shop**
   - Role: discovery + native shopping.
   - Dependencies: Shopify online store, verifiable location, TikTok for Business, eligible country/product catalog.
   - Manual steps: TikTok account auth, merchant terms, verification, public shop settings.

3. **Instagram/Facebook Shop**
   - Role: social catalog + profile shopping.
   - Dependencies: Shopify store not password-protected, valid sender email, Facebook account/Page, business portfolio, Instagram professional account, verified domain/direct purchase eligibility.
   - Manual steps: Meta login, business asset permissions, shop publishing/review.

### Product tracks

1. **POD first**
   - Lowest inventory risk.
   - Good for testing martial arts, coding, ninja-clan, motivational, or meme-style designs.

2. **Stock/fulfillment second**
   - Only after the store flow works.
   - Requires COGS, shipping material, return policy, inventory risk, and reorder rule.

3. **Experimental products**
   - Keep in a separate testing lane.
   - Use clear success criteria: clicks, add-to-cart, sales, margin, content response.

4. **Election/seasonal products**
   - Treat as high-sensitivity.
   - Require manual review for platform policy, public optics, and product claims before publishing.

5. **Dropshipping**
   - Last, not first.
   - High customer-experience risk; validate supplier speed, product quality, return handling, and refund path before public push.

### Promotion tracks

1. **Organic short-form content**
   - Reusable scripts, product demos, behind-the-scenes, coding/martial arts angle.

2. **Affiliate**
   - Keep disclosure language ready.
   - Track links separately from owned products.

3. **Paid ads**
   - Do not start until store, product page, tax/shipping, and fulfillment are clean.

## Approval-sensitive actions

Do not automate without Affan approval:

- Shopify billing/plan/domain/payment changes
- TikTok/Meta account login and authorization
- Public product publishing
- Public posts or ads
- Inventory purchases
- Dropshipping supplier contracts/apps
- Tax/legal policy decisions
- Election or political product launch
- Any secret/API/auth configuration

## First 3 actionable tasks

1. **Create product shortlist**
   - Output: `PRODUCT_SHORTLIST.md`
   - Include: product name, track, target buyer, estimated price, fulfillment method, risk, first content angle.

2. **Draft POD-first SKU plan**
   - Output: `POD_SKU_PLAN.md`
   - Include: 3-5 designs, mockup needs, product type, pricing hypothesis, margin assumptions.

3. **Create channel readiness checklist**
   - Output: `CHANNEL_READINESS_CHECKLIST.md`
   - Include: Shopify, TikTok Shop, Instagram/Facebook Shop, manual auth steps, required assets, blockers.

## Recommended next slice

Build `PRODUCT_SHORTLIST.md` first. It keeps the work concrete without requiring account access, spending, public posting, or platform configuration.

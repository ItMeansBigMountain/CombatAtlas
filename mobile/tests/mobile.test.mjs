import test from 'node:test';
import assert from 'node:assert/strict';
import { AD_POLICY, canShowInterstitial, createBillingBoundary, developmentAdAdapter } from '../src/monetization.js';
import { martialArts, drills, searchAll } from '../src/data/combatData.js';

test('mobile build preserves the full atlas', () => {
  assert.equal(martialArts.length, 22);
  assert.equal(drills.length, 882);
  assert.ok(searchAll('armbar').drills.length > 0);
});

test('ads require consent and respect remove-ads entitlement', () => {
  const session = { interstitialCount: 0, actionsSinceInterstitial: AD_POLICY.minActionsBetweenInterstitials, lastInterstitialAt: 0 };
  assert.equal(canShowInterstitial({ preferences: { consent: 'unset', removeAds: false }, session }), false);
  assert.equal(canShowInterstitial({ preferences: { consent: 'accepted', removeAds: true }, session }), false);
  assert.equal(canShowInterstitial({ preferences: { consent: 'accepted', removeAds: false }, session }), true);
});

test('frequency caps block excessive interstitials', () => {
  const session = { interstitialCount: AD_POLICY.maxInterstitialsPerSession, actionsSinceInterstitial: 999, lastInterstitialAt: 0 };
  assert.equal(canShowInterstitial({ preferences: { consent: 'accepted', removeAds: false }, session }), false);
});

test('billing boundary trusts only verified matching purchases and restoration', async () => {
  const billing = createBillingBoundary({
    purchase: async () => ({ verified: true, productId: 'combatatlas_remove_ads' }),
    restore: async () => [{ verified: true, productId: 'combatatlas_remove_ads' }],
  });
  assert.equal(await billing.purchaseRemoveAds(), true);
  assert.equal(await billing.restoreRemoveAds(), true);
});

test('development adapter uses test identifiers only', () => {
  assert.equal(developmentAdAdapter.mode, 'test');
  assert.match(developmentAdAdapter.bannerUnitId, /^test-/);
  assert.match(developmentAdAdapter.interstitialUnitId, /^test-/);
});

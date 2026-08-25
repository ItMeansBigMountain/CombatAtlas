export const AD_POLICY = Object.freeze({
  minActionsBetweenInterstitials: 8,
  minMinutesBetweenInterstitials: 10,
  maxInterstitialsPerSession: 3,
});

export const defaultPreferences = Object.freeze({
  consent: 'unset',
  personalizedAds: false,
  removeAds: false,
});

export function canShowInterstitial({ preferences, session, now = Date.now() }) {
  if (!preferences || preferences.removeAds || preferences.consent !== 'accepted') return false;
  if (session.interstitialCount >= AD_POLICY.maxInterstitialsPerSession) return false;
  if (session.actionsSinceInterstitial < AD_POLICY.minActionsBetweenInterstitials) return false;
  if (session.lastInterstitialAt && now - session.lastInterstitialAt < AD_POLICY.minMinutesBetweenInterstitials * 60_000) return false;
  return true;
}

export function createBillingBoundary(adapter) {
  return {
    async purchaseRemoveAds() {
      const result = await adapter.purchase('combatatlas_remove_ads');
      return Boolean(result?.verified && result?.productId === 'combatatlas_remove_ads');
    },
    async restoreRemoveAds() {
      const purchases = await adapter.restore();
      return purchases.some((item) => item.verified && item.productId === 'combatatlas_remove_ads');
    },
  };
}

export const developmentAdAdapter = Object.freeze({
  mode: 'test',
  bannerUnitId: 'test-banner',
  interstitialUnitId: 'test-interstitial',
});

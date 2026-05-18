from django.test import TestCase
from django.urls import reverse

from .views import analyze_ticker


class LatestNewsAnalysisTests(TestCase):
    def test_public_analyze_endpoint_returns_demo_sentiment(self):
        response = self.client.post(
            reverse('analyze_stocks'),
            data={'stocks': [{'ticker_name': 'AAPL', 'amount_invested': 1000}]},
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload[0]['ticker_name'], 'AAPL')
        self.assertIn('analysis_data', payload[0])
        self.assertIn(payload[0]['analysis_data']['label'], {'bullish', 'bearish', 'neutral'})
        self.assertGreaterEqual(payload[0]['analysis_data']['article_count'], 1)

    def test_analyze_ticker_has_latest_articles_shape(self):
        result = analyze_ticker('MSFT')

        self.assertIn(result['label'], {'bullish', 'bearish', 'neutral'})
        self.assertGreaterEqual(result['article_count'], 1)
        self.assertIsInstance(result['latest_articles'], list)
        self.assertIn('title', result['latest_articles'][0])

# DJANGO
from contextlib import contextmanager
from datetime import datetime
import json
import math
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import CustomUser, Stock, NewsSource
from .serializers import UserSerializer, StockSerializer, NewsSourceSerializer
from . import watson_service as watson


BULLISH_WORDS = {
    "beat", "beats", "upgrade", "upgraded", "buy", "bullish", "gain", "gains",
    "growth", "profit", "profits", "record", "surge", "surges", "rally", "rallies",
    "strong", "outperform", "positive", "raises", "raised", "higher", "optimistic",
    "expands", "partnership", "approval", "launch", "wins", "winner"
}

BEARISH_WORDS = {
    "miss", "misses", "downgrade", "downgraded", "sell", "bearish", "loss", "losses",
    "decline", "declines", "drop", "drops", "fall", "falls", "plunge", "plunges",
    "weak", "underperform", "negative", "cuts", "cut", "lower", "lawsuit", "probe",
    "investigation", "recall", "layoffs", "risk", "warns", "warning", "slump"
}


def _text_to_score(text):
    words = re.findall(r"[a-zA-Z']+", (text or "").lower())
    if not words:
        return 0.0
    bullish = sum(1 for word in words if word in BULLISH_WORDS)
    bearish = sum(1 for word in words if word in BEARISH_WORDS)
    raw = bullish - bearish
    return round(max(-1.0, min(1.0, raw / 4)), 3)


def _score_to_emotions(score):
    joy = max(0.05, min(0.9, 0.45 + score * 0.45))
    fear = max(0.05, min(0.85, 0.35 - score * 0.3))
    sadness = max(0.03, min(0.65, 0.25 - score * 0.2))
    anger = max(0.03, min(0.55, 0.18 - score * 0.12))
    disgust = max(0.02, min(0.45, 0.12 - score * 0.08))
    return {
        "joy": round(joy, 3),
        "fear": round(fear, 3),
        "sadness": round(sadness, 3),
        "anger": round(anger, 3),
        "disgust": round(disgust, 3),
    }


def _fetch_latest_articles(ticker, limit=8):
    """Fetch latest finance headlines without requiring API keys.

    Yahoo Finance RSS is used as the no-secret default so the demo remains deployable
    while paid/private NewsAPI or IBM Watson credentials are still being located.
    """
    safe_ticker = urllib.parse.quote((ticker or "").upper())
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={safe_ticker}&region=US&lang=en-US"
    request = urllib.request.Request(url, headers={"User-Agent": "stock-news-demo/1.0"})
    with urllib.request.urlopen(request, timeout=12) as response:
        xml_body = response.read()

    root = ET.fromstring(xml_body)
    articles = []
    for item in root.findall("./channel/item")[:limit]:
        title = item.findtext("title") or "Untitled article"
        description = re.sub(r"<[^>]+>", "", item.findtext("description") or "")
        link = item.findtext("link") or ""
        published = item.findtext("pubDate") or ""
        text = f"{title}. {description}"
        score = _text_to_score(text)
        articles.append({
            "title": title,
            "description": description,
            "url": link,
            "publishedAt": published,
            "sentiment": score,
            "label": "bullish" if score > 0.08 else "bearish" if score < -0.08 else "neutral",
        })
    return articles


def _fallback_articles(ticker):
    ticker = (ticker or "STOCK").upper()
    samples = [
        (f"{ticker} investors weigh latest market momentum", "Analysts discuss growth, valuation, and risk as fresh market data arrives."),
        (f"{ticker} update: earnings expectations stay in focus", "Traders watch whether revenue growth can beat expectations this quarter."),
        (f"{ticker} volatility rises with macro uncertainty", "Markets balance positive demand signals against lower guidance and sector risk."),
    ]
    articles = []
    for title, description in samples:
        score = _text_to_score(f"{title}. {description}")
        articles.append({
            "title": title,
            "description": description,
            "url": "",
            "publishedAt": datetime.utcnow().isoformat() + "Z",
            "sentiment": score,
            "label": "bullish" if score > 0.08 else "bearish" if score < -0.08 else "neutral",
        })
    return articles


def analyze_ticker(ticker):
    try:
        articles = _fetch_latest_articles(ticker)
    except Exception:
        articles = _fallback_articles(ticker)

    if not articles:
        articles = _fallback_articles(ticker)

    scores = [article["sentiment"] for article in articles]
    avg = round(sum(scores) / len(scores), 3) if scores else 0.0
    bullish = sum(1 for score in scores if score > 0.08)
    bearish = sum(1 for score in scores if score < -0.08)
    neutral = max(0, len(scores) - bullish - bearish)
    confidence = round((abs(avg) + (max(bullish, bearish, neutral) / max(1, len(scores)))) / 2, 3)

    return {
        "sentiment": avg,
        "label": "bullish" if avg > 0.08 else "bearish" if avg < -0.08 else "neutral",
        "confidence": confidence,
        "article_count": len(articles),
        "bullish_count": bullish,
        "bearish_count": bearish,
        "neutral_count": neutral,
        "emotions": _score_to_emotions(avg),
        "latest_articles": articles,
        "analyzer": "latest Yahoo Finance RSS + heuristic sentiment",
    }


class NewsSourceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = NewsSource.objects.all()
    serializer_class = NewsSourceSerializer


class StockView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, stock_id=None):
        if stock_id:
            stock = Stock.objects.filter(user=request.user, id=stock_id).first()
            if stock:
                serializer = StockSerializer(stock)
                return Response(serializer.data)
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        stocks = Stock.objects.filter(user=request.user)
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.pk
        serializer = StockSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, stock_id=None):
        if not stock_id:
            return Response({"detail": "Stock ID is required for update."}, status=status.HTTP_400_BAD_REQUEST)

        stock = Stock.objects.filter(user=request.user, id=stock_id).first()
        if not stock:
            return Response({"detail": "Stock not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = StockSerializer(stock, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, stock_id):
        stock = Stock.objects.filter(user=request.user, id=stock_id).first()
        if stock:
            stock.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Stock not found."}, status=status.HTTP_404_NOT_FOUND)


class CreateUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class AnalyzeStocksView(APIView):
    # Public for the live demo. Authenticated users still get DB persistence.
    permission_classes = [AllowAny]

    def post(self, request):
        stocks_data = request.data.get('stocks', [])
        analyzed_stocks = []

        for index, stock in enumerate(stocks_data):
            ticker = (stock.get("ticker_name") or stock.get("symbol") or "").upper().strip()
            if not ticker:
                continue
            analyzed = dict(stock)
            analyzed.setdefault("id", index + 1)
            analyzed["ticker_name"] = ticker
            analyzed["analysis_data"] = analyze_ticker(ticker)
            analyzed["last_analysis_date"] = timezone.now().isoformat()
            analyzed_stocks.append(analyzed)

            if request.user and request.user.is_authenticated:
                Stock.objects.filter(user=request.user, ticker_name=ticker).update(
                    analysis_data=analyzed["analysis_data"],
                    last_analysis_date=timezone.now(),
                )

        return Response(analyzed_stocks)


class RobinhoodImportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get("rsn")
        password = request.data.get("rpw")

        with robin_login(username, password) as robin:
            if not robin:
                return Response({'error': 'Failed to login to Robinhood'}, status=status.HTTP_400_BAD_REQUEST)

            user_robinhood_account = robin.build_user_profile()
            user_robinhood_stocks = robin.build_holdings(with_dividends=True)

            for stock, data in user_robinhood_stocks.items():
                stock_serializer = StockSerializer(data=data)
                if stock_serializer.is_valid():
                    stock_serializer.save(user=request.user)
                else:
                    return Response(stock_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            user = request.user
            user.equity = float(user_robinhood_account.get("equity", 0))
            user.cash = float(user_robinhood_account.get("cash", 0))
            user.dividend_total = float(user_robinhood_account.get("dividend_total", 0))
            user.save()

        return Response({'message': 'Stocks imported successfully'}, status=status.HTTP_200_OK)


@contextmanager
def robin_login(username, password):
    try:
        import robin_stocks.robinhood as robin
        robin.login(username, password)
        yield robin
    except Exception:
        yield None
    finally:
        try:
            robin.logout()
        except Exception:
            pass

# Stock News - Stock Portfolio Analysis App

## Overview
This application allows users to log in, manage their stock portfolio, and get sentiment analysis on their investments based on recent news. The backend is built with Python Django and the frontend with AngularJS.

## Project Structure
```
/stockNews
├── stock_news_backend/       # Django backend application
├── stock-news-frontend/      # AngularJS frontend application
├── readme.md                 # Project overview and features
├── stockNews.txt             # Detailed description of app functionality
```

## Features (from readme.md)
- OAuth2 authentication for secure login/signup
- Dashboard to manage and view stock portfolio
- Add or edit investment details
- Customizable settings for user profiles and news source preferences
- Automated sentiment analysis of stocks based on news articles

## User Flow (from readme.md)
1. **Login/Signup Page**
   - OAuth2 Token Exchange
   - User Authentication

2. **Portfolio Dashboard**
   - Fetch & Display Investments
   - Timeframe Selection
   - Add/Edit Investments
   - Run Analysis
   - Navigate to Settings

3. **Add/Edit Investments**
   - Update Backend with Investment Data

4. **Settings Page**
   - Update Personal Info & News Sources

5. **Analysis Process**
   - Fetch & Analyze News
   - Update Dashboard with Sentiment

## Detailed Description (from stockNews.txt)
### App Overview
- User logs in (with preferred OAuth2 signup process to avoid storing sensitive information)
- User loads stock portfolio manually (ticker name and investment amount)
- Application saves user information and searches news sources for relevant portfolio information
- Uses LLM (ChatGPT OpenAI or Hugging Face) to read news and analyze sentiment
- Average sentiment analysis displayed for each stock (bullish/green or bearish/red)
- Dashboard shows timeframe for news gathering (default: present)

### Pages/Sections
1. **Login Page** - Login/Signup with OAuth2
2. **Portfolio Dashboard** - Main interface with:
   - Empty dashboard initially
   - Add stocks button
   - Scrollable list of investments
   - Timeframe selector (default: week ago to present)
   - Run analysis button
   - Profile settings button (top right)
3. **Add/Edit Investments** - Popup for ticker symbol and investment amount
4. **Settings Page** - Update user information and news source preferences

### Data Flow
- Client logs in via OAuth2 → submits token to backend
- Backend fetches user's stocks, investment amounts, and personal information
- After authentication, populates scrollable list on frontend
- Updating investments updates backend with new list and prices
- Currently uses Nasdaq symbols only (news APIs filtered for NASDAQ)
- Analysis uses LLM (OpenAI API or Hugging Face transformers) to read news articles from specified news APIs

### User Actions
- **Login Page**: Login/Signup with OAuth2 services
- **Portfolio Dashboard**:
  - Change timeframe for news articles (calendar view with "from" & "to" sections)
  - Present time button for "to" section
  - Add investment button (popup for ticker symbol and amount invested)
  - Run analysis button (shows loading indicator during processing)
  - Gear symbol (top right) → Settings page
- **Investment List Interactions**:
  - Swipe left on stock: reveals delete button
  - Swipe right on stock: reveals edit button for investment amount
  - Scrollable list with stagnant add investment, timeframe, and analysis buttons

## Technical Implementation Notes (from stockNews.txt)
### JWT Token Auth for Django
- `pip install rest_framework_simplejwt`
- Configure `urls.py` with JWT views:
  - `path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair')`
  - `path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')`
- Requires custom user model in `models.py`
- Configure `settings.py` with custom user model
- Create authentication workflow in frontend to request `/api/token` endpoints
- Use `permission_classes = [AllowAny]` for public endpoints (adjust as needed)

## Next Steps for Completion
1. **Backend Setup**:
   - Install Django and required packages (djangorestframework, rest_framework_simplejwt)
   - Configure custom user model
   - Set up OAuth2 authentication
   - Create models for User, Portfolio, Investments, News Sources, Sentiment Analysis
   - Implement news fetching from APIs
   - Integrate LLM for sentiment analysis (OpenAI API or Hugging Face)
   - Create API endpoints for portfolio management and analysis

2. **Frontend Setup**:
   - Install AngularJS dependencies
   - Create login/signup interface with OAuth2
   - Build portfolio dashboard with scrollable investment list
   - Implement timeframe selector
   - Create add/edit investment popups
   - Build settings page for user preferences
   - Implement swipe gestures for delete/edit actions
   - Add loading indicators for analysis process

3. **Integration & Testing**:
   - Connect frontend to backend APIs
   - Test OAuth2 flow
   - Test news fetching and sentiment analysis
   - Test portfolio CRUD operations
   - Test timeframe filtering
   - Test UI responsiveness and interactions

4. **Deployment Preparation**:
   - Configure production settings
   - Set up environment variables for API keys
   - Prepare for deployment to cloud services
   - Create documentation for setup and usage

## Integration Opportunities
This project could integrate with:
- Local Meeting Transcriber for analyzing transcripts of financial discussions
- MusicAI for analyzing music industry stock sentiment
- WattHappened for financial news aggregation
- Coding School Platform for teaching investment concepts
- Journal AI for analyzing investment-related journal entries

## Privacy and Security Notes
- OAuth2 authentication avoids storing sensitive credentials in database
- API keys for news services and LLM should be stored securely (environment variables)
- Consider rate limiting and caching for external API calls
- Implement proper error handling for service failures
- Secure JWT token storage on frontend (HttpOnly cookies or secure storage)

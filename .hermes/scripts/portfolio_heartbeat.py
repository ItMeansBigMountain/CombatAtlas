#!/usr/bin/env python3
"""
Portfolio Heartbeat for Morning Report
Fetches all Robinhood accounts, positions, 24h P&L, and news for owned symbols.
"""

import sys
import json
from pathlib import Path

# Use hermes-agent to path for MCP tools
sys.path.insert(0, '/opt/data/hermes-agent')

from tools.mcp_tool import McpToolClient


def call_mcp_tool(tool_name, **kwargs):
    """Call MCP tool using the McpToolClient."""
    client = McpToolClient()
    return client.call_tool(tool_name, **kwargs)


def get_all_accounts():
    """Get all Robinhood accounts."""
    try:
        result = call_mcp_tool("robinhood_trading:get_accounts")
        return result
    except Exception as e:
        return {"error": str(e)}


def get_account_portfolio(account_number):
    """Get portfolio for an account."""
    try:
        result = call_mcp_tool("robinhood_trading:get_portfolio", account_number=account_number)
        return result
    except Exception as e:
        return {"error": str(e)}


def get_account_positions(account_number):
    """Get equity positions for an account."""
    try:
        result = call_mcp_tool("robinhood_trading:get_equity_positions", account_number=account_number, nonzero=True)
        return result
    except Exception as e:
        return {"error": str(e)}


def get_quotes(symbols):
    """Get current quotes for symbols."""
    try:
        result = call_mcp_tool("robinhood_trading:get_equity_quotes", symbols=symbols)
        return result
    except Exception as e:
        return {"error": str(e)}


def get_historicals(symbols, start_time, end_time):
    """Get historical data for P&L calculation."""
    try:
        result = call_mcp_tool("robinhood_trading:get_equity_historicals", 
            symbols=symbols, 
            start_time=start_time, 
            end_time=end_time, 
            interval="day",
            bounds="regular",
            adjustment_type="split"
        )
        return result
    except Exception as e:
        return {"error": str(e)}


def calculate_24h_change(symbol, current_price, historical_data):
    """Calculate 24h change from historical data."""
    try:
        if symbol in historical_data.get('results', {}):
            candles = historical_data['results'][symbol].get('candles', [])
            if len(candles) >= 2:
                yesterday_close = float(candles[-2].get('close_price', 0))
                current = float(current_price)
                change_pct = ((current - yesterday_close) / yesterday_close) * 100
                change_dollar = current - yesterday_close
                return change_pct, change_dollar
    except Exception:
        pass
    return None, None


def format_account_heartbeat(account, portfolio, positions, quotes, news):
    """Format a single account's heartbeat."""
    lines = []
    
    account_id = account.get('account_number', 'unknown')
    display_name = f"...{account_id[-4:]}" if len(account_id) >= 4 else account_id
    
    # Account value and P&L
    total_value = float(portfolio.get('total_value', 0))
    cash = float(portfolio.get('cash', 0))
    buying_power = float(portfolio.get('buying_power', {}).get('buying_power', 0))
    
    lines.append(f"**Account {display_name}**")
    lines.append(f"  Value: ${total_value:,.2f} | Cash: ${cash:,.2f} | BP: ${buying_power:,.2f}")
    
    # Positions
    positions_list = positions.get('positions', [])
    if positions_list:
        for pos in positions_list:
            symbol = pos.get('symbol', '')
            qty = float(pos.get('quantity', 0))
            avg_cost = float(pos.get('average_buy_price', 0))
            
            # Get quote for this symbol
            quote_data = {}
            for r in quotes.get('results', []):
                if r.get('quote', {}).get('symbol') == symbol:
                    quote_data = r.get('quote', {})
                    break
            
            current_price = float(quote_data.get('last_trade_price', 0))
            
            # Calculate current value and P&L
            current_value = qty * current_price
            cost_basis = qty * avg_cost
            unrealized_pl = current_value - cost_basis
            unrealized_pct = (unrealized_pl / cost_basis * 100) if cost_basis > 0 else 0
            
            pl_sign = "+" if unrealized_pl >= 0 else ""
            lines.append(f"  {symbol}: {qty:.6f} @ ${avg_cost:.2f} → ${current_price:.2f} | P&L: {pl_sign}${unrealized_pl:.2f} ({pl_sign}{unrealized_pct:.2f}%)")
            
            # News
            if symbol in news and news[symbol]:
                for n in news[symbol][:1]:
                    title = n.get('title', '')
                    if len(title) > 80:
                        title = title[:80] + "..."
                    lines.append(f"    News: {title}")
    
    return lines


def main():
    """Main entry point."""
    print("🔍 Fetching Robinhood portfolio heartbeat...")
    
    # Get all accounts
    accounts_data = get_all_accounts()
    accounts = accounts_data if isinstance(accounts_data, list) else []
    
    if not accounts:
        print("No accounts found or error fetching accounts")
        print(f"Error: {accounts_data}")
        return
    
    all_symbols = set()
    account_data = {}
    
    # Collect data for each account
    for account in accounts:
        acc_num = account.get('account_number')
        if not acc_num:
            continue
            
        portfolio = get_account_portfolio(acc_num)
        positions = get_account_positions(acc_num)
        
        # Collect symbols
        for pos in positions.get('positions', []):
            all_symbols.add(pos.get('symbol'))
        
        account_data[acc_num] = {
            'account': account,
            'portfolio': portfolio,
            'positions': positions
        }
    
    # Fetch quotes for all symbols
    symbols_list = list(all_symbols)
    quotes = get_quotes(symbols_list) if symbols_list else {}
    
    # Fetch news for owned symbols
    news = {}
    try:
        from hermes_tools import web_search
        for symbol in symbols_list:
            try:
                results = web_search(query=f"{symbol} stock news", limit=2)
                news_items = []
                for r in results.get('data', {}).get('web', []):
                    news_items.append({
                        'title': r.get('title', ''),
                        'url': r.get('url', ''),
                        'snippet': r.get('description', '')[:200]
                    })
                news[symbol] = news_items
            except Exception:
                pass
    except Exception:
        pass
    
    # Format output
    output = []
    output.append("**📊 Portfolio Heartbeat**")
    output.append("")
    
    for acc_num, data in account_data.items():
        lines = format_account_heartbeat(
            data['account'],
            data['portfolio'],
            data['positions'],
            quotes,
            news
        )
        output.extend(lines)
        output.append("")
    
    # Print result
    result = "\n".join(output)
    print(result)
    
    # Also save to file for cron to pick up
    out_path = Path('/tmp/portfolio_heartbeat.txt')
    out_path.write_text(result)


if __name__ == '__main__':
    main()
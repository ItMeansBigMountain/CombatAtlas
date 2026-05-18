import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { tap } from 'rxjs/operators';

export interface StockInvestment {
  id: number;
  ticker_name: string;
  amount_invested: number;
  analysis_data?: any;
  last_analysis_date?: string;
  editing?: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class StockService {
  private storageKey = 'stockNews.demoPortfolio';
  private apiUrl = this.getApiUrl();

  constructor(private http: HttpClient) { }

  private getApiUrl(): string {
    const host = window.location.hostname;
    if (host === 'localhost' || host === '127.0.0.1') {
      return 'http://localhost:8000/api/stocks/';
    }
    return 'https://stocknews-api.vercel.app/api/stocks/';
  }

  private readPortfolio(): StockInvestment[] {
    const raw = localStorage.getItem(this.storageKey);
    if (!raw) {
      return [
        { id: 1, ticker_name: 'AAPL', amount_invested: 2500 },
        { id: 2, ticker_name: 'MSFT', amount_invested: 1800 },
        { id: 3, ticker_name: 'NVDA', amount_invested: 1200 }
      ];
    }

    try {
      return JSON.parse(raw);
    } catch {
      return [];
    }
  }

  private savePortfolio(stocks: StockInvestment[]): void {
    localStorage.setItem(this.storageKey, JSON.stringify(stocks));
  }

  addStock(stockData: any): Observable<any> {
    const stocks = this.readPortfolio();
    const ticker = String(stockData.ticker_name || '').toUpperCase().trim();
    const existing = stocks.find(stock => stock.ticker_name === ticker);

    if (existing) {
      existing.amount_invested = Number(existing.amount_invested) + Number(stockData.amount_invested || 0);
      this.savePortfolio(stocks);
      return of(existing);
    }

    const newStock = {
      id: Date.now(),
      ticker_name: ticker,
      amount_invested: Number(stockData.amount_invested || 0)
    };
    stocks.push(newStock);
    this.savePortfolio(stocks);
    return of(newStock);
  }

  getAllStocks(): Observable<StockInvestment[]> {
    return of(this.readPortfolio());
  }

  updateStock(stockId: number, stockData: any): Observable<any> {
    const stocks = this.readPortfolio();
    const index = stocks.findIndex(stock => stock.id === stockId);
    if (index !== -1) {
      stocks[index] = { ...stocks[index], ...stockData, ticker_name: String(stockData.ticker_name || stocks[index].ticker_name).toUpperCase() };
      this.savePortfolio(stocks);
      return of(stocks[index]);
    }
    return of(stockData);
  }

  deleteStock(stockId: number): Observable<any> {
    const stocks = this.readPortfolio().filter(stock => stock.id !== stockId);
    this.savePortfolio(stocks);
    return of({ ok: true });
  }

  analyzeStocks(stocks: StockInvestment[]): Observable<StockInvestment[]> {
    return this.http.post<StockInvestment[]>(`${this.apiUrl}analyze-stocks/`, { stocks }).pipe(
      tap((analyzedStocks) => this.savePortfolio(analyzedStocks))
    );
  }
}

import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';
import { StockService, StockInvestment } from '../stock.service';

@Component({
  selector: 'app-portfolio-dashboard',
  templateUrl: './portfolio-dashboard.component.html',
  styleUrls: ['./portfolio-dashboard.component.css']
})
export class PortfolioDashboardComponent implements OnInit {
  fromDate!: string;
  toDate!: string;
  newInvestmentSymbol: string = '';
  newInvestmentAmount: number = 0;
  investments: StockInvestment[] = [];
  isLoading: boolean = false;
  errorMessage: string = '';

  colorScheme: any = {
    domain: ['#16a34a', '#ef4444', '#f59e0b', '#6366f1', '#64748b']
  };

  constructor(
    private stockService: StockService,
    private cdr: ChangeDetectorRef,
    private router: Router,
    private authService: AuthService
  ) { }

  ngOnInit(): void {
    this.initializeDateRange();
    this.fetchUserInvestments();
  }

  private initializeDateRange(): void {
    const currentDate = new Date();
    const oneWeekAgo = new Date(currentDate.getTime() - 7 * 24 * 60 * 60 * 1000);
    this.toDate = currentDate.toISOString().split('T')[0];
    this.fromDate = oneWeekAgo.toISOString().split('T')[0];
  }

  private fetchUserInvestments(): void {
    this.stockService.getAllStocks().subscribe({
      next: (stocks) => {
        this.investments = stocks;
        this.cdr.detectChanges();
      },
      error: () => {
        this.errorMessage = 'Could not load the saved demo portfolio.';
      }
    });
  }

  logout(): void {
    this.authService.removeToken();
    this.router.navigate(['/dashboard']);
  }

  addInvestment(): void {
    const ticker = this.newInvestmentSymbol.toUpperCase().trim();
    const amount = Number(this.newInvestmentAmount);
    if (!ticker || amount <= 0) {
      this.errorMessage = 'Enter a ticker symbol and an investment amount greater than $0.';
      return;
    }

    this.stockService.addStock({ ticker_name: ticker, amount_invested: amount }).subscribe({
      next: () => {
        this.errorMessage = '';
        this.newInvestmentSymbol = '';
        this.newInvestmentAmount = 0;
        this.fetchUserInvestments();
      },
      error: () => {
        this.errorMessage = 'Could not add that ticker.';
      }
    });
  }

  enableEditing(investment: StockInvestment): void {
    investment.editing = true;
  }

  deleteEditing(index: number): void {
    const stockId = this.investments[index].id;
    this.stockService.deleteStock(stockId).subscribe({
      next: () => {
        this.investments.splice(index, 1);
        this.cdr.detectChanges();
      },
      error: () => {
        this.errorMessage = 'Could not delete that stock.';
      }
    });
  }

  saveEditing(investment: StockInvestment, index: number): void {
    investment.editing = false;
    this.stockService.updateStock(investment.id, {
      ticker_name: investment.ticker_name,
      amount_invested: investment.amount_invested,
      analysis_data: investment.analysis_data,
      last_analysis_date: investment.last_analysis_date
    }).subscribe({
      next: (response) => {
        this.investments[index] = { ...response };
        this.cdr.detectChanges();
      },
      error: () => {
        this.errorMessage = 'Could not save that edit.';
        investment.editing = true;
      }
    });
  }

  cancelEditing(investment: StockInvestment): void {
    investment.editing = false;
    this.fetchUserInvestments();
  }

  goToSettings(): void {
    this.router.navigate(['/settings']);
  }

  analyzeStocks(): void {
    if (!this.investments.length) {
      this.errorMessage = 'Add at least one stock before running analysis.';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.stockService.analyzeStocks(this.investments).subscribe({
      next: (analysisResults) => {
        this.isLoading = false;
        this.investments = analysisResults;
        this.cdr.detectChanges();
      },
      error: () => {
        this.isLoading = false;
        this.errorMessage = 'Latest-news analysis is temporarily unavailable. Try again in a minute.';
      }
    });
  }

  sentimentPercent(investment: StockInvestment): number {
    const score = Number(investment.analysis_data?.sentiment || 0);
    return Math.round(((score + 1) / 2) * 100);
  }

  sentimentClass(investment: StockInvestment): string {
    return investment.analysis_data?.label || 'neutral';
  }

  formatEmotions(emotions: any): any[] {
    if (!emotions) {
      return [];
    }
    return Object.keys(emotions).map(key => ({
      name: key.charAt(0).toUpperCase() + key.slice(1),
      value: emotions[key]
    }));
  }
}

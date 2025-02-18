# File: esg_global.py
import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from typing import Dict, List, Optional

console = Console()

# Configuration
EXCHANGE_SUFFIXES = {
    '.US': 'Yahoo Finance',
    '.L': 'London SE',
    '.TO': 'Toronto SE',
    '.PA': 'Euronext Paris',
    '.BR': 'Euronext Brussels',
    '.AS': 'Euronext Amsterdam',
    '.LS': 'Euronext Lisbon',
    '.MI': 'Borsa Italiana',
    '.VI': 'Vienna SE',
    '.BE': 'Berlin SE',
    '.F': 'Frankfurt SE',
    '.DE': 'XETRA',
    '.SG': 'Singapore SGX',
    '.SI': 'Singapore SGX',
    '.HK': 'Hong Kong SE',
    '.SZ': 'Shenzhen SE',
    '.SS': 'Shanghai SE',
    '.KS': 'Korea SE',
    '.KQ': 'KOSDAQ',
    '.TW': 'Taiwan SE',
    '.T': 'Tokyo SE',
    '.TA': 'Tel Aviv SE',
    '.SA': 'Saudi SE',
    '.BA': 'Buenos Aires SE',
    '.MX': 'Mexican SE',
    '.JK': 'Indonesia SE',
    '.NS': 'India NSE',
    '.BO': 'India BSE',
    '.AX': 'Australia ASX',
    '.NZ': 'New Zealand SE'
}

class GlobalESGScanner:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def detect_exchange(self, ticker: str) -> str:
        for suffix, exchange in EXCHANGE_SUFFIXES.items():
            if ticker.upper().endswith(suffix):
                return exchange
        return 'Unknown Exchange'

    def get_esg_data(self, ticker: str) -> Dict:
        exchange = self.detect_exchange(ticker)
        console.print(f"\n[cyan]Scanning {exchange} for {ticker}[/cyan]")
        
        # Try multiple data sources
        data = self._try_yahoo(ticker) or \
               self._try_alpha_vantage(ticker) or \
               self._try_exchange_scraping(ticker, exchange)
        
        return data or {'error': 'ESG data not found'}

    def _try_yahoo(self, ticker: str) -> Optional[Dict]:
        try:
            url = f"https://finance.yahoo.com/quote/{ticker}/sustainability"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return {
                'ticker': ticker,
                'esg_score': self._parse_yahoo_score(soup),
                'environment': self._parse_yahoo_cat(soup, 'environment'),
                'social': self._parse_yahoo_cat(soup, 'social'),
                'governance': self._parse_yahoo_cat(soup, 'governance'),
                'source': 'Yahoo Finance'
            }
        except Exception as e:
            return None

    def _try_alpha_vantage(self, ticker: str) -> Optional[Dict]:
        api_key = os.getenv('ALPHA_VANTAGE_KEY')
        if not api_key:
            return None
            
        try:
            url = f"https://www.alphavantage.co/query?function=ESG_SCORE&symbol={ticker}&apikey={api_key}"
            data = self.session.get(url).json()
            return {
                'ticker': ticker,
                'esg_score': data.get('ESG Score'),
                'environment': data.get('Environmental Score'),
                'social': data.get('Social Score'),
                'governance': data.get('Governance Score'),
                'source': 'Alpha Vantage'
            }
        except:
            return None

    def _try_exchange_scraping(self, ticker: str, exchange: str) -> Optional[Dict]:
        try:
            clean_ticker = re.sub(r'\..*$', '', ticker)
            
            # Special handling for major exchanges
            if 'Euronext' in exchange:
                return self._scrape_euronext(clean_ticker)
            elif 'London' in exchange:
                return self._scrape_lse(clean_ticker)
            elif 'Tokyo' in exchange:
                return self._scrape_jpx(clean_ticker)
            
            # Generic exchange scraper
            return self._generic_scrape(ticker, exchange)
        except:
            return None

    def _scrape_lse(self, ticker: str) -> Dict:
        url = f"https://www.londonstockexchange.com/stock/{ticker}/esg"
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        return {
            'ticker': ticker,
            'esg_score': soup.find('div', class_='esg-rating').text,
            'source': 'London Stock Exchange'
        }

    def _scrape_jpx(self, ticker: str) -> Dict:
        url = f"https://www.jpx.co.jp/english/listing/esg/{ticker}.html"
        response = self.session.get(url)
        # ... (JPX-specific parsing logic)
        return jpx_data

    def display_results(self, data: Dict):
        table = Table(title="Global ESG Analysis", show_lines=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        table.add_column("Source", style="green")
        
        if 'error' in data:
            table.add_row("Error", data['error'], "")
        else:
            for key in ['esg_score', 'environment', 'social', 'governance']:
                table.add_row(key.upper(), str(data.get(key, 'N/A')), data.get('source', ''))
        
        console.print(table)

def main():
    scanner = GlobalESGScanner()
    
    while True:
        console.print("\n[bold]Global ESG Analyzer[/bold]")
        console.print("1. Analyze Ticker\n2. Bulk Export\n3. Exit")
        choice = input("Select option: ")
        
        if choice == '1':
            ticker = input("Enter global ticker (e.g.: AAPL.US, RIO.L, 7203.T): ")
            data = scanner.get_esg_data(ticker)
            scanner.display_results(data)
        elif choice == '2':
            tickers = input("Enter tickers (comma-separated): ").split(',')
            all_data = [scanner.get_esg_data(t.strip()) for t in tickers]
            pd.DataFrame(all_data).to_excel('global_esg.xlsx')
            console.print("[green]Exported to global_esg.xlsx[/green]")
        elif choice == '3':
            break

if __name__ == "__main__":
    main()
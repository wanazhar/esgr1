import argparse
import os
import sys
import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from textwrap import wrap
from rich.console import Console
from rich.table import Table
import openpyxl

# Configuration
console = Console()
API_KEYS = {
    'alpha_vantage': os.getenv('ALPHA_VANTAGE_API_KEY'),
    'gnews': os.getenv('GNEWS_API_KEY'),
    'openai': os.getenv('OPENAI_API_KEY')  # For LLM analysis
}

# Malaysian company helpers
MY_EXCHANGES = {'KLSE': 'KL', 'MYX': 'MY'}
MY_ESG_SOURCES = {
    'Bursa Malaysia': 'https://www.bursamalaysia.com',
    'Securities Commission Malaysia': 'https://www.sc.com.my'
}

def display_header():
    console.print("\n[bold cyan]ESG Data Collector[/bold cyan]")
    console.print("[yellow]⊛ Malaysian Company Support[/yellow]")
    console.print("[yellow]⊛ Annual Report Analysis[/yellow]\n")

def menu():
    display_header()
    console.print("1. View ESG Data", style="bold green")
    console.print("2. Export Data to Excel", style="bold blue")
    console.print("3. Analyze Annual Reports", style="bold magenta")
    console.print("4. Full Analysis & Export", style="bold red")
    console.print("5. Exit\n", style="bold yellow")
    return input("Enter choice (1-5): ")

def get_malaysia_esg(symbol):
    """Custom ESG data for Malaysian companies"""
    try:
        url = f"{MY_ESG_SOURCES['Bursa Malaysia']}/market/company/{symbol}"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example extraction - adjust based on actual page structure
        esg_section = soup.find('div', {'class': 'esg-score'})
        return {
            'Symbol': symbol,
            'Environment': float(esg_section.find('span', class_='env-score').text),
            'Social': float(esg_section.find('span', class_='soc-score').text),
            'Governance': float(esg_section.find('span', class_='gov-score').text),
            'Source': 'Bursa Malaysia'
        }
    except Exception as e:
        console.print(f"[red]Error fetching Malaysia ESG: {e}[/red]")
        return None

def analyze_with_llm(text):
    """Use OpenAI GPT for ESG analysis"""
    if not API_KEYS['openai']:
        console.print("[yellow]LLM analysis disabled. Set OPENAI_API_KEY[/yellow]")
        return ""
    
    from openai import OpenAI
    client = OpenAI(api_key=API_KEYS['openai'])
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"Analyze this annual report text for ESG factors. Focus on Malaysian context. Return key findings in bullet points:\n\n{text}"
        }]
    )
    return response.choices[0].message.content

def parse_annual_report(url):
    """Scrape and analyze annual reports"""
    try:
        console.print(f"[cyan]Fetching {url}[/cyan]")
        response = requests.get(url)
        
        if url.endswith('.pdf'):
            from PyPDF2 import PdfReader
            pdf = PdfReader(response.content)
            text = "\n".join([page.extract_text() for page in pdf.pages])
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
        
        analysis = analyze_with_llm(text[:15000])  # Limit context
        return analysis
    except Exception as e:
        console.print(f"[red]Error processing report: {e}[/red]")
        return None

def display_esg(data):
    """Rich terminal display"""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Symbol", style="cyan")
    table.add_column("Environmental", justify="right")
    table.add_column("Social", justify="right")
    table.add_column("Governance", justify="right")
    table.add_column("Source")
    
    for item in data:
        table.add_row(
            item['Symbol'],
            str(item['Environment']),
            str(item['Social']),
            str(item['Governance']),
            item['Source']
        )
    
    console.print(table)

def main():
    while True:
        choice = menu()
        
        if choice == '1':
            symbols = input("Enter tickers (e.g., 1155.KL, MAYBANK.MY): ").split()
            data = [get_malaysia_esg(sym) for sym in symbols]
            display_esg([d for d in data if d])
        
        elif choice == '2':
            symbols = input("Enter tickers to export: ").split()
            output_file = input("Output filename (e.g., esg_data.xlsx): ")
            data = [get_malaysia_esg(sym) for sym in symbols]
            pd.DataFrame([d for d in data if d]).to_excel(output_file, index=False)
            console.print(f"[green]Data saved to {output_file}[/green]")
        
        elif choice == '3':
            url = input("Enter annual report URL: ")
            analysis = parse_annual_report(url)
            console.print(f"\n[bold]LLM Analysis:[/bold]\n{analysis}")
        
        elif choice == '4':
            symbols = input("Enter tickers: ").split()
            output_file = input("Output filename: ")
            data = [get_malaysia_esg(sym) for sym in symbols]
            pd.DataFrame([d for d in data if d]).to_excel(output_file, index=False)
            console.print(f"[green]Full export completed to {output_file}[/green]")
        
        elif choice == '5':
            console.print("[yellow]Exiting...[/yellow]")
            break
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
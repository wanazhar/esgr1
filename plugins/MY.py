import requests
from bs4 import BeautifulSoup
from typing import Dict, Any

def get_esg_data(ticker: str) -> Dict[str, Any]:
    """Malaysia-specific ESG data from Bursa Malaysia"""
    try:
        url = f"https://www.bursamalaysia.com/market/company/{ticker}"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        return {
            'company': _get_company_name(soup),
            'metrics': [
                {'name': 'Environmental', 'value': _extract_score(soup, 'env'),
                 'source': 'Bursa Malaysia', 'updated': _get_date()},
                {'name': 'Social', 'value': _extract_score(soup, 'soc'),
                 'source': 'Bursa Malaysia', 'updated': _get_date()}
            ]
        }
    except Exception as e:
        return _fallback_data(ticker)

def _get_company_name(soup):
    return soup.find('h1', class_='company-name').text.strip()

def _extract_score(soup, category):
    return soup.find('div', class_=f'esg-{category}-score').text.strip()
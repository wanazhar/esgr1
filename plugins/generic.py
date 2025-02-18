import os
import requests
from typing import Dict, Any

def get_esg_data(ticker: str) -> Dict[str, Any]:
    """Fallback using Alpha Vantage"""
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    url = f"https://www.alphavantage.co/query?function=ESG_SCORE&symbol={ticker}&apikey={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        return {
            'company': data.get('name', ticker),
            'metrics': [
                {'name': 'ESG Score', 'value': data.get('ESG Score', 'N/A'),
                 'source': 'Alpha Vantage', 'updated': data.get('Last Updated')}
            ]
        }
    except:
        return {'error': 'Data unavailable'}
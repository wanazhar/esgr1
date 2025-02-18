import xml.etree.ElementTree as ET
from typing import Dict, Any

def get_esg_data(ticker: str) -> Dict[str, Any]:
    """UK ESG data from London Stock Exchange"""
    try:
        # LSEG ESG API (example)
        response = requests.get(
            f"https://api.londonstockexchange.com/esg/{ticker}",
            headers={'Authorization': f'Bearer {os.getenv("LSE_API_KEY")}'}
        )
        
        root = ET.fromstring(response.content)
        return {
            'company': root.find('.//CompanyName').text,
            'metrics': [
                _parse_lseg_xml(root),
                _get_ftse4good_rating(ticker)
            ]
        }
    except:
        return _fallback_uk(ticker)
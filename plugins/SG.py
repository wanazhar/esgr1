def get_esg_data(ticker: str) -> Dict[str, Any]:
    """Singapore ESG data from SGX"""
    try:
        # SGX Sustainability Reports
        pdf_url = f"https://api.sgx.com/sustainability/{ticker}"
        pdf_text = _extract_pdf_text(pdf_url)
        
        return {
            'company': _extract_company_name(pdf_text),
            'metrics': [
                _analyze_sgx_pdf(pdf_text),
                _get_carbon_pricing_data(ticker)
            ]
        }
    except:
        return _fallback_sg(ticker)
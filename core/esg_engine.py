import importlib
import yaml
from pathlib import Path
from typing import Dict, Any

class ESGEngine:
    def __init__(self):
        self.countries = self._load_config('config/countries.yaml')
        self.sources = self._load_config('config/sources.yaml')
        self.plugins = self._load_plugins()

    def _load_config(self, path: str) -> Dict:
        with open(path) as f:
            return yaml.safe_load(f)

    def _load_plugins(self) -> Dict:
        plugins = {}
        for country_code in self.countries['countries']:
            try:
                module = importlib.import_module(f"plugins.{country_code}")
                plugins[country_code] = module
            except ImportError:
                continue
        return plugins

    def get_esg_data(self, country: str, ticker: str) -> Dict[str, Any]:
        if country not in self.plugins:
            return self._fallback_data(ticker)
        return self.plugins[country].get_esg_data(ticker)

    def _fallback_data(self, ticker: str) -> Dict:
        from plugins.generic import get_esg_data
        return get_esg_data(ticker)
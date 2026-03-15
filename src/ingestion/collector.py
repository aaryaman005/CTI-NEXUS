from typing import List
import requests
from src.core.logger import logger
from src.ingestion.parser import ThreatParser
from src.models.indicator import BaseIndicator


class IntelCollector:
    """Base class for threat intelligence collectors."""

    def __init__(self, source_name: str):
        self.source_name = source_name
        self.parser = ThreatParser()

    def fetch_data(self) -> List[dict]:
        """Fetch raw data from the source. To be implemented by subclasses."""
        raise NotImplementedError

    def collect_and_normalize(self) -> List[BaseIndicator]:
        """Fetches and normalizes indicators."""
        logger.info(f"Starting collection from {self.source_name}")
        raw_data = self.fetch_data()
        indicators = []
        for item in raw_data:
            ind = self.parser.parse_raw_indicator(item)
            if ind:
                indicators.append(ind)
        logger.info(f"Collected and normalized {len(indicators)} indicators from {self.source_name}")
        return indicators


class OSINTFeedCollector(IntelCollector):
    """Collects indicators from a generic OSINT JSON feed."""

    def __init__(self, source_name: str, feed_url: str):
        super().__init__(source_name)
        self.feed_url = feed_url

    def fetch_data(self) -> List[dict]:
        try:
            response = requests.get(self.feed_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and "indicators" in data:
                return data.get("indicators", [])
            return []
        except Exception as e:
            logger.error(f"Error fetching OSINT feed from {self.feed_url}: {e}")
            return []

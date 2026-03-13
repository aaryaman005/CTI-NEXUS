from typing import List, Dict, Any
from src.models.indicator import BaseIndicator, IndicatorType
from src.core.logger import logger
from src.core.config import settings

class BaseEnricher:
    """Base class for indicator enrichment services."""
    def __init__(self, name: str):
        self.name = name

    def enrich(self, indicator: BaseIndicator) -> BaseIndicator:
        """Enriches a single indicator. To be implemented by subclasses."""
        raise NotImplementedError

class VirusTotalEnricher(BaseEnricher):
    def __init__(self, api_key: str):
        super().__init__("VirusTotal")
        self.api_key = api_key

    def enrich(self, indicator: BaseIndicator) -> BaseIndicator:
        if not self.api_key:
            logger.warning("VirusTotal API key missing, skipping enrichment.")
            return indicator
            
        logger.info(f"Enriching {indicator.value} with VirusTotal")
        # Stub implementation
        # Ideally, make an API call to VT and append to indicator.metadata
        if indicator.type in [IndicatorType.IPV4, IndicatorType.DOMAIN, IndicatorType.URL, IndicatorType.FILE_HASH]:
            indicator.metadata['vt_score'] = "0/90" # Stub
            indicator.metadata['vt_enriched'] = True
        return indicator

class ShodanEnricher(BaseEnricher):
    def __init__(self, api_key: str):
        super().__init__("Shodan")
        self.api_key = api_key

    def enrich(self, indicator: BaseIndicator) -> BaseIndicator:
        if not self.api_key:
            logger.warning("Shodan API key missing, skipping enrichment.")
            return indicator
            
        if indicator.type == IndicatorType.IPV4:
            logger.info(f"Enriching {indicator.value} with Shodan")
            # Stub implementation
            indicator.metadata['shodan_ports'] = [80, 443] # Stub
        return indicator

class EnrichmentManager:
    """Manages multiple enrichment services and applies them to indicators."""
    def __init__(self):
        self.enrichers: List[BaseEnricher] = []
        if settings.VIRUSTOTAL_API_KEY:
            self.enrichers.append(VirusTotalEnricher(settings.VIRUSTOTAL_API_KEY))
        if settings.SHODAN_API_KEY:
            self.enrichers.append(ShodanEnricher(settings.SHODAN_API_KEY))
            
    def enrich_all(self, indicators: List[BaseIndicator]) -> List[BaseIndicator]:
        logger.info(f"Enriching {len(indicators)} indicators using {len(self.enrichers)} services")
        enriched_indicators = []
        for ind in indicators:
            current_ind = ind
            for enricher in self.enrichers:
                try:
                    current_ind = enricher.enrich(current_ind)
                except Exception as e:
                    logger.error(f"Error enriching {ind.value} with {enricher.name}: {e}")
            enriched_indicators.append(current_ind)
        return enriched_indicators

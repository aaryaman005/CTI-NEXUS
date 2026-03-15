import os
import sys

# Add the project root to the sys path if executing directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.logger import logger  # noqa: E402
from src.enrichment.enricher import EnrichmentManager  # noqa: E402
from src.analysis.graph import GraphEngine  # noqa: E402
from src.reporting.generator import ReportGenerator  # noqa: E402
from src.models.indicator import IPv4Indicator, DomainIndicator  # noqa: E402
from src.analysis.correlation import CorrelationEngine  # noqa: E402
from src.analysis.campaign import CampaignDetector  # noqa: E402

def main():
    logger.info("Starting CTI Nexus Intelligence Core...")

    # Mocking data for immediate end-to-end testing
    indicators = [
        DomainIndicator(id="dom-1", value="malware-c2.example.com", confidence=90),
        IPv4Indicator(id="ip-1", value="192.168.1.100", confidence=85, metadata={"a_records": ["192.168.1.100"]}),
    ]
    indicators[0].metadata["a_records"] = ["192.168.1.100"]

    # 1. Enrichment
    enrichment_manager = EnrichmentManager()
    enriched_indicators = enrichment_manager.enrich_all(indicators)

    # 2. Graph Engine & Correlation
    graph_engine = GraphEngine()
    try:
        graph_engine.connect()

        correlation_engine = CorrelationEngine(graph_engine)
        correlation_engine.correlate(enriched_indicators)

        # Campaign Detection
        campaign_detector = CampaignDetector(graph_engine)
        campaigns = campaign_detector.detect_campaigns()

        # Reporting
        report_generator = ReportGenerator()
        report = report_generator.generate_summary_report(enriched_indicators, campaigns)

        logger.info(f"Execution complete. Final Intelligence Output Summary:\n{report}")

    except Exception as e:
        logger.error(f"Execution failed: {e}")
    finally:
        graph_engine.close()


if __name__ == "__main__":
    main()

import os
import sys

# Add the project root to the sys path if executing directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.logger import logger  # noqa: E402
from src.enrichment.enricher import EnrichmentManager  # noqa: E402
from src.analysis.graph import GraphEngine  # noqa: E402
from src.reporting.generator import ReportGenerator  # noqa: E402
from src.models.indicator import IPv4Indicator, DomainIndicator  # noqa: E402


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
        # Note: requires Neo4j running locally for a successful connection
        # graph_engine.connect()
        # To avoid failure when testing without Neo4j, we will print a warning if not connected
        logger.warning(
            "Skipping real Neo4j connection for this demo run. "
            "Graph relationship creation will be skipped/simulated."
        )

        # We manually stub driver for this quick run if neo4j is down
        # correlation_engine = CorrelationEngine(graph_engine)
        # correlation_engine.correlate(enriched_indicators)

        # Campaign Detection
        # campaign_detector = CampaignDetector(graph_engine)
        # campaigns = campaign_detector.detect_campaigns()
        campaigns = [{"campaign_id": "CMP-SIMULATED-1001", "indicators": "simulated"}]

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

from typing import List, Dict, Any
import json
from datetime import datetime, timezone
from src.core.logger import logger
from src.models.indicator import BaseIndicator


class ReportGenerator:
    """Generates structured intelligence reports."""

    def generate_summary_report(self, indicators: List[BaseIndicator], campaigns: List[Dict[str, Any]]) -> str:
        """Generates a JSON formatted summary report."""
        logger.info("Generating intelligence summary report")

        report = {
            "report_id": f"REP-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "metrics": {"total_indicators": len(indicators), "total_campaigns": len(campaigns)},
            "campaigns": campaigns,
            "indicators": [ind.model_dump() for ind in indicators],
        }

        # Simply return the JSON string for now
        return json.dumps(report, indent=4, default=str)

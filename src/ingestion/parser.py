from typing import Dict, Any, Optional
import uuid
from src.models.indicator import (
    IndicatorType,
    BaseIndicator,
    IPv4Indicator,
    DomainIndicator,
    FileHashIndicator,
    URLIndicator,
    get_utc_now,
)
from src.core.logger import logger


class ThreatParser:
    """Parses raw threat intelligence data into normalized Pydantic models."""

    @staticmethod
    def parse_raw_indicator(raw_data: Dict[str, Any]) -> Optional[BaseIndicator]:
        """
        Parses a raw dictionary into an Indicator model.
        Expected minimum fields in raw_data:
        - 'value': str
        - 'type': str (must match an IndicatorType)
        """
        try:
            ind_type_str = raw_data.get("type", "").lower()
            value = raw_data.get("value")

            if not ind_type_str or not value:
                logger.warning(f"Missing type or value in raw data: {raw_data}")
                return None

            ind_id = raw_data.get("id", str(uuid.uuid4()))
            confidence = raw_data.get("confidence", 50)
            tags = raw_data.get("tags", [])
            metadata = raw_data.get("metadata", {})
            first_seen = raw_data.get("first_seen", get_utc_now())

            base_kwargs = {
                "id": ind_id,
                "value": value,
                "confidence": confidence,
                "tags": tags,
                "metadata": metadata,
                "first_seen": first_seen,
            }

            if ind_type_str == IndicatorType.IPV4.value:
                return IPv4Indicator(**base_kwargs, asn=raw_data.get("asn"), country=raw_data.get("country"))
            elif ind_type_str == IndicatorType.DOMAIN.value:
                return DomainIndicator(**base_kwargs, registrar=raw_data.get("registrar"))
            elif ind_type_str == IndicatorType.FILE_HASH.value:
                return FileHashIndicator(
                    **base_kwargs,
                    hash_type=raw_data.get("hash_type", "unknown"),
                    file_size=raw_data.get("file_size"),
                    file_names=raw_data.get("file_names", []),
                )
            elif ind_type_str == IndicatorType.URL.value:
                return URLIndicator(**base_kwargs, domain_ref=raw_data.get("domain_ref"))
            else:
                logger.warning(f"Unsupported indicator type: {ind_type_str}")
                return None

        except Exception as e:
            logger.error(f"Failed to parse raw indicator data {raw_data}: {e}")
            return None

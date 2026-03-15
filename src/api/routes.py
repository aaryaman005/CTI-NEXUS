from fastapi import APIRouter, HTTPException
from typing import List, Dict
from src.api.models import IndicatorCreateRequest, IndicatorResponse, CampaignResponse
from src.models.indicator import (
    IndicatorType,
    IPv4Indicator,
    DomainIndicator,
    FileHashIndicator,
    URLIndicator,
    BaseIndicator,
)
from src.enrichment.enricher import EnrichmentManager
from src.analysis.graph import GraphEngine
from src.analysis.correlation import CorrelationEngine
from src.analysis.campaign import CampaignDetector
from src.reporting.generator import ReportGenerator
from src.core.logger import logger
import uuid

router = APIRouter(prefix="/api/v1", tags=["Intelligence"])

# In a real app, these would be injected dependencies. For now, global instances.
enrichment_manager = EnrichmentManager()
graph_engine = GraphEngine()
# Suppress connection errors if Neo4j isn't running
try:
    graph_engine.connect()
except Exception:
    logger.warning("Neo4j not available, operating in degraded Graph mode for API")


def _convert_to_core_model(req: IndicatorCreateRequest) -> BaseIndicator:
    ind_id = str(uuid.uuid4())
    if req.type == IndicatorType.IPV4:
        return IPv4Indicator(id=ind_id, value=req.value, confidence=req.confidence, metadata=req.metadata)
    elif req.type == IndicatorType.DOMAIN:
        return DomainIndicator(id=ind_id, value=req.value, confidence=req.confidence, metadata=req.metadata)
    elif req.type == IndicatorType.FILE_HASH:
        return FileHashIndicator(
            id=ind_id, value=req.value, confidence=req.confidence, metadata=req.metadata, hash_type="UNKNOWN"
        )
    elif req.type == IndicatorType.URL:
        return URLIndicator(id=ind_id, value=req.value, confidence=req.confidence, metadata=req.metadata)
    raise ValueError(f"Unsupported indicator type: {req.type}")


def _convert_to_api_response(ind: BaseIndicator) -> IndicatorResponse:
    return IndicatorResponse(
        id=ind.id, value=ind.value, type=ind.type.value, confidence=ind.confidence, metadata=ind.metadata
    )


@router.post("/ingest", response_model=IndicatorResponse)
async def ingest_indicator(indicator_in: IndicatorCreateRequest):
    """Ingests a new indicator, enriches it, and adds it to the graph."""
    logger.info(f"API Ingesting indicator: {indicator_in.value}")
    try:
        # 1. Convert to Core Model
        core_ind = _convert_to_core_model(indicator_in)

        # 2. Enrich
        enriched_ind = enrichment_manager.enrich_all([core_ind])[0]

        # 3. Add to Graph (if available)
        if graph_engine.driver:
            correlation_engine = CorrelationEngine(graph_engine)
            correlation_engine.correlate([enriched_ind])

        return _convert_to_api_response(enriched_ind)
    except Exception as e:
        logger.error(f"API Ingestion error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/campaigns", response_model=List[CampaignResponse])
async def get_campaigns():
    """Detects and returns active threat campaigns based on graph clusters."""
    if not graph_engine.driver:
        # Return a simulated campaign if no DB
        return [
            CampaignResponse(campaign_id="CMP-SIMULATED", indicator_count=2, indicators=["192.168.1.1", "evil.com"])
        ]

    try:
        detector = CampaignDetector(graph_engine)
        campaigns = detector.detect_campaigns()

        results = []
        for c in campaigns:
            results.append(
                CampaignResponse(
                    campaign_id=c.get("campaign_id", "UNKNOWN"),
                    indicator_count=len(c.get("indicators", [])),
                    indicators=c.get("indicators", []),
                )
            )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


import json


@router.get("/report", response_model=Dict)
async def generate_report():
    """Generates a full intelligence summary report."""
    rg = ReportGenerator()
    try:
        report_str = rg.generate_summary_report([], [])
        return json.loads(report_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

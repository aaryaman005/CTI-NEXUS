from pydantic import BaseModel, Field
from typing import List, Dict, Any
from src.models.indicator import IndicatorType


class IndicatorCreateRequest(BaseModel):
    """Schema for ingesting a new indicator via API."""

    value: str = Field(..., description="The observable value (e.g. IP, Domain)")
    type: IndicatorType = Field(..., description="The type of the indicator")
    confidence: int = Field(50, ge=0, le=100, description="Confidence score from 0-100")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


class IndicatorResponse(BaseModel):
    """Schema for returning an indicator via API."""

    id: str
    value: str
    type: str
    confidence: int
    metadata: Dict[str, Any]


class CampaignResponse(BaseModel):
    """Schema for returning a detected campaign."""

    campaign_id: str
    indicator_count: int
    indicators: List[str]


class IntelligenceReportResponse(BaseModel):
    """Schema for the final generated intelligence report."""

    report_id: str
    generated_at: str
    total_indicators: int
    campaigns_detected: int
    indicators: List[IndicatorResponse]
    campaigns: List[CampaignResponse]

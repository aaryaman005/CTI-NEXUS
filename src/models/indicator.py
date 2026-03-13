from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone

def get_utc_now():
    return datetime.now(timezone.utc)

class IndicatorType(str, Enum):
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    DOMAIN = "domain"
    URL = "url"
    FILE_HASH = "file_hash"
    EMAIL = "email"

class BaseIndicator(BaseModel):
    id: str
    type: IndicatorType
    value: str
    first_seen: datetime = Field(default_factory=get_utc_now)
    last_seen: datetime = Field(default_factory=get_utc_now)
    confidence: int = Field(default=50, ge=0, le=100)
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
class IPv4Indicator(BaseIndicator):
    type: IndicatorType = IndicatorType.IPV4
    asn: Optional[str] = None
    country: Optional[str] = None

class DomainIndicator(BaseIndicator):
    type: IndicatorType = IndicatorType.DOMAIN
    registrar: Optional[str] = None
    creation_date: Optional[datetime] = None

class FileHashIndicator(BaseIndicator):
    type: IndicatorType = IndicatorType.FILE_HASH
    hash_type: str  # MD5, SHA1, SHA256
    file_size: Optional[int] = None
    file_names: List[str] = Field(default_factory=list)

class URLIndicator(BaseIndicator):
    type: IndicatorType = IndicatorType.URL
    domain_ref: Optional[str] = None

from src.models.indicator import (
    IPv4Indicator,
    DomainIndicator,
    FileHashIndicator,
    IndicatorType,
)


def test_ipv4_indicator_creation():
    ind = IPv4Indicator(id="test-1", value="10.0.0.1", confidence=90)
    assert ind.type == IndicatorType.IPV4
    assert ind.value == "10.0.0.1"


def test_domain_indicator_creation():
    ind = DomainIndicator(id="test-2", value="bad.com")
    assert ind.type == IndicatorType.DOMAIN


def test_file_hash_indicator_creation():
    ind = FileHashIndicator(
        id="test-3",
        value="abc123",
        hash_type="SHA256",
    )
    assert ind.type == IndicatorType.FILE_HASH
    assert ind.hash_type == "SHA256"


def test_confidence_bounds():
    ind = IPv4Indicator(id="test-4", value="1.2.3.4", confidence=0)
    assert ind.confidence == 0

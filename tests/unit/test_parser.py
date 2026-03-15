from src.ingestion.parser import ThreatParser


def test_parse_ipv4_indicator():
    raw = {
        "type": "ipv4",
        "value": "192.168.1.1",
        "confidence": 80,
    }
    result = ThreatParser.parse_raw_indicator(raw)
    assert result is not None
    assert result.value == "192.168.1.1"
    assert result.confidence == 80


def test_parse_domain_indicator():
    raw = {
        "type": "domain",
        "value": "evil.example.com",
    }
    result = ThreatParser.parse_raw_indicator(raw)
    assert result is not None
    assert result.value == "evil.example.com"


def test_parse_file_hash_indicator():
    raw = {
        "type": "file_hash",
        "value": "d41d8cd98f00b204e9800998ecf8427e",
        "hash_type": "MD5",
    }
    result = ThreatParser.parse_raw_indicator(raw)
    assert result is not None
    assert result.value == "d41d8cd98f00b204e9800998ecf8427e"


def test_parse_invalid_type():
    raw = {
        "type": "unknown_type",
        "value": "something",
    }
    result = ThreatParser.parse_raw_indicator(raw)
    assert result is None


def test_parse_missing_value():
    raw = {
        "type": "ipv4",
    }
    result = ThreatParser.parse_raw_indicator(raw)
    assert result is None

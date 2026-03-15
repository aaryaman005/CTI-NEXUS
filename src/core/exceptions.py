class CTINexusException(Exception):
    """Base exception for all CTI Nexus errors."""

    pass


class ConfigurationError(CTINexusException):
    """Raised when there is a configuration issue."""

    pass


class IngestionError(CTINexusException):
    """Raised when data ingestion fails."""

    pass


class NormalizationError(CTINexusException):
    """Raised when data normalization fails."""

    pass


class EnrichmentError(CTINexusException):
    """Raised when data enrichment fails."""

    pass


class GraphEngineError(CTINexusException):
    """Raised when graph database operations fail."""

    pass

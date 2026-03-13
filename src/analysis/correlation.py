from typing import List
from src.core.logger import logger
from src.models.indicator import BaseIndicator, IndicatorType
from src.analysis.graph import GraphEngine

class CorrelationEngine:
    """Identifies relationships between indicators and updates the intelligence graph."""
    
    def __init__(self, graph_engine: GraphEngine):
        self.graph = graph_engine
        
    def correlate(self, indicators: List[BaseIndicator]):
        """Runs correlation algorithms on a set of indicators."""
        logger.info(f"Starting correlation for {len(indicators)} indicators")
        
        # 1. Add all indicators as nodes
        for ind in indicators:
            self.graph.add_indicator(ind)
            
        # 2. Identify simple relationships based on metadata
        # Example: if a Domain indicator has an 'a_records' list in metadata, link them to the domain
        for ind in indicators:
            if ind.type == IndicatorType.DOMAIN:
                a_records = ind.metadata.get("a_records", [])
                for ip in a_records:
                    self.graph.add_relationship(ind.value, ip, "RESOLVES_TO")
                    
        # Future implementations will run more complex Cypher queries on the graph 
        # to identify shared infrastructure and higher level correlations.
        
        logger.info("Correlation complete")

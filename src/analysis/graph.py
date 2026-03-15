from typing import Dict, Any, Optional
from neo4j import GraphDatabase, Driver
from src.core.logger import logger
from src.core.config import settings
from src.models.indicator import BaseIndicator


class GraphEngine:
    """Manages connections and operations with the Neo4j Graph Database."""

    def __init__(self):
        self.uri = settings.NEO4J_URI
        self.user = settings.NEO4J_USER
        self.password = settings.NEO4J_PASSWORD
        self.driver: Optional[Driver] = None

    def connect(self):
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            self.driver.verify_connectivity()
            logger.info(f"Connected to Neo4j at {self.uri}")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise

    def close(self):
        if self.driver:
            self.driver.close()
            logger.info("Closed Neo4j connection")

    def add_indicator(self, indicator: BaseIndicator):
        """Adds or updates an indicator node in the graph."""
        query = (
            "MERGE (i:Indicator {value: $value}) "
            "SET i.id = $id, i.type = $type, i.confidence = $confidence, "
            "i.first_seen = $first_seen, i.last_seen = $last_seen "
            "RETURN i"
        )
        parameters = {
            "value": indicator.value,
            "id": indicator.id,
            "type": indicator.type.value,
            "confidence": indicator.confidence,
            "first_seen": indicator.first_seen.isoformat(),
            "last_seen": indicator.last_seen.isoformat(),
        }
        with self.driver.session() as session:
            try:
                session.run(query, parameters)
                logger.debug(f"Added/Updated indicator node: {indicator.value}")
            except Exception as e:
                logger.error(f"Error adding indicator node {indicator.value}: {e}")

    def add_relationship(
        self, source_value: str, target_value: str, relationship_type: str, properties: Dict[str, Any] = None
    ):
        """Adds a relationship between two existing indicator nodes."""
        if properties is None:
            properties = {}

        # Simplistic merge without relationship properties for now
        query = (
            "MATCH (a:Indicator {value: $source_value}) "
            "MATCH (b:Indicator {value: $target_value}) "
            f"MERGE (a)-[r:{relationship_type}]->(b) "
            "RETURN r"
        )
        parameters = {"source_value": source_value, "target_value": target_value}
        with self.driver.session() as session:
            try:
                session.run(query, parameters)
                logger.debug(f"Added relationship {source_value} -[{relationship_type}]-> {target_value}")
            except Exception as e:
                logger.error(f"Error adding relationship: {e}")

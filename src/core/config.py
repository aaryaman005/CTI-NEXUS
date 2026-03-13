import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

    VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")
    SHODAN_API_KEY = os.getenv("SHODAN_API_KEY", "")
    MISP_URL = os.getenv("MISP_URL", "")
    MISP_KEY = os.getenv("MISP_KEY", "")

settings = Settings()

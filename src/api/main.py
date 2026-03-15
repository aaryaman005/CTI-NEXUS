from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.logger import logger
from src.api.routes import router as api_router


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application instance."""
    app = FastAPI(
        title="CTI Nexus API",
        description="Cyber Threat Intelligence Correlation & Analysis Platform API",
        version="1.0.0",
    )

    # Configure CORS for potential frontend integration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict this
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(api_router)

    @app.on_event("startup")
    async def startup_event():
        logger.info("CTI Nexus API starting up...")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("CTI Nexus API shutting down...")
        # Close DB connections, etc. if needed
        # from src.api.routes import graph_engine
        # graph_engine.close()

    @app.get("/health", tags=["System"])
    async def health_check():
        """Basic health check endpoint."""
        return {"status": "healthy", "service": "cti-nexus"}

    return app


# The instance for uvicorn to run
app = create_app()

"""
Application Runner
==================
Main entry point for the EMR Integrative Care System
"""

import uvicorn
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

from app.core.config import get_settings

def main():
    """Main function to run the application"""
    settings = get_settings()
    
    # Configure logging
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "root": {
            "level": settings.LOG_LEVEL,
            "handlers": ["default"],
        },
    }
    
    # Run the application
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_config=log_config,
        access_log=True
    )

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Main entry point for the ArXiv Research Agent
"""
import logging
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.arxiv_agent.ui.gradio_interface import GradioInterface
from config.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('arxiv_agent.log')
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main function to launch the ArXiv Research Agent"""
    try:
        logger.info("Starting ArXiv Research Agent...")
        
        # Load configuration
        config = Config()
        config.validate_config()
        
        # Create and launch Gradio interface
        interface = GradioInterface(config)
        interface.launch()
        
    except Exception as e:
        logger.error(f"Failed to start ArXiv Research Agent: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
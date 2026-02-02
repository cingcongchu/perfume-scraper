# Simple scraper module
# This file is maintained for backward compatibility

from src.scrapers.fragrantica_scraper import FragranticaScraper

# Maintain backward compatibility
SimplePerfumeScraper = FragranticaScraper

__all__ = ['SimplePerfumeScraper']

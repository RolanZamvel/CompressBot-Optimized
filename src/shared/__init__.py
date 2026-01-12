"""
Shared module for CompressBot Optimized.

This module provides common utilities and services for the application.
"""

from .config import ConfigService
from .logging import get_logger, setup_logging
from .dependency_injection import DIContainer

__all__ = ['ConfigService', 'get_logger', 'setup_logging', 'DIContainer']
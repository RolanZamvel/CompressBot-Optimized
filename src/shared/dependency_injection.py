"""
Dependency Injection Container for CompressBot Optimized.

This module provides a simple dependency injection container
to manage service dependencies following SOLID principles.
"""
from typing import Dict, Any, Type, TypeVar, Callable, Optional
from abc import ABC, abstractmethod

T = TypeVar('T')


class DIContainer:
    """Simple dependency injection container."""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._singletons: Dict[str, Any] = {}
    
    def register(self, name: str, service: Any, singleton: bool = True) -> None:
        """Register a service instance."""
        if singleton:
            self._singletons[name] = service
        else:
            self._services[name] = service
    
    def register_factory(self, name: str, factory: Callable, singleton: bool = True) -> None:
        """Register a service factory."""
        self._factories[name] = (factory, singleton)
    
    def get(self, name: str) -> Any:
        """Get a service instance."""
        # Check singletons first
        if name in self._singletons:
            return self._singletons[name]
        
        # Check regular services
        if name in self._services:
            return self._services[name]
        
        # Check factories
        if name in self._factories:
            factory, is_singleton = self._factories[name]
            instance = factory()
            if is_singleton:
                self._singletons[name] = instance
            return instance
        
        raise ValueError(f"Service '{name}' not registered")
    
    def has(self, name: str) -> bool:
        """Check if a service is registered."""
        return name in self._services or name in self._factories or name in self._singletons
    
    def clear(self) -> None:
        """Clear all registered services."""
        self._services.clear()
        self._factories.clear()
        self._singletons.clear()


class ServiceProvider(ABC):
    """Abstract base class for service providers."""
    
    @abstractmethod
    def register(self, container: DIContainer) -> None:
        """Register services in the container."""
        pass

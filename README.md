# 🤖 CompressBot Optimized

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![SOLID](https://img.shields.io/badge/SOLID-Principles-green)
![Clean Architecture](https://img.shields.io/badge/Clean-Architecture-orange)

Versión optimizada de CompressBot con principios SOLID y arquitectura limpia desde cero.

## 🎯 Objetivo

Este proyecto es una refactorización completa del BotCompressor original, aplicando principios SOLID de manera rigurosa para crear un sistema altamente mantenible, escalable y testeable.

## 🏗️ Arquitectura SOLID

### Principios Implementados

- **S**ingle Responsibility: Cada clase tiene una única responsabilidad
- **O**pen/Closed: Abierto para extensión, cerrado para modificación  
- **L**iskov Substitution: Las subclases pueden reemplazar a sus clases base
- **I**nterface Segregation: Interfaces pequeñas y específicas
- **D**ependency Inversion: Dependencias de abstracciones, no de concretos

### Estructura del Proyecto

```
src/
├── domain/                    # Dominio y entidades de negocio
│   ├── entities/             # Entidades principales
│   ├── value_objects/        # Objetos de valor
│   └── exceptions/           # Excepciones de dominio
├── application/              # Casos de uso y lógica de aplicación
│   ├── use_cases/           # Casos de uso
│   ├── services/            # Servicios de aplicación
│   └── dto/                 # Data Transfer Objects
├── infrastructure/           # Implementaciones concretas
│   ├── external/            # APIs externas (Telegram, YouTube)
│   ├── compression/         # Servicios de compresión
│   ├── storage/             # Almacenamiento de archivos
│   └── notifications/       # Sistema de notificaciones
├── interfaces/              # Interfaces y adaptadores
│   ├── controllers/         # Controladores de bot
│   ├── cli/                 # Interface de línea de comandos
│   └── web/                 # Interface web (futura)
├── shared/                  # Utilidades compartidas
│   ├── config/              # Configuración
│   ├── logging/             # Logging estructurado
│   ├── utils/               # Utilidades generales
│   └── patterns/            # Patrones de diseño
└── tests/                   # Tests completos
    ├── unit/                # Tests unitarios
    ├── integration/         # Tests de integración
    └── e2e/                 # Tests end-to-end
```

## 🚀 Características Mejoradas

### ✅ Características del Bot Original
- Compresión de audio (voz y archivos)
- Compresión de video y animaciones
- Descarga de videos de YouTube
- Notificaciones de progreso en tiempo real
- Reenvío de archivos comprimidos

### 🆕 Mejoras Arquitectónicas
- **Arquitectura Hexagonal**: Desacoplamiento completo del dominio
- **Patrón CQRS**: Separación de comandos y queries
- **Event-Driven Architecture**: Sistema de eventos asíncrono
- **Dependency Injection Container**: Inyección automática de dependencias
- **Repository Pattern**: Abstracción de almacenamiento
- **Factory Pattern**: Creación de objetos y estrategias
- **Observer Pattern**: Sistema de notificaciones flexible
- **Strategy Pattern**: Estrategias de compresión extensibles

### 🔧 Mejoras Técnicas
- **Type Hints**: Tipado completo en Python
- **Logging Estructurado**: Logs con contexto y métricas
- **Error Handling**: Manejo robusto de errores
- **Configuration Management**: Configuración por ambiente
- **Testing Suite**: Cobertura > 90%
- **Performance Monitoring**: Métricas y profiling
- **Async/Await**: Procesamiento asíncrono completo

## 📋 Requisitos

- Python 3.9+
- FFmpeg (para compresión de video)
- Redis (para cola de tareas)
- PostgreSQL (opcional, para persistencia)

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/RolanZanvel/CompressBot-Optimized.git
cd CompressBot-Optimized

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Ejecutar tests
pytest

# Iniciar el bot
python main.py
```

## ⚙️ Configuración

```env
# Telegram Configuration
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_BOT_TOKEN=your_bot_token

# Compression Configuration
COMPRESSION_QUALITY=high
MAX_FILE_SIZE_MB=100
TEMP_DIR=./temp

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json
```

## 🎯 Uso

### Interfaz de Línea de Comandos
```bash
# Iniciar bot
python main.py start

# Ver estado
python main.py status

# Probar compresión
python main.py test-compress --file input.mp4

# Ver logs
python main.py logs --follow
```

### Bot de Telegram
1. Envía un archivo de audio, video o un enlace de YouTube
2. Elige las opciones de compresión
3. Recibe el archivo comprimido con progreso en tiempo real

## 🔧 Extensión

### Añadir Nuevo Compresor

```python
# src/infrastructure/compression/image_compressor.py
from src.application.services.compression_service import ICompressionService

class ImageCompressionService(ICompressionService):
    def compress(self, input_path: str, output_path: str, options: CompressionOptions) -> CompressionResult:
        # Implementación de compresión de imágenes
        pass
    
    def supported_formats(self) -> List[str]:
        return ['.jpg', '.png', '.webp']
```

### Añadir Nueva Estrategia

```python
# src/infrastructure/compression/strategies/ultra_fast_strategy.py
from src.application.services.compression_strategy import ICompressionStrategy

class UltraFastStrategy(ICompressionStrategy):
    def get_parameters(self, media_type: MediaType) -> Dict[str, Any]:
        return {
            'preset': 'ultrafast',
            'crf': 28,
            'threads': 4
        }
    
    def get_description(self) -> str:
        return "⚡ Ultra Rápido (Compresión máxima)"
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Ejecutar solo tests unitarios
pytest tests/unit/

# Ejecutar con cobertura
pytest --cov=src --cov-report=html

# Ejecutar tests de integración
pytest tests/integration/
```

## 📊 Métricas y Monitoreo

El sistema incluye monitoreo integrado:

- **Métricas de rendimiento**: Tiempo de compresión, uso de CPU/memoria
- **Métricas de negocio**: Archivos procesados, tasa de éxito
- **Health Checks**: Verificación de servicios externos
- **Alerting**: Notificaciones de errores críticos

## 🔄 Flujo de Trabajo de Desarrollo

### 1. Entender el Contexto
- Revisar issues y epics asignados
- Leer documentación técnica
- Sincronizar con el equipo

### 2. Trabajar desde Rama Aislada
```bash
git checkout main
git pull origin main
git checkout -b feat/nueva-funcionalidad
```

### 3. Desarrollo Iterativo
- Commits pequeños y enfocados
- Mensajes convencionales
- Tests locales antes de push

### 4. Pull Request
```bash
git add .
git commit -m "feat: add new compression strategy"
git push origin feat/nueva-funcionalidad
```

### 5. Code Review
- Revisión respetuosa y constructiva
- Tests que pasen
- Documentación actualizada

## 🤝 Contribuir

1. Fork del repositorio
2. Crear rama de feature
3. Implementar con tests
4. Pull Request con descripción detallada

## 📄 Licencia

MIT License - ver archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- Proyecto original: [BotCompressor](https://github.com/RolanZamvel/BotCompressor)
- Principios SOLID: Robert C. Martin
- Clean Architecture: Uncle Bob

---

**Nota**: Esta es una refactorización completa aplicando principios de diseño de software enterprise-grade para máxima calidad y mantenibilidad.

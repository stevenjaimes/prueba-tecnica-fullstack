from flask_caching import Cache

# Configuración directa para desarrollo local
cache = Cache(config={
    'CACHE_TYPE': 'SimpleCache',  # Caché en memoria
    'CACHE_DEFAULT_TIMEOUT': 800  
})
import requests
from datetime import datetime
from flask import current_app
from app.infrastructure.external.stackexchange import StackExchangeConfig as Config
from typing import Dict, List, Any, Tuple, Optional

class StackExchangeService:
    """Servicio para interactuar con la API de Stack Exchange y procesar estadísticas de preguntas."""
    
    BASE_URL = Config.API_URL  # URL base de la API configurada externamente
    
    def __init__(self):
        """Inicializa el servicio con una sesión HTTP reutilizable."""
        self.session = requests.Session()
    
    def obtener_estadisticas(self, etiqueta: str = 'perl') -> Tuple[Dict[str, Any], int]:
        """Obtiene y procesa estadísticas de preguntas de Stack Overflow para una etiqueta específica.
        
        Args:
            etiqueta (str): Etiqueta para filtrar preguntas (default: 'perl')
            
        Returns:
            Tuple[Dict[str, Any], int]: Tupla con:
                - Dict: Estadísticas procesadas o mensaje de error
                - int: Código HTTP de respuesta
                
        Ejemplo de éxito:
            (
                {
                    "stats": {"total": 10, "contestadas": 8, "no_contestadas": 2},
                    "mayor_puntuacion": {...},
                    ...
                },
                200
            )
            
        Ejemplo de error:
            ({"error": "No se encontraron resultados"}, 404)
        """
        try:
            params = {
                'order': 'desc',
                'sort': 'activity',
                'intitle': etiqueta,
                'site': 'stackoverflow',
                'filter': '!9Z(-wzu0T'  # Filtro para campos específicos
            }
            
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()  # Lanza excepción para códigos 4XX/5XX
            data = response.json()
            
            if not data.get('items'):
                return {"error": "No se encontraron resultados"}, 404
            
            return self._procesar_respuesta(data['items']), 200
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error StackExchange API: {str(e)}")
            return {"error": "Error al consultar StackExchange"}, 503
    
    def _procesar_respuesta(self, preguntas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Procesa la lista de preguntas para extraer estadísticas clave.
        
        Args:
            preguntas (List[Dict]): Lista de preguntas de la API
            
        Returns:
            Dict[str, Any]: Diccionario con:
                - stats: Estadísticas generales
                - mayor_puntuacion: Pregunta con mayor score
                - menor_visitas: Pregunta con menos vistas
                - mas_antigua: Pregunta más antigua
                - mas_reciente: Pregunta más reciente
        """
        contestadas = sum(1 for p in preguntas if p.get('is_answered'))        

        mayor_punt = max(preguntas, key=lambda x: x.get('score', 0))        

        menor_visitas = min(preguntas, key=lambda x: x.get('view_count', float('inf')))        

        mas_antigua = min(preguntas, key=lambda x: x.get('creation_date', 0))

        mas_reciente = max(preguntas, key=lambda x: x.get('creation_date', 0))        

        self._log_console(mayor_punt, menor_visitas, mas_antigua, mas_reciente)
        
        return {
            "stats": {
                "total": len(preguntas),
                "contestadas": contestadas,
                "no_contestadas": len(preguntas) - contestadas
            },
            "mayor_puntuacion": self._formatear_pregunta(mayor_punt),
            "menor_visitas": self._formatear_pregunta(menor_visitas),
            "mas_antigua": self._formatear_pregunta(mas_antigua),
            "mas_reciente": self._formatear_pregunta(mas_reciente)
        }
    
    def _formatear_pregunta(self, pregunta: Dict[str, Any]) -> Dict[str, Any]:
        """Formatea los datos de una pregunta individual para la respuesta.
        
        Args:
            pregunta (Dict): Datos crudos de una pregunta de la API
            
        Returns:
            Dict: Pregunta formateada con campos estandarizados
        """
        return {
            "titulo": pregunta.get('title'),
            "score": pregunta.get('score'),
            "views": pregunta.get('view_count'),
            "link": pregunta.get('link'),
            "fecha": datetime.fromtimestamp(pregunta.get('creation_date')).isoformat()
        }
    
    def _log_console(self, *preguntas: Dict[str, Any]) -> None:
        """Imprime en consola los resultados clave (para debugging/registro).
        
        Args:
            *preguntas: Diccionarios con datos de preguntas relevantes
        """
        print("\n=== Resultados StackExchange ===")
        print(f"2. Mayor puntuación: {preguntas[0].get('title')} (Score: {preguntas[0].get('score')})")
        print(f"3. Menor visitas: {preguntas[1].get('title')} (Views: {preguntas[1].get('view_count')})")
        print(f"4. Más antigua: {preguntas[2].get('title')} ({datetime.fromtimestamp(preguntas[2].get('creation_date'))})")
        print(f"5. Más reciente: {preguntas[3].get('title')} ({datetime.fromtimestamp(preguntas[3].get('creation_date'))})")
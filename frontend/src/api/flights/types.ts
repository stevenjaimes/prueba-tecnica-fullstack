export interface Airline {
  id_aerolinea: number;     // Identificador único de la aerolínea
  nombre_aerolinea: string; // Nombre completo de la aerolínea (ej: "Aeroméxico")
}
  
  export interface Airport {
    id_aeropuerto: number;     // Identificador único del aeropuerto
    nombre_aeropuerto: string; // Nombre completo del aeropuerto (ej: "Aeropuerto Internacional de la Ciudad de México")
  }
  
  export interface Movement {
    id_movimiento: number; // Identificador único del tipo de movimiento
    descripcion: string;   // Tipo de movimiento (ej: "Salida" o "Llegada")
  }
  export interface Flight {
    id: number;             // Identificador único del vuelo
    id_aerolinea: number;   // Referencia a la aerolínea (relación con Airline)
    id_aeropuerto: number;  // Referencia al aeropuerto (relación con Airport)
    id_movimiento: number;  // Referencia al tipo de movimiento (relación con Movement)
    dia: string;            // Fecha del vuelo en formato ISO 8601 (YYYY-MM-DD)
  }
  
  export interface FlightMetrics {
    aeropuerto_mas_ocupado: Array<{
      id_aeropuerto: number;
      nombre_aeropuerto: string;
      total_movimientos: number;  // Cantidad total de movimientos (salidas + llegadas)
    }>;
    
    aerolinea_mas_ocupada: Array<{
      id_aerolinea: number;
      nombre_aerolinea: string;
      total_vuelos: number;       // Cantidad total de vuelos operados
    }>;
    
    dia_mas_ocupado: Array<{
      dia: string;                // Fecha en formato ISO 8601
      total_vuelos: number;       // Cantidad de vuelos en ese día
    }>;
    
    aerolineas_mas_de_dos_vuelos: Array<{
      id_aerolinea: number;
      nombre_aerolinea: string;
      total_vuelos: number;       // Vuelos totales (siempre > 2)
    }>;
  }
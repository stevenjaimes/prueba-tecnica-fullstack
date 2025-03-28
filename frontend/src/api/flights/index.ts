import axios from 'axios';
import { 
  Airline, 
  Airport, 
  Movement, 
  Flight, 
  FlightMetrics 
} from './types';

// ==================== URL BASE DE LA API ====================
// Debe ir en archivos de configuración o variables de entorno
// para producción, pero aquí se deja como localhost para desarrollo
const API_BASE_URL = 'http://localhost:5000/api';
// ==================== MÉTODOS API ====================

/**
 * Obtiene las métricas estadísticas de vuelos
 * @returns {Promise<FlightMetrics>} Objeto con estadísticas completas
 * @throws {Error} Error al obtener las métricas
 * 
 * @example
 * try {
 *   const metrics = await getFlightMetrics();
 *   console.log('Aeropuerto más activo:', metrics.aeropuerto_mas_ocupado[0]);
 * } catch (error) {
 *   console.error('Error obteniendo métricas:', error.message);
 * }
 */

export const getFlightMetrics = async (): Promise<FlightMetrics> => {
  const response = await axios.get(`${API_BASE_URL}/vuelos/metricas`);
  return response.data;
};

/**
 * Obtiene el listado completo de aerolíneas registradas
 * @returns {Promise<Airline[]>} Lista de aerolíneas
 * @throws {Error} Error al obtener las aerolíneas
 * 
 * @example
 * const airlines = await getAirlines();
 * console.log(`Total aerolíneas: ${airlines.length}`);
 */

export const getAirlines = async (): Promise<Airline[]> => {
  const response = await axios.get(`${API_BASE_URL}/aerolineas`);
  return response.data;
};

/**
 * Obtiene el listado completo de aeropuertos registrados
 * @returns {Promise<Airport[]>} Lista de aeropuertos
 * @throws {Error} Error al obtener los aeropuertos
 * 
 * @example
 * const airports = await getAirports();
 * const airportNames = airports.map(a => a.nombre_aeropuerto);
 */

export const getAirports = async (): Promise<Airport[]> => {
  const response = await axios.get(`${API_BASE_URL}/aeropuertos`);
  return response.data;
};

/**
 * Obtiene los tipos de movimiento disponibles
 * @returns {Promise<Movement[]>} Lista de movimientos (Salida/Llegada)
 * @throws {Error} Error al obtener los movimientos
 * 
 * @example
 * const movements = await getMovements();
 * console.log('Tipos de movimiento:', movements);
 */
export const getMovements = async (): Promise<Movement[]> => {
    const response = await fetch(`${API_BASE_URL}/movimientos`);
    if (!response.ok) throw new Error('Error al obtener los movimientos');
    return response.json();
  };


/**
 * Obtiene el listado completo de vuelos registrados
 * @returns {Promise<Flight[]>} Lista de vuelos con sus detalles
 * @throws {Error} Error al obtener los vuelos
 * 
 * @example
 * const flights = await getFlights();
 * console.log('Vuelos hoy:', flights.filter(f => f.dia === new Date().toISOString()));
 */
export const getFlights = async (): Promise<Flight[]> => {
    const response = await fetch(`${API_BASE_URL}/vuelos`);
    if (!response.ok) throw new Error('Error al obtener los vuelos');
    return response.json();
  };
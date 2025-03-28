import axios from 'axios';
import { StackExchangeResponse } from './types';

//
// ==================== URL BASE DE LA API ====================
// Debe ir en archivos de configuración o variables de entorno
// para producción, pero aquí se deja como localhost para desarrollo
const API_BASE_URL = 'http://localhost:5000/api';


/**
 * Obtiene estadísticas de StackExchange para una etiqueta específica
 * @async
 * @function getStackExchangeStats
 * @param {string} [tag='perl'] - Etiqueta a buscar (default: 'perl')
 * @returns {Promise<StackExchangeResponse>} Objeto con estadísticas
 * @throws {Error} Cuando:
 * - La respuesta está vacía
 * - La respuesta no tiene el formato esperado
 * - Hay errores de red o del servidor
 * 
 * @example
 * try {
 *   const stats = await getStackExchangeStats('javascript');
 *   console.log(stats.mayor_puntuacion);
 * } catch (error) {
 *   console.error('Error:', error.message);
 * }
 */
export const getStackExchangeStats = async (tag: string = 'perl'): Promise<StackExchangeResponse> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/stackexchange/stats?etiqueta=${tag}`);
    
    // Validación de respuesta
    if (!response.data) {
      throw new Error('La respuesta del servidor está vacía');
    }

    // Validación de estructura
    if (!response.data.stats || !response.data.mayor_puntuacion) {
      throw new Error('La respuesta no tiene el formato esperado');
    }

    return response.data;
  } catch (error) {
    console.error('Error al obtener estadísticas:', error);
    throw error;     // Re-lanzamos el error para manejo externo
  }
};
import React from 'react';
import { Flight, Airline, Airport, Movement } from '../../api/flights/types';

/**
 * Componente que muestra una tabla interactiva de vuelos con información relacionada.
 * 
 * Características principales:
 * - Tabla responsive con capacidad para grandes volúmenes de datos
 * - Integración de datos de aerolíneas, aeropuertos y movimientos
 * - Formateo profesional de fechas
 * - Visualización diferenciada de salidas/llegadas
 * - Diseño accesible y moderno
 * 
 * @component
 * @param {Object} props - Propiedades del componente
 * @param {Flight[]} props.flights - Lista de vuelos a mostrar
 * @param {Airline[]} props.airlines - Lista de aerolíneas para referencia
 * @param {Airport[]} props.airports - Lista de aeropuertos para referencia
 * @param {Movement[]} props.movements - Lista de tipos de movimiento
 * 
 * @example
 * const flights = [...];
 * const airlines = [...];
 * const airports = [...];
 * const movements = [...];
 * 
 * return (
 *   <FlightsTable 
 *     flights={flights}
 *     airlines={airlines}
 *     airports={airports}
 *     movements={movements}
 *   />
 * );
 */

interface FlightsTableProps {
  flights: Flight[];
  airlines: Airline[];
  airports: Airport[];
  movements: Movement[];
}

export const FlightsTable: React.FC<FlightsTableProps> = ({ 
  flights, 
  airlines, 
  airports, 
  movements 
}) => {

    /**
   * Obtiene el nombre de una aerolínea basado en su ID
   * @param {number} id - ID de la aerolínea
   * @returns {string} Nombre de la aerolínea o 'Desconocida'
   */

  const getAirlineName = (id: number): string => {
    const airline = airlines.find(a => a.id_aerolinea === id);
    return airline?.nombre_aerolinea || 'Desconocida';
  };

    /**
   * Obtiene el nombre de un aeropuerto basado en su ID
   * @param {number} id - ID del aeropuerto
   * @returns {string} Nombre del aeropuerto o 'Desconocido'
   */

  const getAirportName = (id: number): string => {
    const airport = airports.find(a => a.id_aeropuerto === id);
    return airport?.nombre_aeropuerto || 'Desconocido';
  };

    /**
   * Obtiene la descripción de un movimiento basado en su ID
   * @param {number} id - ID del movimiento
   * @returns {string} Descripción del movimiento o 'Desconocido'
   */
  const getMovementDescription = (id: number): string => {
    const movement = movements.find(m => m.id_movimiento === id);
    return movement?.descripcion || 'Desconocido';
  };

   /**
   * Formatea una fecha ISO a formato legible en español
   * @param {string} dateString - Fecha en formato ISO (YYYY-MM-DD)
   * @returns {string} Fecha formateada (ej: "lunes, 1 de enero de 2023")
   */
  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('es-ES', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden">
      <div className="p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Listado de Vuelos</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Aerolínea</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Aeropuerto</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {flights.map((flight) => {
                const movementType = getMovementDescription(flight.id_movimiento);
                const isDeparture = movementType === 'Salida';
                
                return (
                  <tr key={flight.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {flight.id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {getAirlineName(flight.id_aerolinea)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {getAirportName(flight.id_aeropuerto)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                        ${isDeparture ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'}`}>
                        {movementType}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatDate(flight.dia)}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
import React from 'react';
import { FlightMetrics } from '../../api/flights/types';
import { FaPlane, FaPlaneDeparture, FaCalendarAlt, FaChartBar } from 'react-icons/fa';

/**
 * Componente que muestra las principales métricas de vuelos en tarjetas visuales.
 * 
 * Características principales:
 * - Muestra 4 categorías de métricas en tarjetas independientes
 * - Diseño responsive con sombras y bordes redondeados
 * - Iconografía descriptiva para cada sección
 * - Manejo de empates en las métricas
 * - Formateo de fechas legible
 * 
 * @component
 * @param {Object} props - Propiedades del componente
 * @param {FlightMetrics} props.metrics - Objeto con todas las métricas de vuelos
 * 
 * @example
 * const metrics = {
 *   aeropuerto_mas_ocupado: [{ nombre_aeropuerto: "MEX", total_movimientos: 120 }],
 *   aerolinea_mas_ocupada: [{ nombre_aerolinea: "Aeroméxico", total_vuelos: 85 }],
 *   dia_mas_ocupado: [{ dia: "2023-01-01", total_vuelos: 200 }],
 *   aerolineas_mas_de_dos_vuelos: [
 *     { nombre_aerolinea: "Volaris", total_vuelos: 3 },
 *     { nombre_aerolinea: "VivaAerobus", total_vuelos: 4 }
 *   ]
 * };
 * 
 * return <FlightMetricsCard metrics={metrics} />;
 */
export const FlightMetricsCard: React.FC<{ metrics: FlightMetrics }> = ({ metrics }) => {
  return (
    <div className="space-y-8">
      {/* Tarjeta: Aeropuerto(s) más ocupado(s) */}
      <div className="bg-white rounded-xl shadow-md overflow-hidden">
        <div className="p-6">
          <div className="flex items-center mb-4">
            <div className="p-3 rounded-full bg-blue-100 text-blue-600 mr-4">
              <FaPlane className="text-xl" />
            </div>
            <h2 className="text-xl font-semibold text-gray-800">
              {metrics.aeropuerto_mas_ocupado?.length > 1 
                ? "Aeropuertos con Mayor Movimiento" 
                : "Aeropuerto con Mayor Movimiento"}
            </h2>
          </div>
          <div className="pl-16">
            {metrics.aeropuerto_mas_ocupado?.length > 0 ? (
              <div className="space-y-4">
                {metrics.aeropuerto_mas_ocupado.map((aeropuerto, index) => (
                  <div key={index}>
                    <p className="text-2xl font-bold text-gray-900">
                      {aeropuerto.nombre_aeropuerto}
                    </p>
                    <p className="text-lg text-gray-600">
                      <span className="font-semibold">{aeropuerto.total_movimientos}</span> movimientos totales
                    </p>
                    {index < metrics.aeropuerto_mas_ocupado.length - 1 && (
                      <hr className="my-3 border-gray-200" />
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-lg text-gray-600">No hay datos de aeropuertos</p>
            )}
          </div>
        </div>
      </div>

      {/* Tarjeta: Aerolínea(s) con más vuelos */}
      <div className="bg-white rounded-xl shadow-md overflow-hidden">
        <div className="p-6">
          <div className="flex items-center mb-4">
            <div className="p-3 rounded-full bg-green-100 text-green-600 mr-4">
              <FaChartBar className="text-xl" />
            </div>
            <h2 className="text-xl font-semibold text-gray-800">
              {metrics.aerolinea_mas_ocupada?.length > 1 
                ? "Aerolíneas con Más Vuelos" 
                : "Aerolínea con Más Vuelos"}
            </h2>
          </div>
          <div className="pl-16">
            {metrics.aerolinea_mas_ocupada?.length > 0 ? (
              <div className="space-y-4">
                {metrics.aerolinea_mas_ocupada.map((aerolinea, index) => (
                  <div key={index}>
                    <p className="text-2xl font-bold text-gray-900">
                      {aerolinea.nombre_aerolinea}
                    </p>
                    <p className="text-lg text-gray-600">
                      <span className="font-semibold">{aerolinea.total_vuelos}</span> vuelos realizados
                    </p>
                    {index < metrics.aerolinea_mas_ocupada.length - 1 && (
                      <hr className="my-3 border-gray-200" />
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-lg text-gray-600">No hay datos de aerolíneas</p>
            )}
          </div>
        </div>
      </div>

      {/* Tarjeta: Día(s) con más vuelos */}
      <div className="bg-white rounded-xl shadow-md overflow-hidden">
        <div className="p-6">
          <div className="flex items-center mb-4">
            <div className="p-3 rounded-full bg-purple-100 text-purple-600 mr-4">
              <FaCalendarAlt className="text-xl" />
            </div>
            <h2 className="text-xl font-semibold text-gray-800">Día con Mayor Tráfico Aéreo</h2>
          </div>
          <div className="pl-16">
            {metrics.dia_mas_ocupado?.length > 0 ? (
              <div className="space-y-4">
                {metrics.dia_mas_ocupado.map((dia, index) => (
                  <div key={index}>
                    <p className="text-2xl font-bold text-gray-900">
                      {new Date(dia.dia).toLocaleDateString('es-ES', { 
                        weekday: 'long', 
                        year: 'numeric', 
                        month: 'long', 
                        day: 'numeric' 
                      })}
                    </p>
                    <p className="text-lg text-gray-600">
                      <span className="font-semibold">{dia.total_vuelos}</span> vuelos registrados
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-lg text-gray-600">No hay datos de días</p>
            )}
          </div>
        </div>
      </div>

      {/* Tarjeta: Aerolíneas con más de 2 vuelos (en tabla) */}
      <div className="bg-white rounded-xl shadow-md overflow-hidden">
        <div className="p-6">
          <div className="flex items-center mb-4">
            <div className="p-3 rounded-full bg-yellow-100 text-yellow-600 mr-4">
              <FaPlaneDeparture className="text-xl" />
            </div>
            <h2 className="text-xl font-semibold text-gray-800">Aerolíneas con Más de 2 Vuelos</h2>
          </div>
          <div className="pl-16">
            {metrics.aerolineas_mas_de_dos_vuelos?.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Aerolínea</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total de Vuelos</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {metrics.aerolineas_mas_de_dos_vuelos.map((aerolinea, index) => (
                      <tr key={index}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {aerolinea.nombre_aerolinea}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {aerolinea.total_vuelos}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-lg text-gray-600">No hay aerolíneas con más de 2 vuelos</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
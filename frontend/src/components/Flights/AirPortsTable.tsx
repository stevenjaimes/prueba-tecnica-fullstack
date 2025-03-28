import React from 'react';
import { Airport } from '../../api/flights/types';
import { FaMapMarkerAlt } from 'react-icons/fa';

/**
 * Componente que muestra una tabla de aeropuertos con diseño responsive y estilizado.
 * 
 * Características principales:
 * - Tarjeta con sombra y bordes redondeados
 * - Encabezado con icono de ubicación
 * - Tabla adaptable a diferentes tamaños de pantalla
 * - Efecto hover en filas para mejor interacción
 * - Muestra ID y nombre de cada aeropuerto
 * 
 * @component
 * @param {Object} props - Propiedades del componente
 * @param {Airport[]} props.airports - Array de objetos Airport a mostrar
 * 
 * @example
 * const airports = [
 *   { id_aeropuerto: 1, nombre_aeropuerto: "Aeropuerto Internacional de la Ciudad de México" },
 *   { id_aeropuerto: 2, nombre_aeropuerto: "Aeropuerto Internacional de Cancún" }
 * ];
 * 
 * return <AirportsTable airports={airports} />;
 */
export const AirportsTable: React.FC<{ airports: Airport[] }> = ({ airports }) => {
  return (
    <div className="bg-white shadow-md rounded-xl overflow-hidden">
      {/* Encabezado de la tarjeta con icono */}
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-xl font-semibold text-gray-800 flex items-center">
          <FaMapMarkerAlt className="mr-2 text-green-500" />
          Aeropuertos Registrados
        </h2>
      </div>
      
      {/* Contenedor de tabla responsive */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          {/* Cabecera de la tabla */}
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                ID
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Nombre
              </th>
            </tr>
          </thead>
          
          {/* Cuerpo de la tabla */}
          <tbody className="bg-white divide-y divide-gray-200">
            {airports.map((airport) => (
              <tr 
                key={airport.id_aeropuerto} 
                className="hover:bg-gray-50 transition-colors duration-150"
              >
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {airport.id_aeropuerto}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {airport.nombre_aeropuerto}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
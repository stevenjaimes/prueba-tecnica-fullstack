import React from 'react';
import { Airline } from '../../api/flights/types';
import { FaPlane } from 'react-icons/fa';

/**
 * Componente que muestra una tabla de aerolíneas con estilo responsive.
 * 
 * Características principales:
 * - Diseño con sombra y bordes redondeados
 * - Header con icono descriptivo
 * - Tabla responsive con hover effects
 * - Muestra ID y nombre de cada aerolínea
 * 
 * @component
 * @param {Object} props - Propiedades del componente
 * @param {Airline[]} props.airlines - Array de aerolíneas a mostrar
 * 
 * @example
 * const airlines = [
 *   { id_aerolinea: 1, nombre_aerolinea: "Aeroméxico" },
 *   { id_aerolinea: 2, nombre_aerolinea: "Volaris" }
 * ];
 * 
 * return <AirlinesTable airlines={airlines} />;
 */
export const AirlinesTable: React.FC<{ airlines: Airline[] }> = ({ airlines }) => {
  return (
    <div className="bg-white shadow-md rounded-xl overflow-hidden">
      {/* Encabezado de la tarjeta */}
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-xl font-semibold text-gray-800 flex items-center">
          <FaPlane className="mr-2 text-blue-500" />
          Aerolíneas Registradas
        </h2>
      </div>
      
      {/* Tabla responsive */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {airlines.map((airline) => (
              <tr key={airline.id_aerolinea} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {airline.id_aerolinea}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {airline.nombre_aerolinea}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
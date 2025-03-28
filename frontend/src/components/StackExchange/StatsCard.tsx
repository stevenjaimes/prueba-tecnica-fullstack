import React from 'react';
import { StackExchangeResponse } from '../../api/stackExchange/types';
import { Card } from '../UI/Card';
import { Error } from '../UI/Error';
import { FaCheckCircle, FaTimesCircle, FaChartLine, FaEye, FaCalendarAlt, FaExternalLinkAlt } from 'react-icons/fa';

interface StatsCardProps {
    data: StackExchangeResponse | null;     // Datos estadísticos de StackExchange
}

/**
 * Formatea una fecha ISO a formato legible en español
 * @param {string} dateString - Fecha en formato ISO
 * @returns {string} Fecha formateada (ej: "1 ene. 2023")
 * @throws {Error} Si la fecha no puede ser parseada
 */

const formatDate = (dateString: string): string => {
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    } catch (e) {
        console.error('Error formateando fecha:', dateString, e);
        return dateString;
    }
};

/**
 * Componente StatsCard - Muestra estadísticas de StackExchange en tarjetas visuales
 * @param {StatsCardProps} props - Propiedades del componente
 * @returns {JSX.Element} - Tarjetas con estadísticas o mensaje de error
 */
export const StatsCard: React.FC<StatsCardProps> = ({ data }) => {
    if (!data) {
        return <Error message="No se encontraron datos para mostrar" />;
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Card 1: Estadísticas generales */}
            <Card className="hover:shadow-lg transition-shadow duration-300">
                <div className="flex items-center space-x-3 mb-4">
                    <div className="p-2 rounded-full bg-blue-100 text-blue-600">
                        <FaChartLine className="text-xl" />
                    </div>
                    <h3 className="text-xl font-semibold text-gray-800">Resumen de preguntas</h3>
                </div>

                <div className="space-y-4">
                    <div className="flex justify-between items-center p-3 bg-green-50 rounded-lg">
                        <div>
                            <p className="text-green-700 font-medium flex items-center">
                                <FaCheckCircle className="mr-2" /> Contestadas
                            </p>
                            <p className="text-sm text-gray-600 ml-6">
                                {Math.round((data.stats.contestadas / data.stats.total) * 100)}% del total
                            </p>
                        </div>
                        <span className="text-2xl font-bold text-green-600">
                            {data.stats.contestadas}
                        </span>
                    </div>

                    <div className="flex justify-between items-center p-3 bg-red-50 rounded-lg">
                        <div>
                            <p className="text-red-700 font-medium flex items-center">
                                <FaTimesCircle className="mr-2" /> No contestadas
                            </p>
                            <p className="text-sm text-gray-600 ml-6">
                                {Math.round((data.stats.no_contestadas / data.stats.total) * 100)}% del total
                            </p>
                        </div>
                        <span className="text-2xl font-bold text-red-600">
                            {data.stats.no_contestadas}
                        </span>
                    </div>

                    <div className="pt-3 border-t border-gray-200 text-center">
                        <p className="font-medium text-gray-700">
                            Total: <span className="text-blue-600">{data.stats.total}</span> preguntas
                        </p>
                    </div>
                </div>
            </Card>

            {/* Card 2: Pregunta con mayor puntuación */}
            <Card className="hover:shadow-lg transition-shadow duration-300">
                <div className="flex items-center space-x-3 mb-4">
                    <div className="p-2 rounded-full bg-purple-100 text-purple-600">
                        <FaChartLine className="text-xl" />
                    </div>
                    <h3 className="text-xl font-semibold text-gray-800">Top Puntuación</h3>
                </div>

                <div className="space-y-3">
                    <h3 className="font-medium text-lg line-clamp-2 text-gray-800">
                        {data.mayor_puntuacion.titulo}
                    </h3>

                    <div className="flex flex-wrap gap-4 mt-2">
                        <div className="flex items-center text-blue-600">
                            <span className="font-semibold mr-2">Puntos:</span>
                            <span className="bg-blue-100 px-2 py-1 rounded-md">
                                {data.mayor_puntuacion.score}
                            </span>
                        </div>
                        <div className="flex items-center text-purple-600">
                            <FaEye className="mr-1" />
                            <span className="font-semibold mr-2">Vistas:</span>
                            <span className="bg-purple-100 px-2 py-1 rounded-md">
                                {data.mayor_puntuacion.views}
                            </span>
                        </div>
                    </div>

                    <div className="flex items-center text-sm text-gray-500 mt-2">
                        <FaCalendarAlt className="mr-1" />
                        {formatDate(data.mayor_puntuacion.fecha)}
                    </div>

                    <a
                        href={data.mayor_puntuacion.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center mt-3 text-blue-500 hover:text-blue-700 transition-colors"
                    >
                        Ver pregunta <FaExternalLinkAlt className="ml-1 text-sm" />
                    </a>
                </div>
            </Card>

            {/* Card 3: Pregunta con menos visitas */}
            <Card className="hover:shadow-lg transition-shadow duration-300">
                <div className="flex items-center space-x-3 mb-4">
                    <div className="p-2 rounded-full bg-yellow-100 text-yellow-600">
                        <FaEye className="text-xl" />
                    </div>
                    <h3 className="text-xl font-semibold text-gray-800">Menos Visitas</h3>
                </div>

                <div className="space-y-3">
                    <h3 className="font-medium text-lg line-clamp-2 text-gray-800">
                        {data.menor_visitas.titulo}
                    </h3>

                    <div className="flex flex-wrap gap-4 mt-2">
                        <div className="flex items-center text-blue-600">
                            <span className="font-semibold mr-2">Puntos:</span>
                            <span className="bg-blue-100 px-2 py-1 rounded-md">
                                {data.menor_visitas.score}
                            </span>
                        </div>
                        <div className="flex items-center text-purple-600">
                            <FaEye className="mr-1" />
                            <span className="font-semibold mr-2">Vistas:</span>
                            <span className="bg-purple-100 px-2 py-1 rounded-md">
                                {data.menor_visitas.views}
                            </span>
                        </div>
                    </div>

                    <div className="flex items-center text-sm text-gray-500 mt-2">
                        <FaCalendarAlt className="mr-1" />
                        {formatDate(data.menor_visitas.fecha)}
                    </div>

                    <a
                        href={data.menor_visitas.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center mt-3 text-blue-500 hover:text-blue-700 transition-colors"
                    >
                        Ver pregunta <FaExternalLinkAlt className="ml-1 text-sm" />
                    </a>
                </div>
            </Card>

            {/* Card 4: Preguntas destacadas */}
            <Card className="hover:shadow-lg transition-shadow duration-300">
                <div className="flex items-center space-x-3 mb-4">
                    <div className="p-2 rounded-full bg-indigo-100 text-indigo-600">
                        <FaCalendarAlt className="text-xl" />
                    </div>
                    <h3 className="text-xl font-semibold text-gray-800">Histórico</h3>
                </div>

                <div className="space-y-4">
                    <div className="bg-gray-50 p-3 rounded-lg">
                        <h4 className="font-medium text-gray-800 flex items-center">
                            <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                            Más antigua
                        </h4>
                        <p className="line-clamp-2 text-gray-700 mt-1">
                            {data.mas_antigua.titulo}
                        </p>
                        <div className="flex justify-between items-center mt-2 text-sm text-gray-500">
                            <span className="flex items-center">
                                <FaCalendarAlt className="mr-1" />
                                {formatDate(data.mas_antigua.fecha)}
                            </span>
                            <span className="flex items-center">
                                <FaEye className="mr-1" />
                                {data.mas_antigua.views}
                            </span>
                        </div>
                        <a
                            href={data.mas_antigua.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center mt-2 text-sm text-blue-500 hover:text-blue-700"
                        >
                            Ver <FaExternalLinkAlt className="ml-1 text-xs" />
                        </a>
                    </div>

                    <div className="bg-gray-50 p-3 rounded-lg">
                        <h4 className="font-medium text-gray-800 flex items-center">
                            <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                            Más reciente
                        </h4>
                        <p className="line-clamp-2 text-gray-700 mt-1">
                            {data.mas_reciente.titulo}
                        </p>
                        <div className="flex justify-between items-center mt-2 text-sm text-gray-500">
                            <span className="flex items-center">
                                <FaCalendarAlt className="mr-1" />
                                {formatDate(data.mas_reciente.fecha)}
                            </span>
                            <span className="flex items-center">
                                <FaEye className="mr-1" />
                                {data.mas_reciente.views}
                            </span>
                        </div>
                        <a
                            href={data.mas_reciente.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center mt-2 text-sm text-blue-500 hover:text-blue-700"
                        >
                            Ver <FaExternalLinkAlt className="ml-1 text-xs" />
                        </a>
                    </div>
                </div>
            </Card>
        </div>
    );
};
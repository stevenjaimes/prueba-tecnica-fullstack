import React, { useState, useEffect } from 'react';
import {
    getFlightMetrics,
    getAirlines,
    getAirports,
    getFlights,
    getMovements
} from '../api/flights/index';
import { FlightMetricsCard } from '../components/Flights/FlightMetricsCard';
import { AirlinesTable } from '../components/Flights/AirlinesTable';
import { AirportsTable } from '../components/Flights/AirPortsTable';
import { FlightsTable } from '../components/Flights/FlightsTable';
import { Loading } from '../components/UI/Loading';
import { Error } from '../components/UI/Error';
import { FlightMetrics, Airline, Airport, Flight, Movement } from '../api/flights/types';

/**
 * Página principal que muestra estadísticas y datos de vuelos en México.
 * 
 * Funcionalidades principales:
 * - Muestra métricas clave de vuelos
 * - Lista de aerolíneas, aeropuertos y vuelos
 * - Sistema de pestañas para navegar entre secciones
 * - Manejo de estados de carga y errores
 * 
 * @component
 * @example
 * return <FlightsPage />
 */
export const FlightsPage: React.FC = () => {
    // Estados para almacenar los datos
    const [metrics, setMetrics] = useState<FlightMetrics | null>(null);
    const [airlines, setAirlines] = useState<Airline[]>([]);
    const [airports, setAirports] = useState<Airport[]>([]);
    const [flights, setFlights] = useState<Flight[]>([]);
    const [movements, setMovements] = useState<Movement[]>([]);
    
    // Estados para manejar la UI
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [activeTab, setActiveTab] = useState('metrics');

    /**
     * Efecto para cargar los datos al montar el componente
     * 
     * Realiza múltiples peticiones en paralelo usando Promise.all
     * Maneja errores individualmente para cada petición
     * Actualiza los estados correspondientes
     */
    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                setError(null);

                // Carga inicial de datos esenciales
                const [metricsRes, airlinesRes, airportsRes] = await Promise.all([
                    getFlightMetrics(),
                    getAirlines(),
                    getAirports()
                ]);

                setMetrics(metricsRes);
                setAirlines(airlinesRes);
                setAirports(airportsRes);

                // Carga opcional de vuelos (maneja errores individualmente)
                try {
                    const flightsRes = await getFlights();
                    setFlights(flightsRes);
                } catch (flightsError) {
                    console.error('Error loading flights:', flightsError);
                    setFlights([]);
                }

                // Carga opcional de movimientos (maneja errores individualmente)
                try {
                    const movementsRes = await getMovements();
                    setMovements(movementsRes);
                } catch (movementsError) {
                    console.error('Error loading movements:', movementsError);
                    setMovements([]);
                }

            } catch (err) {
                // Manejo de errores generales
                const errorMessage = typeof err === 'object' && err !== null && 'message' in err
                    ? (err as { message: string }).message
                    : 'Error al cargar los datos';
                setError(errorMessage);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    // Estados de carga y error
    if (loading) return <Loading />;
    if (error) return <Error message={error} />;

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-6">Estadísticas de Vuelos en México</h1>

            {/* Sistema de pestañas para navegación */}
            <div className="mb-8 border-b border-gray-200">
                <nav className="flex space-x-8">
                    <button
                        onClick={() => setActiveTab('metrics')}
                        className={`py-4 px-1 font-medium text-sm border-b-2 ${activeTab === 'metrics' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
                    >
                        Métricas Clave
                    </button>
                    <button
                        onClick={() => setActiveTab('flights')}
                        className={`py-4 px-1 font-medium text-sm border-b-2 ${activeTab === 'flights' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
                    >
                        Vuelos
                    </button>
                    <button
                        onClick={() => setActiveTab('airlines')}
                        className={`py-4 px-1 font-medium text-sm border-b-2 ${activeTab === 'airlines' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
                    >
                        Aerolíneas
                    </button>
                    <button
                        onClick={() => setActiveTab('airports')}
                        className={`py-4 px-1 font-medium text-sm border-b-2 ${activeTab === 'airports' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
                    >
                        Aeropuertos
                    </button>
                </nav>
            </div>

            {/* Contenido dinámico basado en la pestaña activa */}
            {activeTab === 'metrics' && metrics && <FlightMetricsCard metrics={metrics} />}
            {activeTab === 'flights' && (
                <FlightsTable
                    flights={flights}
                    airlines={airlines}
                    airports={airports}
                    movements={movements}
                />
            )}
            {activeTab === 'airlines' && <AirlinesTable airlines={airlines} />}
            {activeTab === 'airports' && <AirportsTable airports={airports} />}
        </div>
    );
};
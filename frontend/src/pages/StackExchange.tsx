import React, { useState, useEffect, useCallback } from 'react';
import { getStackExchangeStats } from '../api/stackExchange';
import { SearchControl, StatsCard } from '../components/StackExchange';
import { Error } from '../components/UI/Error';
import { StackExchangeResponse } from '../api/stackExchange/types';
import { SkeletonLoader } from '../components/UI/SkeletonLoader';

type ApiError = {
    message: string;
    [key: string]: unknown;
};

export const StackExchangePage: React.FC = () => {
    const [data, setData] = useState<StackExchangeResponse | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [currentTag, setCurrentTag] = useState<string>('perl');

    const fetchStats = useCallback(async (tag: string) => {
        try {
            setLoading(true);
            setError(null);
            const response = await getStackExchangeStats(tag);
            setData(response);

        } catch (err) {
            let errorMessage = 'Error al cargar los datos';
            if (err instanceof Error) {
                errorMessage = (err as ApiError).message;
            } else if (typeof err === 'object' && err !== null && 'message' in err) {
                errorMessage = String((err as ApiError).message);
            }

            setError(errorMessage);

        } finally {
            setLoading(false);
        }
    }, []);


    useEffect(() => {
        fetchStats(currentTag);
    }, [fetchStats, currentTag]);

    return (
        <div className="container mx-auto px-4 py-8">
            {/* Mostrar skeleton solo en la carga inicial */}

            <>
                {/* Sección de cabecera */}
                <div className="mb-8">
                    <h2 className="text-2xl font-bold text-gray-800 mb-2">
                        Estadísticas de StackExchange
                    </h2>
                    <p className="text-gray-600 mb-4">
                        Mostrando resultados para: <span className="font-semibold">{currentTag}</span>
                    </p>

                    <SearchControl
                        initialTag={currentTag}
                        onDebouncedSearch={setCurrentTag}
                    />
                </div>

                {/* Renderizado condicional del contenido */}
                {loading ? (
                    <SkeletonLoader />
                ) : error ? (
                    <Error message={error} />
                ) : (
                    <StatsCard data={data} />
                )}
            </>

        </div>
    );
};
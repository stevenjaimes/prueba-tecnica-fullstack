import React from 'react';

/**
 * Componente SkeletonLoader para mostrar mientras se cargan los datos
 * 
 * @component
 * @example
 * return <SkeletonLoader />
 */
export const SkeletonLoader: React.FC = () => {
    return (
        <div className="animate-pulse space-y-6">
            {/* Encabezado */}
            <div className="space-y-4">
                <div className="h-8 bg-gray-200 rounded w-3/4"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2"></div>
            </div>
            
            {/* Barra de búsqueda */}
            <div className="h-12 bg-gray-200 rounded"></div>
            
            {/* Tarjetas de estadísticas */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[...Array(4)].map((_, index) => (
                    <div key={index} className="p-6 bg-white rounded-lg shadow">
                        <div className="h-5 bg-gray-200 rounded w-1/2 mb-4"></div>
                        <div className="h-8 bg-gray-200 rounded w-3/4 mb-2"></div>
                        <div className="h-4 bg-gray-200 rounded w-full"></div>
                    </div>
                ))}
            </div>
        </div>
    );
};
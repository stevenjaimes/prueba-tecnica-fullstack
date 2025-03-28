import React, { useState, useEffect, useRef } from 'react';
import { FaSearch, FaTimes } from 'react-icons/fa';

/**
 * Propiedades del componente SearchControl
 * @interface SearchControlProps
 * @property {string} initialTag - Etiqueta inicial de búsqueda
 * @property {(tag: string) => void} onDebouncedSearch - Callback que se ejecuta al realizar una búsqueda (con debounce)
 */
interface SearchControlProps {
  initialTag: string;
  onDebouncedSearch: (tag: string) => void;
}

/**
 * Componente de búsqueda con debounce y funcionalidad de limpieza
 * 
 * Características principales:
 * - Campo de búsqueda con estilos interactivos
 * - Debounce automático (1 segundo)
 * - Soporte para búsqueda con Enter
 * - Botón para limpiar búsqueda
 * - Indicador visual de la búsqueda actual
 * - Efectos visuales al enfocar/desenfocar
 * 
 * @component
 * @param {SearchControlProps} props - Propiedades del componente
 * 
 * @example
 * const [tag, setTag] = useState('javascript');
 * 
 * return (
 *   <SearchControl 
 *     initialTag={tag}
 *     onDebouncedSearch={setTag}
 *   />
 * );
 */
export const SearchControl: React.FC<SearchControlProps> = ({ 
  initialTag,
  onDebouncedSearch
}) => {
  // Estados del componente
  const [inputValue, setInputValue] = useState(initialTag);
  const [isFocused, setIsFocused] = useState(false);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  /**
   * Maneja el cambio en el input con debounce
   * @param {React.ChangeEvent<HTMLInputElement>} e - Evento de cambio
   */
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setInputValue(value);

    // Reinicia el debounce anterior
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }

    // Configura nuevo debounce
    debounceRef.current = setTimeout(() => {
      onDebouncedSearch(value.trim() || initialTag);
    }, 1000);
  };

  /**
   * Maneja la tecla Enter para búsqueda inmediata
   * @param {React.KeyboardEvent} e - Evento de teclado
   */
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      if (debounceRef.current) {
        clearTimeout(debounceRef.current);
      }
      onDebouncedSearch(inputValue.trim() || initialTag);
    }
  };

  /**
   * Limpia el input y restablece la búsqueda inicial
   */
  const clearInput = () => {
    setInputValue('');
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }
    onDebouncedSearch(initialTag);
  };

  // Limpieza del debounce al desmontar
  useEffect(() => {
    return () => {
      if (debounceRef.current) {
        clearTimeout(debounceRef.current);
      }
    };
  }, []);

  return (
    <div className="mb-8">
      <div className="relative max-w-2xl mx-auto">
        {/* Etiqueta accesible para screen readers */}
        <label htmlFor="search-input" className="sr-only">Buscar por etiqueta</label>
        
        {/* Contenedor del input con estilos dinámicos */}
        <div className={`flex items-center px-4 py-3 rounded-xl border-2 transition-all duration-300 ${
          isFocused 
            ? 'border-blue-500 shadow-lg bg-white' 
            : 'border-gray-200 bg-gray-50 hover:bg-white'
        }`}>
          {/* Icono de búsqueda con color dinámico */}
          <FaSearch className={`text-lg mr-3 transition-colors ${
            isFocused ? 'text-blue-500' : 'text-gray-400'
          }`} />
          
          {/* Input de búsqueda principal */}
          <input
            id="search-input"
            type="text"
            value={inputValue}
            onChange={handleChange}
            onKeyDown={handleKeyPress}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            className="flex-1 bg-transparent outline-none text-gray-700 placeholder-gray-400"
            placeholder="Buscar por etiqueta (ej: python, javascript)"
            aria-label="Campo de búsqueda por etiqueta"
          />
          
          {/* Botón para limpiar búsqueda (solo visible con texto) */}
          {inputValue && (
            <button 
              onClick={clearInput}
              className="ml-2 p-1 rounded-full text-gray-400 hover:text-gray-600 transition-colors"
              aria-label="Limpiar búsqueda"
            >
              <FaTimes />
            </button>
          )}
        </div>
        
        {/* Indicador de búsqueda actual */}
        <div className="mt-2 text-sm text-gray-500 text-center">
          {inputValue ? (
            <span>Buscando: <span className="font-semibold text-blue-600">{inputValue || initialTag}</span></span>
          ) : (
            <span>Mostrando resultados para: <span className="font-semibold text-blue-600">{initialTag}</span></span>
          )}
        </div>
      </div>
    </div>
  );
};
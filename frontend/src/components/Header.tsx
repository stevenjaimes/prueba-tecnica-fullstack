import { Link } from 'react-router-dom';
import { FaStackOverflow, FaPlane } from 'react-icons/fa';

export const Header = () => {
    return (
        <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg sticky top-0 z-50">
            <div className="container mx-auto px-4 py-3 sm:py-4">
                <div className="flex flex-col sm:flex-row justify-between items-center gap-2 sm:gap-0">

                    {/* Logo/Título - ajustado para móviles */}
                    <Link to="/" className="group w-full sm:w-auto">
                        <div className="flex flex-col sm:flex-row items-center sm:items-baseline">
                            <h1 className="text-xl sm:text-2xl md:text-3xl font-bold flex items-center">
                                <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-300 to-white group-hover:from-white group-hover:to-blue-300 transition-all duration-300">
                                    Reto FullStack
                                </span>
                            </h1>
                            <span className="ml-0 sm:ml-2 mt-1 sm:mt-0 px-2 py-1 bg-blue-500 rounded-md text-xs sm:text-sm md:text-base font-normal">
                                by Dev
                            </span>
                        </div>
                    </Link>

                    {/* Navegación - optimizada para móviles */}
                    <nav className="w-full sm:w-auto">
                        <ul className="flex justify-between sm:justify-normal space-x-1 sm:space-x-3 md:space-x-6 bg-blue-700/40 sm:bg-transparent rounded-lg p-1 sm:p-0">
                            <li className="flex-1 sm:flex-none text-center">
                                <Link
                                    to="/"
                                    className="flex flex-col sm:flex-row items-center px-2 sm:px-4 py-1 sm:py-2 rounded-md hover:bg-blue-500/50 transition-all group text-sm sm:text-base"
                                >
                                    <FaStackOverflow className="mb-1 sm:mb-0 sm:mr-2 text-blue-300 group-hover:text-white text-lg" />
                                    <span className="font-medium">StackExchange</span>
                                </Link>
                            </li>
                            <li className="flex-1 sm:flex-none text-center">
                                <Link
                                    to="/vuelos"
                                    className="flex flex-col sm:flex-row items-center px-2 sm:px-4 py-1 sm:py-2 rounded-md hover:bg-blue-500/50 transition-all group text-sm sm:text-base"
                                >
                                    <FaPlane className="mb-1 sm:mb-0 sm:mr-2 text-blue-300 group-hover:text-white text-lg" />
                                    <span className="font-medium">Vuelos</span>                                   
                                </Link>
                            </li>
                        </ul>
                    </nav>
                </div>
            </div>
        </header>
    );
};
import React from 'react';
import { FaGithub, FaLinkedin, FaCode } from 'react-icons/fa';
import { SiReact, SiTypescript, SiTailwindcss, SiFlask } from 'react-icons/si';

export const Footer: React.FC = () => {
    return (
        <footer className="bg-gray-800 text-gray-100 py-8 px-4 border-t border-gray-700">
            <div className="container mx-auto">
                <div className="flex flex-col items-center text-center">
                    <div className="mb-4 flex items-center space-x-2">
                        <FaCode className="text-2xl text-blue-400" />
                        <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                            Prueba Técnica
                        </span>
                    </div>

                    <p className="max-w-2xl mx-auto text-gray-300 mb-6">
                        Ejercicio de desarrollo FullStack implementando Flask, React, TypeScript y Tailwind CSS. Una demostración de 
                        integración entre frontend y backend con enfoque en buenas prácticas y funcionalidad.
                    </p>

                    <div className="flex space-x-6 mb-6">
                        <a href="https://github.com/stevenjaimes"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-gray-400 hover:text-blue-400 transition-colors"
                            aria-label="GitHub">
                            <FaGithub className="text-2xl" />
                        </a>
                        <a href="https://linkedin.com/in/henry-steven-jaimes"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-gray-400 hover:text-blue-400 transition-colors"
                            aria-label="LinkedIn">
                            <FaLinkedin className="text-2xl" />
                        </a>
                    </div>

                    <div className="flex flex-wrap justify-center gap-4 mb-6">
                        <span className="px-3 py-1 bg-gray-700 rounded-full text-sm flex items-center">
                            <SiFlask className="text-gray-200 mr-1" /> Flask
                        </span>
                        <span className="px-3 py-1 bg-gray-700 rounded-full text-sm flex items-center">
                            <SiReact className="text-blue-400 mr-1" /> React
                        </span>
                        <span className="px-3 py-1 bg-gray-700 rounded-full text-sm flex items-center">
                            <SiTypescript className="text-blue-600 mr-1" /> TypeScript
                        </span>
                        <span className="px-3 py-1 bg-gray-700 rounded-full text-sm flex items-center">
                            <SiTailwindcss className="text-cyan-400 mr-1" /> Tailwind
                        </span>
                    </div>

                    <div className="text-sm text-gray-500">
                        © {new Date().getFullYear()} Desarrollo de Prueba Técnica.
                    </div>
                </div>
            </div>
        </footer>
    );
};
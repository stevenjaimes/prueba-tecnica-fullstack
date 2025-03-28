export interface StatsData {
    total: number;
    contestadas: number;
    no_contestadas: number;
  }
  
  export interface PreguntaData {
    titulo: string;
    score: number;
    views: number;
    link: string;
    fecha: string;
  }
  
  export interface StackExchangeResponse {
    stats: StatsData;
    mayor_puntuacion: PreguntaData;
    menor_visitas: PreguntaData;
    mas_antigua: PreguntaData;
    mas_reciente: PreguntaData;
  }
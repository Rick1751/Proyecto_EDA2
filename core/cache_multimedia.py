"""
cache_multimedia.py

Módulo para cachear y precargar recursos multimedia (imágenes, sonidos)
de forma paralela para optimizar el rendimiento en Pygame.

Características:
    - Caché thread-safe para multimedia
    - Precarga de imágenes en paralelo
    - Gestión de memoria para recursos
    - Limpieza automática de recursos
"""

import os
import pygame
import logging
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

logger = logging.getLogger(__name__)


class CacheMultimedia:
    """Gestor centralizado de caché para recursos multimedia."""
    
    def __init__(self, max_workers=2):
        """
        Inicializa el caché.
        
        Args:
            max_workers: número máximo de threads para precarga
        """
        self.cache_imagenes = {}
        self.cache_sonidos = {}
        self.lock = Lock()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        logger.info("CacheMultimedia inicializado")
    
    def cargar_imagen(self, ruta_imagen):
        """
        Carga una imagen y la cachea.
        
        Args:
            ruta_imagen: ruta al archivo de imagen
        
        Returns:
            pygame.Surface con la imagen o None si hay error
        """
        if not os.path.exists(ruta_imagen):
            logger.warning(f"Imagen no encontrada: {ruta_imagen}")
            return None
        
        with self.lock:
            if ruta_imagen in self.cache_imagenes:
                return self.cache_imagenes[ruta_imagen]
        
        try:
            imagen = pygame.image.load(ruta_imagen).convert_alpha()
            with self.lock:
                self.cache_imagenes[ruta_imagen] = imagen
            return imagen
        except Exception as e:
            logger.error(f"Error cargando imagen {ruta_imagen}: {e}")
            return None
    
    def precargar_imagenes_paralelo(self, rutas_imagenes):
        """
        Precarga múltiples imágenes en paralelo.
        
        Args:
            rutas_imagenes: lista de rutas a imágenes
        
        Returns:
            lista de imágenes cargadas
        """
        futuros = [
            self.executor.submit(self.cargar_imagen, ruta)
            for ruta in rutas_imagenes
        ]
        return [futuro.result() for futuro in futuros]
    
    def cargar_sonido(self, ruta_sonido):
        """
        Carga un sonido y lo cachea.
        
        Args:
            ruta_sonido: ruta al archivo de audio
        
        Returns:
            pygame.mixer.Sound con el audio o None si hay error
        """
        if not os.path.exists(ruta_sonido):
            logger.warning(f"Sonido no encontrado: {ruta_sonido}")
            return None
        
        with self.lock:
            if ruta_sonido in self.cache_sonidos:
                return self.cache_sonidos[ruta_sonido]
        
        try:
            sonido = pygame.mixer.Sound(ruta_sonido)
            with self.lock:
                self.cache_sonidos[ruta_sonido] = sonido
            return sonido
        except Exception as e:
            logger.error(f"Error cargando sonido {ruta_sonido}: {e}")
            return None
    
    def limpiar_cache(self):
        """Limpia todos los recursos en caché."""
        with self.lock:
            self.cache_imagenes.clear()
            self.cache_sonidos.clear()
        logger.info("Caché multimedia limpiado")
    
    def obtener_stats(self):
        """Retorna estadísticas del caché."""
        with self.lock:
            return {
                "imagenes_cacheadas": len(self.cache_imagenes),
                "sonidos_cacheados": len(self.cache_sonidos),
            }
    
    def cerrar(self):
        """Cierra el executor y limpia recursos."""
        self.executor.shutdown(wait=True)
        self.limpiar_cache()
        logger.info("CacheMultimedia cerrado")
    
    def __del__(self):
        """Limpieza automática."""
        try:
            self.cerrar()
        except:
            pass


# Singleton global del caché
_cache_global = None


def obtener_cache_multimedia():
    """Obtiene la instancia global del caché multimedia."""
    global _cache_global
    if _cache_global is None:
        _cache_global = CacheMultimedia()
    return _cache_global


def limpiar_cache_multimedia():
    """Limpia el caché global."""
    global _cache_global
    if _cache_global is not None:
        _cache_global.cerrar()
        _cache_global = None

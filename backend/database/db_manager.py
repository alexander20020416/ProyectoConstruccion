"""
Gestor de Base de Datos - Sistema Braille
==========================================
Maneja el almacenamiento en SQLite para historial de conversiones
y registros de generación de PDFs.

Tablas:
- conversions: Historial de conversiones texto↔braille
- pdf_generations: Registro de PDFs generados

Autor: GR4
Fecha: Noviembre 2025
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional


class DatabaseManager:
    """Gestor de base de datos SQLite para el sistema Braille."""
    
    def __init__(self, db_path: str = None):
        """
        Inicializa el gestor de base de datos.
        
        Args:
            db_path: Ruta a la base de datos SQLite
        """
        if db_path is None:
            # Directorio raíz del proyecto
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            db_dir = os.path.join(project_root, 'backend', 'database')
            os.makedirs(db_dir, exist_ok=True)
            self.db_path = os.path.join(db_dir, 'braille_system.db')
        else:
            self.db_path = db_path
        
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Obtiene una conexión a la base de datos.
        
        Returns:
            Conexión SQLite
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Permite acceso por nombre de columna
        return conn
    
    def init_database(self):
        """Inicializa las tablas de la base de datos si no existen."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de conversiones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_text TEXT NOT NULL,
                braille_text TEXT NOT NULL,
                conversion_type TEXT NOT NULL,
                character_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de generación de PDFs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pdf_generations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                file_path TEXT NOT NULL,
                format_type TEXT,
                file_size INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de configuraciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Índices para mejorar rendimiento
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_conversions_type 
            ON conversions(conversion_type)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_conversions_date 
            ON conversions(created_at DESC)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_pdf_date 
            ON pdf_generations(created_at DESC)
        ''')
        
        conn.commit()
        conn.close()
    
    def save_conversion(self, original_text: str, braille_text: str, 
                       conversion_type: str) -> int:
        """
        Guarda un registro de conversión.
        
        Args:
            original_text: Texto original
            braille_text: Texto en Braille
            conversion_type: Tipo de conversión (text_to_braille, braille_to_text)
            
        Returns:
            ID del registro creado
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        character_count = len(original_text)
        
        cursor.execute('''
            INSERT INTO conversions (original_text, braille_text, conversion_type, character_count)
            VALUES (?, ?, ?, ?)
        ''', (original_text, braille_text, conversion_type, character_count))
        
        conversion_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return conversion_id
    
    def get_conversion_history(self, limit: int = 50, 
                              conversion_type: str = None) -> List[Dict]:
        """
        Obtiene el historial de conversiones.
        
        Args:
            limit: Número máximo de registros
            conversion_type: Filtrar por tipo (opcional)
            
        Returns:
            Lista de diccionarios con el historial
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if conversion_type:
            cursor.execute('''
                SELECT id, original_text, braille_text, conversion_type, 
                       character_count, created_at
                FROM conversions
                WHERE conversion_type = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (conversion_type, limit))
        else:
            cursor.execute('''
                SELECT id, original_text, braille_text, conversion_type,
                       character_count, created_at
                FROM conversions
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Convertir a lista de diccionarios
        history = []
        for row in rows:
            history.append({
                'id': row['id'],
                'original_text': row['original_text'],
                'braille_text': row['braille_text'],
                'conversion_type': row['conversion_type'],
                'character_count': row['character_count'],
                'timestamp': row['created_at']
            })
        
        return history
    
    def save_pdf_generation(self, title: str, file_path: str, 
                          format_type: str) -> int:
        """
        Guarda un registro de generación de PDF.
        
        Args:
            title: Título del PDF
            file_path: Ruta del archivo generado
            format_type: Tipo de formato (elevator, door, label)
            
        Returns:
            ID del registro creado
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Obtener tamaño del archivo
        file_size = 0
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
        
        cursor.execute('''
            INSERT INTO pdf_generations (title, file_path, format_type, file_size)
            VALUES (?, ?, ?, ?)
        ''', (title, file_path, format_type, file_size))
        
        pdf_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return pdf_id
    
    def get_pdf_history(self, limit: int = 50) -> List[Dict]:
        """
        Obtiene el historial de PDFs generados.
        
        Args:
            limit: Número máximo de registros
            
        Returns:
            Lista de diccionarios con el historial
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, file_path, format_type, file_size, created_at
            FROM pdf_generations
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                'id': row['id'],
                'title': row['title'],
                'file_path': row['file_path'],
                'format_type': row['format_type'],
                'file_size': row['file_size'],
                'timestamp': row['created_at']
            })
        
        return history
    
    def get_statistics(self) -> Dict:
        """
        Obtiene estadísticas del sistema.
        
        Returns:
            Diccionario con estadísticas
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total de conversiones
        cursor.execute('SELECT COUNT(*) as count FROM conversions')
        total_conversions = cursor.fetchone()['count']
        
        # Conversiones por tipo
        cursor.execute('''
            SELECT conversion_type, COUNT(*) as count
            FROM conversions
            GROUP BY conversion_type
        ''')
        conversions_by_type = {}
        for row in cursor.fetchall():
            conversions_by_type[row['conversion_type']] = row['count']
        
        # Total de PDFs generados
        cursor.execute('SELECT COUNT(*) as count FROM pdf_generations')
        total_pdfs = cursor.fetchone()['count']
        
        # PDFs por formato
        cursor.execute('''
            SELECT format_type, COUNT(*) as count
            FROM pdf_generations
            GROUP BY format_type
        ''')
        pdfs_by_format = {}
        for row in cursor.fetchall():
            pdfs_by_format[row['format_type']] = row['count']
        
        # Total de caracteres convertidos
        cursor.execute('SELECT SUM(character_count) as total FROM conversions')
        total_characters = cursor.fetchone()['total'] or 0
        
        conn.close()
        
        return {
            'total_conversions': total_conversions,
            'conversions_by_type': conversions_by_type,
            'total_pdfs': total_pdfs,
            'pdfs_by_format': pdfs_by_format,
            'total_characters_converted': total_characters
        }
    
    def delete_old_records(self, days: int = 30):
        """
        Elimina registros antiguos (limpieza de base de datos).
        
        Args:
            days: Número de días de antigüedad para eliminar
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM conversions
            WHERE created_at < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        conversions_deleted = cursor.rowcount
        
        cursor.execute('''
            DELETE FROM pdf_generations
            WHERE created_at < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        pdfs_deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return {
            'conversions_deleted': conversions_deleted,
            'pdfs_deleted': pdfs_deleted
        }
    
    def close(self):
        """Cierra la conexión a la base de datos."""
        # SQLite no mantiene conexiones permanentes, no hay nada que cerrar
        pass


# Instancia global
db_manager = DatabaseManager()


if __name__ == "__main__":
    # Pruebas de la base de datos
    print("=" * 60)
    print("PRUEBAS DE BASE DE DATOS")
    print("=" * 60)
    
    db = DatabaseManager()
    
    # Prueba 1: Guardar conversión
    print("\n1. Guardando conversión...")
    conv_id = db.save_conversion(
        original_text="Hola mundo",
        braille_text="⠓⠕⠇⠁ ⠍⠥⠝⠙⠕",
        conversion_type="text_to_braille"
    )
    print(f"✓ Conversión guardada con ID: {conv_id}")
    
    # Prueba 2: Obtener historial
    print("\n2. Obteniendo historial...")
    history = db.get_conversion_history(limit=5)
    print(f"✓ Registros encontrados: {len(history)}")
    for record in history:
        print(f"  - {record['original_text']} → {record['braille_text']}")
    
    # Prueba 3: Estadísticas
    print("\n3. Estadísticas del sistema:")
    stats = db.get_statistics()
    print(f"✓ Total conversiones: {stats['total_conversions']}")
    print(f"✓ Total PDFs: {stats['total_pdfs']}")
    print(f"✓ Caracteres convertidos: {stats['total_characters_converted']}")
    
    print("\n" + "=" * 60)

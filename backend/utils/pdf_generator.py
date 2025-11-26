"""
Generador de PDFs - Señalética Braille
=======================================
Genera documentos PDF con señalética en Braille usando ReportLab.

Formatos soportados:
- Señalética de ascensores (números de pisos)
- Etiquetas de puertas
- Señalización general

Autor: GR4
Fecha: Noviembre 2025
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import cm, inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os
from backend.models.braille_converter import braille_converter


class BrailleSignagePDFGenerator:
    """Generador de PDFs para señalética Braille."""
    
    def __init__(self, output_dir: str = None):
        """
        Inicializa el generador de PDFs.
        
        Args:
            output_dir: Directorio donde guardar los PDFs
        """
        if output_dir is None:
            # Directorio raíz del proyecto
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            self.output_dir = os.path.join(project_root, 'output')
        else:
            self.output_dir = output_dir
        
        # Crear directorio si no existe
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _draw_braille_character(self, c: canvas.Canvas, x: float, y: float, 
                               dots: tuple, dot_size: float = 3, 
                               spacing: float = 6):
        """
        Dibuja un carácter Braille como círculos en el PDF.
        
        Sistema de posiciones:
        1 • • 4
        2 • • 5
        3 • • 6
        
        Args:
            c: Canvas de ReportLab
            x, y: Posición base (esquina superior izquierda)
            dots: Tupla de puntos activos (1-6)
            dot_size: Radio del punto en puntos
            spacing: Espaciado entre puntos
        """
        # Posiciones de los 6 puntos en el cuadratín
        positions = {
            1: (0, 0),
            2: (0, spacing),
            3: (0, 2 * spacing),
            4: (spacing, 0),
            5: (spacing, spacing),
            6: (spacing, 2 * spacing)
        }
        
        # Dibujar puntos activos (llenos)
        c.setFillColor(colors.black)
        for dot in dots:
            if dot in positions:
                dx, dy = positions[dot]
                c.circle(x + dx, y - dy, dot_size, fill=1)
        
        # Dibujar puntos inactivos (contorno) - opcional
        c.setStrokeColor(colors.lightgrey)
        c.setLineWidth(0.5)
        for dot_num, (dx, dy) in positions.items():
            if dot_num not in dots:
                c.circle(x + dx, y - dy, dot_size, fill=0)
    
    def _draw_braille_text(self, c: canvas.Canvas, x: float, y: float, 
                          text: str, char_spacing: float = 15):
        """
        Dibuja una cadena de texto completa en Braille.
        
        Args:
            c: Canvas de ReportLab
            x, y: Posición inicial
            text: Texto a dibujar
            char_spacing: Espaciado entre caracteres
        """
        current_x = x
        
        # Convertir texto a braille usando el convertidor completo
        # Esto maneja números, mayúsculas, indicadores, etc.
        braille_dots_list = braille_converter.text_to_braille_dots(text)
        
        for dots_tuple in braille_dots_list:
            if dots_tuple == tuple():
                # Espacio en blanco - solo avanzar sin dibujar celda
                current_x += char_spacing
            else:
                # Dibujar carácter con sus puntos
                self._draw_braille_character(c, current_x, y, dots_tuple)
                current_x += char_spacing
    
    def generate_elevator_signage(self, title: str, items: list, 
                                 filename: str = None) -> str:
        """
        Genera señalética para ascensores con números de piso.
        
        Args:
            title: Título del documento
            items: Lista de diccionarios con 'text' y 'number'
            filename: Nombre del archivo (opcional)
            
        Returns:
            Ruta del PDF generado
            
        Ejemplo:
            items = [
                {'text': 'Planta Baja', 'number': '0'},
                {'text': 'Piso 1', 'number': '1'}
            ]
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ascensor_{timestamp}.pdf"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Crear canvas
        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4
        
        # Título
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width / 2, height - 2*cm, title)
        
        # Subtítulo
        c.setFont("Helvetica", 12)
        c.drawCentredString(width / 2, height - 3*cm, 
                           "SISTEMA DE LECTO-ESCRITURA BRAILLE ESPAÑOL")
        
        # Línea separadora
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.line(3*cm, height - 3.5*cm, width - 3*cm, height - 3.5*cm)
        
        # Posición inicial para items
        y_position = height - 5*cm
        
        for item in items:
            text = item.get('text', '')
            number = item.get('number', '')
            
            # Marco para cada señal
            box_height = 4*cm
            box_width = width - 6*cm
            
            c.setStrokeColor(colors.grey)
            c.setLineWidth(1)
            c.rect(3*cm, y_position - box_height, box_width, box_height)
            
            # Texto en español
            c.setFont("Helvetica-Bold", 16)
            c.drawString(3.5*cm, y_position - 1*cm, f"Texto en línea:")
            
            c.setFont("Helvetica", 14)
            c.drawString(3.5*cm, y_position - 1.8*cm, f"{text} {number}")
            
            # Texto en Braille
            c.setFont("Helvetica-Bold", 16)
            c.drawString(3.5*cm, y_position - 2.6*cm, f"Texto en braille:")
            
            # Dibujar Braille (más grande para señalética)
            braille_y = y_position - 3.3*cm
            braille_x = 3.5*cm
            
            # Convertir texto a Braille
            full_text = f"{text} {number}"
            self._draw_braille_text(c, braille_x, braille_y, full_text, char_spacing=20)
            
            # Mover posición para siguiente item
            y_position -= (box_height + 1*cm)
            
            # Nueva página si es necesario
            if y_position < 5*cm:
                c.showPage()
                y_position = height - 3*cm
        
        # Pie de página
        c.setFont("Helvetica-Oblique", 8)
        c.drawCentredString(width / 2, 2*cm, 
                           f"Generado por Sistema Braille - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        # Guardar PDF
        c.save()
        return filepath
    
    def generate_door_label(self, room_name: str, room_number: str = None,
                          filename: str = None) -> str:
        """
        Genera etiqueta para puertas.
        
        Args:
            room_name: Nombre de la sala/oficina
            room_number: Número de sala (opcional)
            filename: Nombre del archivo (opcional)
            
        Returns:
            Ruta del PDF generado
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"puerta_{timestamp}.pdf"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Crear canvas (tamaño más pequeño para etiquetas)
        c = canvas.Canvas(filepath, pagesize=(15*cm, 10*cm))
        width = 15*cm
        height = 10*cm
        
        # Borde
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.rect(0.5*cm, 0.5*cm, width - 1*cm, height - 1*cm)
        
        # Texto español
        c.setFont("Helvetica-Bold", 18)
        y_pos = height - 2*cm
        
        if room_number:
            c.drawCentredString(width / 2, y_pos, f"{room_name} {room_number}")
        else:
            c.drawCentredString(width / 2, y_pos, room_name)
        
        # Línea separadora
        c.line(2*cm, y_pos - 0.7*cm, width - 2*cm, y_pos - 0.7*cm)
        
        # Braille (centrado)
        braille_text = f"{room_name} {room_number}" if room_number else room_name
        braille_y = height / 2 - 0.5*cm
        
        # Calcular ancho para centrar
        char_count = len(braille_text)
        total_width = char_count * 20
        braille_x = (width - total_width) / 2
        
        self._draw_braille_text(c, braille_x, braille_y, braille_text, char_spacing=20)
        
        # Guardar
        c.save()
        return filepath
    
    def generate_custom_label(self, text: str, subtitle: str = None,
                            filename: str = None) -> str:
        """
        Genera etiqueta personalizada.
        
        Args:
            text: Texto principal
            subtitle: Subtítulo (opcional)
            filename: Nombre del archivo (opcional)
            
        Returns:
            Ruta del PDF generado
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"etiqueta_{timestamp}.pdf"
        
        filepath = os.path.join(self.output_dir, filename)
        
        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4
        
        # Título
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width / 2, height - 4*cm, text)
        
        if subtitle:
            c.setFont("Helvetica", 14)
            c.drawCentredString(width / 2, height - 5*cm, subtitle)
        
        # Braille del texto principal (centrado)
        braille_y = height / 2 + 1*cm if subtitle else height / 2
        
        # Calcular centrado para texto principal
        char_count = len(text)
        total_width = char_count * 25
        braille_x = (width - total_width) / 2
        
        self._draw_braille_text(c, braille_x, braille_y, text, char_spacing=25)
        
        # Braille del subtítulo (si existe)
        if subtitle:
            braille_y_subtitle = height / 2 - 2*cm
            
            # Calcular centrado para subtítulo
            char_count_subtitle = len(subtitle)
            total_width_subtitle = char_count_subtitle * 20
            braille_x_subtitle = (width - total_width_subtitle) / 2
            
            self._draw_braille_text(c, braille_x_subtitle, braille_y_subtitle, subtitle, char_spacing=20)
        
        # Pie de página
        c.setFont("Helvetica-Oblique", 10)
        c.drawCentredString(width / 2, 2*cm, 
                           f"Sistema Braille - {datetime.now().strftime('%d/%m/%Y')}")
        
        c.save()
        return filepath


# Instancia global
pdf_generator = BrailleSignagePDFGenerator()


def generate_signage_pdf(title: str, items: list, format_type: str = 'elevator') -> str:
    """
    Función helper para generar PDFs de señalética.
    
    Args:
        title: Título del documento
        items: Lista de elementos a incluir
        format_type: Tipo de formato (elevator, door, label)
        
    Returns:
        Ruta del PDF generado
    """
    generator = BrailleSignagePDFGenerator()
    
    if format_type == 'elevator':
        return generator.generate_elevator_signage(title, items)
    elif format_type == 'door':
        # items[0] contiene room_name y room_number
        item = items[0]
        return generator.generate_door_label(
            item.get('text', ''),
            item.get('number', None)
        )
    elif format_type == 'label':
        # items[0] contiene text y subtitle
        item = items[0]
        return generator.generate_custom_label(
            item.get('text', ''),
            item.get('subtitle', None)
        )
    else:
        raise ValueError(f"Formato no soportado: {format_type}")


if __name__ == "__main__":
    # Pruebas
    print("Generando PDFs de prueba...")
    
    # Prueba 1: Ascensor
    items_elevator = [
        {'text': 'Planta Baja', 'number': '0'},
        {'text': 'Piso 1', 'number': '1'},
        {'text': 'Piso 2', 'number': '2'},
        {'text': 'Piso 3', 'number': '3'},
    ]
    
    pdf1 = generate_signage_pdf("ASCENSOR", items_elevator, 'elevator')
    print(f"✓ PDF de ascensor generado: {pdf1}")
    
    # Prueba 2: Puerta
    pdf2 = generate_signage_pdf("Oficina", [{'text': 'Oficina', 'number': '205'}], 'door')
    print(f"✓ PDF de puerta generado: {pdf2}")
    
    # Prueba 3: Etiqueta
    pdf3 = generate_signage_pdf("Salida", [{'text': 'Salida', 'subtitle': 'Emergencia'}], 'label')
    print(f"✓ PDF de etiqueta generado: {pdf3}")
    
    print("\n¡Generación de PDFs completada!")

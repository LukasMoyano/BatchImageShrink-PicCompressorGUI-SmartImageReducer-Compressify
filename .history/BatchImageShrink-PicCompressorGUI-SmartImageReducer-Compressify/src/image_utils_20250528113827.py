"""
Módulo image_utils.py

Funciones auxiliares para procesamiento de imágenes:
- Compresión y guardado en diferentes formatos y calidades.
- Corrección automática de orientación usando EXIF.
- Escalado de imágenes.
- (Opcional) Integración con módulos de restauración IA.
"""

from PIL import Image, ExifTags
import os

def corregir_orientacion(img):
    """
    Corrige la orientación de una imagen usando los metadatos EXIF.
    Devuelve la imagen correctamente orientada.
    """
    try:
        exif = img._getexif()
        if exif is not None:
            orientation_tag = None
            for tag, value in ExifTags.TAGS.items():
                if value == 'Orientation':
                    orientation_tag = tag
                    break
            if orientation_tag is not None:
                orientation = exif.get(orientation_tag, 1)
                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(270, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)
    except Exception:
        pass
    return img

def comprimir_imagen(
    ruta_origen, 
    ruta_destino, 
    formato="JPEG", 
    calidad=85, 
    optimizar=True, 
    progresivo=True
):
    """
    Comprime y guarda una imagen en el formato y calidad especificados.
    Corrige la orientación automáticamente.
    """
    try:
        img = Image.open(ruta_origen)
        img = corregir_orientacion(img)
        # Convertir a RGB si es necesario para JPEG
        if formato.upper() == "JPEG":
            if img.mode in ("RGBA", "LA"):
                fondo = Image.new("RGB", img.size, (255, 255, 255))
                fondo.paste(img, mask=img.split()[-1])
                img = fondo
            else:
                img = img.convert("RGB")
            img.save(ruta_destino, formato, quality=calidad, optimize=optimizar, progressive=progresivo)
        else:
            img.save(ruta_destino, formato, optimize=optimizar)
        return True, None
    except Exception as e:
        return False, str(e)

def escalar_imagen(ruta_origen, ruta_destino, escala=2, formato="JPEG", calidad=85):
    """
    Escala una imagen por un factor dado y la guarda.
    """
    try:
        img = Image.open(ruta_origen)
        img = corregir_orientacion(img)
        nueva_size = (int(img.width * escala), int(img.height * escala))
        img = img.resize(nueva_size, Image.LANCZOS)
        if formato.upper() == "JPEG":
            img = img.convert("RGB")
            img.save(ruta_destino, formato, quality=calidad, optimize=True, progressive=True)
        else:
            img.save(ruta_destino, formato, optimize=True)
        return True, None
    except Exception as e:
        return False, str(e)

# (Opcional) Integración con IA
def restaurar_imagen_ia(ruta_origen, ruta_destino, modelo="realesrgan", escala=2):
    """
    Llama a un módulo externo de IA para restauración/escalado.
    Este es un stub: la implementación real debe estar en ia_restoration.py.
    """
    try:
        from ia_restoration import restaurar_con_ia
        return restaurar_con_ia(ruta_origen, ruta_destino, modelo=modelo, escala=escala)
    except ImportError:
        return False, "Módulo de restauración IA no disponible"
    except Exception as e:
        return False, str(e)

def obtener_imagenes_en_carpeta(carpeta, extensiones=None):
    """
    Devuelve una lista de archivos de imagen válidos en una carpeta.
    """
    if extensiones is None:
        extensiones = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".avif")
    return [
        f for f in os.listdir(carpeta)
        if f.lower().endswith(extensiones) and os.path.isfile(os.path.join(carpeta, f))
    ]

# Exportaciones para otros módulos
__all__ = [
    "corregir_orientacion",
    "comprimir_imagen",
    "escalar_imagen",
    "restaurar_imagen_ia",
    "obtener_imagenes_en_carpeta"
]
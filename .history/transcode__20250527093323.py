from PIL import Image, ExifTags
import os

# Ruta de la carpeta original
input_folder = input("Introduce la ruta de la carpeta de imágenes de origen: ").strip()

# Carpeta destino elegida por el usuario
output_folder = input("Introduce la ruta de la carpeta de destino para las imágenes comprimidas: ").strip()

# Niveles de compresión predefinidos
calidad_config = {
    "1": {"nombre": "Alta calidad", "valor": 85},
    "2": {"nombre": "Calidad media", "valor": 60},
    "3": {"nombre": "Baja calidad", "valor": 30}
}

# Mostrar menú y obtener opción del usuario
print("Selecciona el nivel de compresión:")
for k, v in calidad_config.items():
    print(f"{k}) {v['nombre']} (calidad {v['valor']}%)")
opcion = input("Opción (1/2/3): ")

# Validar opción
if opcion not in calidad_config:
    print("❌ Opción inválida. Seleccionando calidad media por defecto.")
    calidad = 60
else:
    calidad = calidad_config[opcion]["valor"]

print(f"✅ Usando compresión: {calidad_config.get(opcion, {'nombre':'Calidad media'})['nombre']}")

# Validar que existe la carpeta de origen
if not os.path.isdir(input_folder):
    print(f"❌ La carpeta de origen '{input_folder}' no existe.")
    exit(1)

# Crear carpeta destino si no existe
os.makedirs(output_folder, exist_ok=True)

# Buscar imágenes JPG
imagenes = [f for f in os.listdir(input_folder) if f.lower().endswith(".jpg")]

if not imagenes:
    print(f"⚠️ No se encontraron imágenes .jpg en la carpeta: {input_folder}")
    exit(0)

print(f"📦 Encontradas {len(imagenes)} imágenes. Comprimiendo...")

# Función para corregir orientación usando EXIF
def corregir_orientacion(img):
    try:
        exif = img._getexif()
        if exif is not None:
            for tag, value in ExifTags.TAGS.items():
                if value == 'Orientation':
                    orientation_tag = tag
                    break
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

# Procesar cada imagen
for img_file in imagenes:
    ruta_origen = os.path.join(input_folder, img_file)
    ruta_destino = os.path.join(output_folder, img_file)
    
    try:
        print(f"🖼️ Procesando: {img_file}")
        img = Image.open(ruta_origen)
        img = corregir_orientacion(img)
        img = img.convert("RGB")  # Asegura compatibilidad JPEG
        
        # Guardar con calidad seleccionada
        img.save(ruta_destino, "JPEG", quality=calidad, optimize=True, progressive=True)
        
        # Verificar tamaño (máximo 5MB)
        tamaño = os.path.getsize(ruta_destino) / (1024 * 1024)  # en MB
        if tamaño > 5:
            print(f"⚠️ {img_file} pesa {tamaño:.2f}MB (más de 5MB). Considera usar calidad más baja.")
        else:
            print(f"✅ {img_file} comprimido correctamente. Tamaño: {tamaño:.2f}MB")
    
    except Exception as e:
        print(f"❌ Error procesando {img_file}: {str(e)}")

print(f"\n🎉 Compresión terminada. Archivos guardados en: {output_folder}")
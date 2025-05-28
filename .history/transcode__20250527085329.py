from PIL import Image
import os

# Ruta de la carpeta original
input_folder = "/home/userx/Pictures/ProfilesPics/FotoFusa_lks"

# Carpeta destino (paralela)
output_folder = f"{input_folder}_comprimidas"

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

print(f"✅ Usando compresión: {calidad_config[opcion]['nombre']}")

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

# Procesar cada imagen
for img_file in imagenes:
    ruta_origen = os.path.join(input_folder, img_file)
    ruta_destino = os.path.join(output_folder, img_file)
    
    try:
        print(f"🖼️ Procesando: {img_file}")
        img = Image.open(ruta_origen)
        
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
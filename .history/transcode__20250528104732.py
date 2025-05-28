from PIL import Image, ExifTags
import pillow_avif  # Importa el plugin AVIF
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

# Oculta la ventana principal de Tkinter
root = tk.Tk()
root.withdraw()

# Preguntar si se quiere procesar una carpeta o una sola imagen
print("¿Qué deseas procesar?")
print("1) Carpeta completa de imágenes")
print("2) Solo una imagen")
modo = input("Opción (1/2): ")

if modo == "1":
    print("Selecciona la carpeta de imágenes de origen...")
    input_folder = filedialog.askdirectory(title="Selecciona la carpeta de imágenes de origen")
    if not input_folder:
        print("❌ No se seleccionó carpeta de origen.")
        exit(1)
    extensiones_validas = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".avif")
    imagenes = [f for f in os.listdir(input_folder) if f.lower().endswith(extensiones_validas)]
    if not imagenes:
        print(f"⚠️ No se encontraron imágenes válidas en la carpeta: {input_folder}")
        exit(0)
elif modo == "2":
    print("Selecciona la imagen a comprimir...")
    input_file = filedialog.askopenfilename(
        title="Selecciona la imagen",
        filetypes=[("Imágenes", "*.jpg;*.jpeg;*.png;*.webp;*.bmp;*.tiff;*.avif"), ("Todos los archivos", "*.*")]
    )
    if not input_file:
        print("❌ No se seleccionó imagen.")
        exit(1)
    input_folder = os.path.dirname(input_file)
    imagenes = [os.path.basename(input_file)]
else:
    print("Opción inválida.")
    exit(1)

# Selección de carpeta de destino (puede crear nueva)
print("Selecciona la carpeta de destino para las imágenes comprimidas (puedes crear una nueva desde el diálogo)...")
output_folder = filedialog.askdirectory(title="Selecciona la carpeta de destino")
if not output_folder:
    # Ofrecer crear una nueva carpeta desde el script
    crear_nueva = input("¿Deseas crear una nueva carpeta de destino? (s/n): ").strip().lower()
    if crear_nueva == "s":
        nueva_carpeta = input("Introduce el nombre de la nueva carpeta de destino: ").strip()
        if nueva_carpeta:
            output_folder = os.path.join(os.path.expanduser("~"), nueva_carpeta)
            os.makedirs(output_folder, exist_ok=True)
            print(f"✅ Carpeta de destino creada: {output_folder}")
        else:
            print("❌ No se proporcionó nombre de carpeta.")
            exit(1)
    else:
        print("❌ No se seleccionó carpeta de destino.")
        exit(1)
else:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"✅ Carpeta de destino creada: {output_folder}")

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

# Preguntar formato de salida
print("Selecciona el formato de salida:")
print("1) JPEG (.jpg)")
print("2) PNG (.png, conserva transparencia)")
formato_opcion = input("Opción (1/2): ").strip()
if formato_opcion == "2":
    formato_salida = "PNG"
    extension_salida = ".png"
else:
    formato_salida = "JPEG"
    extension_salida = ".jpg"

# Validar que existe la carpeta de origen
if not os.path.isdir(input_folder):
    print(f"❌ La carpeta de origen '{input_folder}' no existe.")
    exit(1)

# Crear carpeta destino si no existe
os.makedirs(output_folder, exist_ok=True)

if not imagenes:
    print(f"⚠️ No se encontraron imágenes válidas en la carpeta: {input_folder}")
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
procesadas = 0
exitosas = 0
fallidas = 0
tamanos_antes = []
tamanos_despues = []

for img_file in imagenes:
    ruta_origen = os.path.join(input_folder, img_file)
    nombre_salida = os.path.splitext(img_file)[0] + extension_salida
    ruta_destino = os.path.join(output_folder, nombre_salida)
    procesadas += 1
    try:
        print(f"🖼️ Procesando: {img_file}")
        img = Image.open(ruta_origen)
        tamanos_antes.append(os.path.getsize(ruta_origen))
        img = corregir_orientacion(img)
        if formato_salida == "JPEG":
            if img.mode in ("RGBA", "LA"):
                fondo = Image.new("RGB", img.size, (255, 255, 255))
                fondo.paste(img, mask=img.split()[-1])
                img = fondo
            else:
                img = img.convert("RGB")
            img.save(ruta_destino, formato_salida, quality=calidad, optimize=True, progressive=True)
        else:  # PNG
            img.save(ruta_destino, formato_salida, optimize=True)
        tamanos_despues.append(os.path.getsize(ruta_destino))
        exitosas += 1
        tamaño = os.path.getsize(ruta_destino) / (1024 * 1024)
        if tamaño > 5:
            print(f"⚠️ {nombre_salida} pesa {tamaño:.2f}MB (más de 5MB). Considera usar calidad más baja.")
        else:
            print(f"✅ {nombre_salida} comprimido correctamente. Tamaño: {tamaño:.2f}MB")
    except Exception as e:
        print(f"❌ Error procesando {img_file}: {str(e)}")
        fallidas += 1

print(f"\n🎉 Compresión terminada. Archivos guardados en: {output_folder}")

# Resumen estadístico
print("\n===== RESUMEN DE EJECUCIÓN =====")
print(f"Total de imágenes encontradas: {len(imagenes)}")
print(f"Imágenes procesadas: {procesadas}")
print(f"Imágenes comprimidas exitosamente: {exitosas}")
print(f"Imágenes con error: {fallidas}")
print(f"Calidad de compresión utilizada: {calidad}%")
print(f"Formato de salida: {formato_salida}")

if tamanos_antes and tamanos_despues:
    avg_antes = sum(tamanos_antes) / len(tamanos_antes)
    avg_despues = sum(tamanos_despues) / len(tamanos_despues)
    print(f"Tamaño promedio antes: {avg_antes/1024:.2f} KB")
    print(f"Tamaño promedio después: {avg_despues/1024:.2f} KB")
    print(f"Reducción promedio: {100 - (avg_despues/avg_antes)*100:.2f}%")
else:
    print("No se pudo calcular la reducción de tamaño.")






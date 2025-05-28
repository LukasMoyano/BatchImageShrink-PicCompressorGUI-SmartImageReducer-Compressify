# ...código existente...

procesadas = 0
exitosas = 0
fallidas = 0
tamanos_antes = []
tamanos_despues = []

for img_file in imagenes:
    ruta_origen = os.path.join(input_folder, img_file)
    ruta_destino = os.path.join(output_folder, img_file)
    procesadas += 1
    try:
        with Image.open(ruta_origen) as img:
            tamanos_antes.append(os.path.getsize(ruta_origen))
            img = corregir_orientacion(img)
            img.save(ruta_destino, "JPEG", quality=calidad)
            tamanos_despues.append(os.path.getsize(ruta_destino))
            exitosas += 1
    except Exception as e:
        print(f"❌ Error procesando {img_file}: {e}")
        fallidas += 1

# Resumen estadístico
print("\n===== RESUMEN DE EJECUCIÓN =====")
print(f"Total de imágenes encontradas: {len(imagenes)}")
print(f"Imágenes procesadas: {procesadas}")
print(f"Imágenes comprimidas exitosamente: {exitosas}")
print(f"Imágenes con error: {fallidas}")
print(f"Calidad de compresión utilizada: {calidad}%")
if tamanos_antes and tamanos_despues:
    avg_antes = sum(tamanos_antes) / len(tamanos_antes)
    avg_despues = sum(tamanos_despues) / len(tamanos_despues)
    print(f"Tamaño promedio antes: {avg_antes/1024:.2f} KB")
    print(f"Tamaño promedio después: {avg_despues/1024:.2f} KB")
    print(f"Reducción promedio: {100 - (avg_despues/avg_antes)*100:.2f}%")
else:
    print("No se pudo calcular la reducción de tamaño.")
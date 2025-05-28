from PIL import Image
import os

input_folder = "/home/userx/Pictures/ProfilesPics/FotoFusa_lks"
output_folder = f"{input_folder}_comprimidas"
quality = 85  # Ajusta de 1 (peor) a 100 (mejor)

os.makedirs(output_folder, exist_ok=True)

for img_file in os.listdir(input_folder):
    if img_file.lower().endswith(".jpg"):
        img = Image.open(os.path.join(input_folder, img_file))
        img.save(os.path.join(output_folder, img_file), "JPEG", quality=quality)pip3 install Pillow
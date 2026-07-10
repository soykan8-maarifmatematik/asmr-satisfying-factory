import argparse
import sys

# Argümanları al
parser = argparse.ArgumentParser()
parser.add_argument("--file")
parser.add_argument("--title")
args = parser.parse_args()

file_path = args.file
video_title = args.title

print(f"--- Yükleme Başladı ---")
print(f"Dosya Yolu: {file_path}")
print(f"Video Başlığı: {video_title}")

# YouTube API Yükleme Kodlarınızı Buraya Ekleyin
# Örnek: upload_service.upload(file=file_path, title=video_title)

print("Yükleme başarıyla tamamlandı.")

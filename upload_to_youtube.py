import argparse
import os
import sys
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import pickle

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

# 1. Kimlik Bilgilerini Yükle
if not os.path.exists("token.pickle"):
    print("HATA: token.pickle dosyası bulunamadı!")
    sys.exit(1)

with open("token.pickle", "rb") as token:
    credentials = pickle.load(token)

# 2. YouTube Servisini Başlat
youtube = build("youtube", "v3", credentials=credentials)

# 3. Yükleme İşlemi
try:
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": video_title,
                "description": "Otomasyon ile yüklenmiştir.",
                "categoryId": "28"  # Matematik/Eğitim için kategori ID
            },
            "status": {"privacyStatus": "public"}
        },
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )

    print("YouTube'a gönderiliyor...")
    response = request.execute()
    print(f"Yükleme başarıyla tamamlandı! Video ID: {response.get('id')}")

except Exception as e:
    print(f"Yükleme sırasında hata oluştu: {str(e)}")
    sys.exit(1)

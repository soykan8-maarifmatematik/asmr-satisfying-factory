import argparse
import os
import sys
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

parser = argparse.ArgumentParser()
parser.add_argument("--file")
parser.add_argument("--title")
args = parser.parse_args()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, "token.pickle")

print(f"--- Yükleme Başlatılıyor ---")
print(f"Dosya: {args.file}")

if not os.path.exists(TOKEN_PATH):
    print(f"HATA: {TOKEN_PATH} bulunamadı!")
    sys.exit(1)

try:
    with open(TOKEN_PATH, "rb") as token:
        credentials = pickle.load(token)
    
    youtube = build("youtube", "v3", credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {"title": args.title, "description": "Maarif Matematik Otomasyon", "categoryId": "27"},
            "status": {"privacyStatus": "public"}
        },
        media_body=MediaFileUpload(args.file, chunksize=-1, resumable=True)
    )
    response = request.execute()
    print(f"BAŞARILI! Video ID: {response.get('id')}")

except Exception as e:
    print(f"HATA DETAYI: {str(e)}")
    sys.exit(1)

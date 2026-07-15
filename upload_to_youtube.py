import argparse
import pickle
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

parser = argparse.ArgumentParser()
parser.add_argument("--file")
parser.add_argument("--category")
args = parser.parse_args()

# İçerik dizini ve dosyalar
path = f"content/shorts/{args.category}"
with open(f"{path}/title.txt", "r", encoding="utf-8") as f: title = f.read().strip()
with open(f"{path}/description.txt", "r", encoding="utf-8") as f: desc = f.read().strip()
with open(f"{path}/tags.txt", "r", encoding="utf-8") as f: tags = f.read().strip().split(",")

with open("token.pickle", "rb") as token:
    creds = pickle.load(token)

youtube = build("youtube", "v3", credentials=creds)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": title,
            "description": desc,
            "tags": tags,
            "categoryId": "27",
            "defaultLanguage": "tr"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    },
    media_body=MediaFileUpload(args.file, chunksize=-1, resumable=True)
)
response = request.execute()
print(f"Video ID: {response.get('id')}")

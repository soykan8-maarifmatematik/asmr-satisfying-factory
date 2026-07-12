import argparse
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

parser = argparse.ArgumentParser()
parser.add_argument("--file")
parser.add_argument("--title")
args = parser.parse_args()

with open("token.pickle", "rb") as token:
    creds = pickle.load(token)

youtube = build("youtube", "v3", credentials=creds)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {"title": args.title, "description": "Maarif Matematik ASMR", "categoryId": "27"},
        "status": {"privacyStatus": "public"}
    },
    media_body=MediaFileUpload(args.file, chunksize=-1, resumable=True)
)
response = request.execute()
print(f"Video ID: {response.get('id')}")

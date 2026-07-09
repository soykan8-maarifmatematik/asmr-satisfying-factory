import os
import base64
import json
import pickle
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# GitHub Secret'lardan bilgileri çek
client_secrets_data = os.environ.get("CLIENT_SECRETS_JSON")
token_b64 = os.environ.get("TOKEN_PICKLE_BASE64")

# Dosyaları geçici olarak oluştur
with open("client_secrets.json", "w") as f:
    f.write(client_secrets_data)

with open("token.pickle", "wb") as f:
    f.write(base64.b64decode(token_b64))

# YouTube servisini başlat
# (Daha önce konuştuğumuz yükleme fonksiyonunu buraya entegre edeceğiz)

import argparse
import sys

# Argümanları al
parser = argparse.ArgumentParser()
parser.add_argument("--file")
parser.add_argument("--title")
args = parser.parse_args()

file_path = args.file
video_title = args.title

print(f"Dosya: {file_path}, Başlık: {video_title}")
# ... BURAYA YouTube API yükleme kodlarınızı koyun ...

import os
import json
import subprocess

def process_video_folder(folder_path):
    # Metadata dosyasını oku
    with open(f"{folder_path}/metadata.json", 'r') as f:
        metadata = json.load(f)
    
    video_path = f"{folder_path}/{metadata['filename']}"
    output_path = f"{folder_path}/final_output.mp4"
    
    # 1. Döngü (Loop) veya Short Kararı
    if metadata['type'] == "loop":
        print("Loop video tespit edildi, 1 saate tamamlanıyor...")
        # 1 saat = 3600 saniye. 3600 / 9 saniye = 400 döngü
        os.system(f"ffmpeg -stream_loop 400 -i {video_path} -t 3600 -c copy {output_path}")
    else:
        print("Short video tespit edildi, işlem yapılmıyor...")
        os.system(f"cp {video_path} {output_path}")

    # 2. YouTube'a Yükleme (YouTube API ve client_secrets gereklidir)
    print("YouTube'a yükleme başlıyor...")
    os.system(f"python3 upload_to_youtube.py --file {output_path} --title \"{metadata['title']}\" --desc \"{metadata['description']}\"")

# Örnek kullanım: Sadece değişen klasörü parametre olarak gönderin
# folder_path = "content/shorts/foam_slime"
# process_video_folder(folder_path)

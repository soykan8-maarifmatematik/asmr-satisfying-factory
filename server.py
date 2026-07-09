import os
import json
import subprocess
import sys

def process_video_folder(folder_path):
    # 1. Metadata dosyasını güvenli oku
    metadata_file = os.path.join(folder_path, "metadata.json")
    if not os.path.exists(metadata_file):
        print(f"HATA: {metadata_file} bulunamadı!")
        return

    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    video_path = os.path.join(folder_path, metadata['filename'])
    output_path = os.path.join(folder_path, "final_output.mp4")
    
    # 2. İşleme (Döngü veya Short)
    if metadata.get('type') == "loop":
        print("Loop video tespit edildi, 1 saate tamamlanıyor...")
        # FFmpeg işlemini çalıştır ve sonucu kontrol et
        ffmpeg_cmd = f"ffmpeg -y -stream_loop 400 -i '{video_path}' -t 3600 -c copy '{output_path}'"
        if subprocess.run(ffmpeg_cmd, shell=True).returncode != 0:
            print("FFmpeg hatası oluştu!")
            return
    else:
        print("Short video tespit edildi, kopyalanıyor...")
        subprocess.run(f"cp '{video_path}' '{output_path}'", shell=True)

    # 3. YouTube'a Yükleme (Argümanları güvenli gönder)
    print("YouTube'a yükleme başlıyor...")
    upload_cmd = [
        "python", "upload_to_youtube.py",
        "--file", output_path,
        "--title", metadata['title'],
        "--desc", metadata['description']
    ]
    
    result = subprocess.run(upload_cmd)
    if result.returncode == 0:
        print("Başarıyla yüklendi!")
    else:
        print("Yükleme sırasında hata oluştu.")

# Tetikleyici: Eğer script doğrudan çalıştırılırsa (örneğin GitHub Actions'tan)
if __name__ == "__main__":
    # Örnek: İlk argüman klasör yolunu alır
    if len(sys.argv) > 1:
        target_folder = sys.argv[1]
        process_video_folder(target_folder)

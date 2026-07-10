import os
import json

# GitHub Actions üzerinden gelen ortam değişkenlerini al
title = os.environ.get("PAYLOAD_TITLE")
category = os.environ.get("PAYLOAD_CAT")
v_type = os.environ.get("PAYLOAD_TYPE")  # Make'ten gelen 'loop' veya 'short'

path = f"content/shorts/{category}/"

print(f"İşlem türü algılandı: {v_type}")

# Bumerang Loop Mantığı
if v_type == "loop":
    print("Loop modu aktif: Bumerang ve 1 saatlik loop oluşturuluyor...")
    # 1. Videoyu tersine çevir
    os.system(f"ffmpeg -i {path}current_video.mp4 -vf reverse {path}rev.mp4 -y")
    # 2. Orijinal + Tersini birleştir
    os.system(f"ffmpeg -i {path}current_video.mp4 -i {path}rev.mp4 -filter_complex '[0:v][1:v]concat=n=2:v=1[out]' -map '[out]' {path}full_loop.mp4 -y")
    # 3. 1 saate (3600s) tamamla
    os.system(f"ffmpeg -stream_loop -1 -i {path}full_loop.mp4 -t 3600 -c copy {path}final_video.mp4 -y")
else:
    print("Short modu: Normal işlem devam ediyor.")
    os.system(f"cp {path}current_video.mp4 {path}final_video.mp4")

print("İşlem başarıyla tamamlandı.")

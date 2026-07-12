import os
import sys

title = os.environ.get("PAYLOAD_TITLE")
category = os.environ.get("PAYLOAD_CAT")
v_type = os.environ.get("PAYLOAD_TYPE")

if not category:
    sys.exit(1)

path = f"content/shorts/{category}/"

# 1. İşleme Mantığı
if v_type == "loop":
    os.system(f"ffmpeg -i {path}current_video.mp4 -vf reverse {path}rev.mp4 -y")
    os.system(f"ffmpeg -i {path}current_video.mp4 -i {path}rev.mp4 -filter_complex '[0:v][1:v]concat=n=2:v=1[out]' -map '[out]' {path}full_loop.mp4 -y")
    os.system(f"ffmpeg -stream_loop -1 -i {path}full_loop.mp4 -t 3600 -c copy {path}final_video.mp4 -y")
else:
    os.system(f"cp {path}current_video.mp4 {path}final_video.mp4")

# 2. Yükleme Tetikleyici
print(f"Yükleme başlatılıyor: {path}final_video.mp4")
# Dosya yolunu ve başlığı tırnak içine alarak gönderiyoruz
cmd = f'python upload_to_youtube.py --file "{path}final_video.mp4" --title "{title}"'
upload_status = os.system(cmd)

if upload_status == 0:
    print("Sistem başarıyla tamamlandı.")
else:
    print("Yükleme başarısız oldu.")
    sys.exit(1)

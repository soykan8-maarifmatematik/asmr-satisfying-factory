import os
import sys

# GitHub Actions üzerinden gelen ortam değişkenlerini al
title = os.environ.get("PAYLOAD_TITLE")
category = os.environ.get("PAYLOAD_CAT")
v_type = os.environ.get("PAYLOAD_TYPE")  # 'loop' veya 'short'

# Güvenlik kontrolü: Eğer gerekli bilgiler gelmediyse süreci durdur
if not category:
    print("HATA: Kategori bilgisi alınamadı!")
    sys.exit(1)

path = f"content/shorts/{category}/"

print(f"--- BAŞLANGIÇ ---")
print(f"Kategori: {category}")
print(f"İşlem türü algılandı: {v_type}")

# Dosya yollarını kontrol et
if not os.path.exists(f"{path}current_video.mp4"):
    print(f"HATA: {path}current_video.mp4 dosyası bulunamadı!")
    sys.exit(1)

# Bumerang Loop Mantığı
if v_type == "loop":
    print("Loop modu aktif: Bumerang ve 1 saatlik loop oluşturuluyor...")
    # 1. Videoyu tersine çevir
    os.system(f"ffmpeg -i {path}current_video.mp4 -vf reverse {path}rev.mp4 -y")
    # 2. Orijinal + Tersini birleştir
    os.system(f"ffmpeg -i {path}current_video.mp4 -i {path}rev.mp4 -filter_complex '[0:v][1:v]concat=n=2:v=1[out]' -map '[out]' {path}full_loop.mp4 -y")
    # 3. 1 saate (3600s) tamamla
    os.system(f"ffmpeg -stream_loop -1 -i {path}full_loop.mp4 -t 3600 -c copy {path}final_video.mp4 -y")
elif v_type == "short":
    print("Short modu: Normal işlem devam ediyor.")
    os.system(f"cp {path}current_video.mp4 {path}final_video.mp4")
else:
    print(f"Bilinmeyen tip: {v_type}. Varsayılan işlem uygulanıyor.")
    os.system(f"cp {path}current_video.mp4 {path}final_video.mp4")

# Metadata yazma kısmı
with open(f"{path}title.txt", "w") as f: f.write(str(title))

# Yükleme işlemini tetikle
print("YouTube yükleme scripti tetikleniyor...")
# upload_to_youtube.py dosyanıza dosya yolunu parametre olarak gönderiyoruz
upload_status = os.system(f"python upload_to_youtube.py --file {path}final_video.mp4")

if upload_status == 0:
    print("Yükleme işlemi başarıyla başlatıldı.")
else:
    print("HATA: Yükleme scripti çalıştırılamadı!")
    sys.exit(1)

print("İşlem başarıyla tamamlandı.")
print(f"--- BİTİŞ ---")

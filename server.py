import json
import os
import subprocess

def process_videos():
    # queue.json dosyasını oku
    with open('queue.json', 'r') as f:
        queue = json.load(f)

    for item in queue:
        if item['status'] == 'pending':
            input_file = f"content/{item['category']}/{item['filename']}"
            output_file = f"processed/{item['filename']}"
            
            # İşlem klasörünün varlığından emin ol
            os.makedirs('processed', exist_ok=True)
            
            # Loop (Ambiyans) videoları için (Eski ayarlar korundu)
            if item['type'] == 'loop':
                cmd = [
                    'ffmpeg', '-i', input_file,
                    '-vf', 'split[v1][v2];[v2]reverse[v2r];[v1][v2r]concat=n=2:v=1:a=0,loop=loop=-1:size=2,trim=duration=3600',
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-t', '3600', '-y', output_file
                ]
            else:
                # Shorts için DİKEY ZORLAMA: 'crop' yöntemi
                # Videoyu önce dikey orana göre büyütür, sonra tam 1080x1920 olarak kırpar.
                # Siyah bant bırakmaz, ekranı tamamen dikey doldurur.
                cmd = [
                    'ffmpeg', '-i', input_file,
                    '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
                    '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-y', output_file
                ]
            
            try:
                subprocess.run(cmd, check=True)
                item['status'] = 'completed'
            except subprocess.CalledProcessError as e:
                print(f"Hata oluştu: {e}")
                item['status'] = 'failed'

    # Güncellenmiş durumu kaydet
    with open('queue.json', 'w') as f:
        json.dump(queue, f, indent=2)

if __name__ == "__main__":
    process_videos()

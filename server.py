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
            
            # Klasörün var olduğundan emin ol
            os.makedirs('processed', exist_ok=True)
            
            # Loop (Ambiyans) videoları için
            if item['type'] == 'loop':
                # Bumerang efekti ile 1 saatlik (3600s) döngü
                cmd = [
                    'ffmpeg', '-i', input_file,
                    '-vf', 'split[v1][v2];[v2]reverse[v2r];[v1][v2r]concat=n=2:v=1:a=0,loop=loop=-1:size=2,trim=duration=3600',
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-t', '3600', '-y', output_file
                ]
            else:
                # Shorts videoları için: Dikey oranı korumayı garantiye alan komut
                # 'scale' ile dikey boyutu zorluyoruz
                cmd = [
                    'ffmpeg', '-i', input_file,
                    '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2',
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-y', output_file
                ]
            
            subprocess.run(cmd)
            item['status'] = 'completed'

    # Güncellenmiş queue.json dosyasını kaydet
    with open('queue.json', 'w') as f:
        json.dump(queue, f, indent=2)

if __name__ == "__main__":
    process_videos()

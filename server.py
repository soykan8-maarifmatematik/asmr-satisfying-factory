import json
import os
import subprocess

def process_videos():
    with open('queue.json', 'r') as f:
        queue = json.load(f)

    for item in queue:
        if item['status'] == 'pending':
            # Dosya yollarını belirle
            input_file = f"content/{item['category']}/{item['filename']}"
            output_file = f"processed/{item['filename']}"
            
            # Boomerang mantığı: Videoyu kopyala, tersini ekle ve birleştir
            if item['loop_style'] == 'boomerang':
                cmd = [
                    'ffmpeg', '-i', input_file,
                    '-vf', 'split[v1][v2];[v2]reverse[v2r];[v1][v2r]concat=n=2:v=1:a=0',
                    '-y', output_file
                ]
            else:
                # Shorts ise sadece optimize et (veya olduğu gibi bırak)
                cmd = ['ffmpeg', '-i', input_file, '-c', 'copy', '-y', output_file]
            
            subprocess.run(cmd)
            item['status'] = 'completed'

    with open('queue.json', 'w') as f:
        json.dump(queue, f, indent=2)

if __name__ == "__main__":
    process_videos()

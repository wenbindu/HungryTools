import os

import ffmpy


def ts2mp4(output_path, name):
    print("Starting to merge...")
    os.chdir(output_path)

    fs = []
    for fn in os.listdir(output_path):
        if fn.endswith('.ts'):
            fs.append(fn)
    
    fs = sorted(fs)
    os.system(f"cat {' '.join(fs)} > tmp.ts")
    os.system(f"ffmpeg -i tmp.ts -acodec copy -vcodec copy {name}.mp4")

    print(f"End the merger: {name}")
    os.system(f"rm *.ts")


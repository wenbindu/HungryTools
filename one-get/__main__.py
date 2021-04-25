import os
import sys

from tqdm import tqdm

_srcdir = os.path.dirname(os.path.realpath(__file__))
# print(_srcdir)
sys.path.append(_srcdir)

from extractors.pangzi import PangziExtractor
from process.merge_ts import ts2mp4

# url = input('请输入下载地址：')
# proxy = input('请输入socks代理：') # 127.0.0.1:1080
# output_path = input('请输入下载路径：')
url = "https://www.pangzitv.com/vod-play-id-81610-src-1-num-4.html"
proxy = "127.0.0.1:1080"
output_path = "/home/dean/Downloads/batch_dl"

if not os.path.exists(output_path):
    os.mkdir(output_path)

ex = PangziExtractor(
    init_url=url,
    proxy={'socks': proxy},
    # proxy={'http': '45.167.89.70:999'},
    out_path=output_path)

m3u8_files = ex.get_m3u8()
if not m3u8_files:
    print('网络或者代理异常！')
    

m3u8_files = [(k,v) for k, v in m3u8_files.items()]
for i, v in enumerate(m3u8_files):
    print(f'[{i+1}]{v[0]}: {v[1]}\n')

parts = input("请输入要下载的集数，如果多个用-分隔，例如(1-10, 1-2): ")

if '-' in parts:
    min, max = parts.split('-')
else:
    min, max = parts, parts

for s in range(int(min), int(max)+1):
    label, url = m3u8_files[s-1]
    label = label.replace('/', '-')
    ts_urls = ex.get_playlist(url, label)
    for i in tqdm(range(len(ts_urls)), desc=f"{label} download process: "):
        ex.download_ts(ts_urls[i], label)
    
    print(f"download {label} success")

    # parse to mp4
    _out = os.path.join(output_path, label)
    ts2mp4(_out, label)

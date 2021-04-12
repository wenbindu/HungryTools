import base64
import html
import os
import re
import urllib

import bs4
import execjs
import m3u8
import requests
import urllib3
from util.hex_tool import parser_hex
from util.http_util import retry

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PangziExtractor:
    __name__ = 'panzi'

    def __init__(self, init_url, proxy, out_path):
        """init the class instance

        Args:
            init_url (str): url to get into site.
            proxy (dict): {'http': "", 'https': '', 'socks': ''}
        """
        self.init_url = init_url
        self.proxy = proxy
        self.out_path = out_path

    @property
    def req(self):
        """add header and proxy

        Returns:
            request-session: request session instance
        """
        s = requests.Session()
        s.headers.update({'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'})

        if 'http' in self.proxy:
            proxies = {
                'http': f'http://{self.proxy.get("http")}',
                'https': f'http://{self.proxy.get("http")}',
            }
            if 'https' in self.proxy:
                proxies['https'] = f'http://{self.proxy.get("https")}'
        
        elif 'socks' in self.proxy:
            s_proxy = self.proxy.get('socks')
            proxies=dict(http=f'socks5://{s_proxy}', https=f'socks5://{s_proxy}')
        else:
            assert 'error'
        
        s.proxies.update(proxies)
        return s 

    def get_m3u8(self):
        resp_js = None

        resp = self.req.get(self.init_url, timeout=10)
        if resp.status_code != 200:
            return
        bs = bs4.BeautifulSoup(resp.text, "html.parser")
        scripts = bs.find_all('script')
        for s in scripts:
            if s.contents and 'unescape' in s.contents[0]:
                result = re.match(r".*?base64decode\(\'(.*?)\'\)\);", s.contents[0]).group(1)
                decode_str = base64.b64decode(result)
                resp_js = urllib.parse.unquote(decode_str.decode('unicode-escape'))

        m3u8s = resp_js.split('#')

        _m3u8_dic = {}
        for url in m3u8s:
            k, v = self.parse_m3u8(url)
            _m3u8_dic[k] = v
        
        return _m3u8_dic

    def parse_m3u8(self, item):
        """parse the raw item which contains the m3u8 and label.

        Args:
            item ([str]): [str contains the label and m3u8]
        """
        if not item:
            return
        
        _label, _m3u8 = item.split('$')
        _label = parser_hex(_label)
        return _label, _m3u8

    def get_playlist(self, mu_url, label):
        _fn = mu_url.split('/')[-1]
        _path = os.path.join(self.out_path, label)
        if not os.path.exists(_path):
            os.mkdir(_path)

        _fp = os.path.join(_path, _fn)
        pre_url = '/'.join(mu_url.split('/')[:-1])

        resp = self.req.get(mu_url, verify=False)
        if resp.status_code != 200:
            return
        
        with open(_fp, 'w+') as f:
            f.write(resp.text)

        playlist = m3u8.load(_fp)
        segs = playlist.segments
        download_urls = [os.path.join(pre_url, seg.uri) for seg in segs]
        return download_urls

    @retry(max=3)
    def download_ts(self, url, label):
        _fn = url.split('/')[-1]
        _path = os.path.join(self.out_path, label)

        _fp = os.path.join(_path, _fn)
        if os.path.exists(_fp):
            return

        resp = self.req.get(url, stream=True, verify=False)
        with open(_fp, 'wb') as f:
            f.write(resp.content)

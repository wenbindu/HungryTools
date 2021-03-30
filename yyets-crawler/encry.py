import base64
import hashlib

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


class AESCipher(object):

    def __init__(self, key):
        self.key = key.encode('utf-8')

    def encrypt(self, raw):
        cipher = AES.new(self.key, AES.MODE_CBC)
        return cipher.encrypt(pad(data, AES.block_size))

    # def decrypt(self, enc):
    #     enc = base64.b64decode(enc)
    #     iv = enc[:AES.block_size]
    #     cipher = AES.new(self.key, AES.MODE_CBC, iv)
    #     return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


if __name__ == "__main__":
    c = AESCipher("40595")
    print(c.encrypt("/api/resource?id=35787"))

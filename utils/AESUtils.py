import base64
from Crypto.Cipher import AES


class AEScrypt:
    def __init__(self):
        self.iv = b"qwertyuiopzxcvbn"
        self.key = b"asdfjkqwoeadedfa"
        self.mode = AES.MODE_CBC

    @staticmethod
    def add_to_16(s):
        while len(s) % 16 != 0:
            s += (16 - len(s) % 16) * chr(16 - len(s) % 16)
        return str.encode(s)

    def aes_encrypt(self, text):
        aes = AES.new(key=self.key, mode=self.mode, iv=self.iv)
        encrypt_aes = aes.encrypt(self.add_to_16(text))
        encrypt_txt = str(base64.encodebytes(encrypt_aes), encoding="utf-8").strip()
        return encrypt_txt

    def aes_decrypt(self, aes_key):
        aes = AES.new(key=self.key, mode=self.mode, iv=self.iv)
        decrypt_text = aes.decrypt(base64.decodebytes(bytes(aes_key, encoding='utf-8'))).decode("utf-8",
                                                                                                "ignore").strip()
        return decrypt_text


aescrypt = AEScrypt()

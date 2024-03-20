import os

import qrcode
import base64
from pyotp import TOTP
from transliterate import translit


class Secret:

    DIR = os.getcwd() + os.sep + "secrets"

    def __init__(self, name: str):
        self.name = name
        self.secret = self.generate_secret()

    def verify(self, code: str) -> bool:
        try:
            answer = self.secret.verify(code)
        except Exception as e:
            print(e)
            return False
        else:
            return answer

    def generate_secret(self):

        b32_secret = base64.b32encode(
            bytearray(translit(self.name, "ru", reversed=True), "ascii")
        ).decode("utf-8")

        uri = TOTP(b32_secret).provisioning_uri(name=self.name, issuer_name="ЛимонадКвест")

        if not os.path.exists(Secret.DIR):
            os.makedirs(Secret.DIR)

        qrcode.make(uri).save(f"{Secret.DIR}{os.sep}{self.name}.png")

        return TOTP(b32_secret)

    
    @classmethod
    def from_text(cls, name: str):
        return Secret(name)



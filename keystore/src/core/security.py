import datetime
import hashlib
import hmac
import random
import secrets
import time

from .config import settings


class KeyGen:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def generate(
        self,
        prefix: str | None = None,
        length: int = None,
        expire_days: int | None = None,
    ) -> str:
        timestamp = int(time.time())
        now = datetime.datetime.now()

        numeric_representation = int(
            f"{now.year}{now.month:02d}{now.day:02d}{now.hour:02d}"
            f"{now.minute:02d}{now.second:02d}"
        )

        timestamp_hash = (
            hmac.new(secrets.token_bytes(32), str(timestamp).encode(), hashlib.sha256)
            .hexdigest()
            .upper()
        )
        numeric_hash = hmac.new(
            secrets.token_bytes(32),
            str(numeric_representation).encode(),
            hashlib.sha256,
        ).hexdigest()

        api_key = "".join(random.sample(f"{timestamp_hash}{numeric_hash}", 64))

        if expire_days:
            api_key = "{}_{}".format(api_key, int(time.time()) + (expire_days * 60))

        return api_key

    def is_valid(key: str) -> bool:
        if "_" in key:
            timestamp = int(key.split("_")[1])
            return int(time.time()) < timestamp
        return True

    def verify(self, key: str, hashed_key: str) -> bool:
        return self.hash(key) == hashed_key

    def hash(self, api_key: str) -> str:
        key_hash = hashlib.sha256(
            hmac.new(self.secret_key.encode(), api_key.encode(), hashlib.sha256)
            .hexdigest()
            .encode()
        ).hexdigest()

        return key_hash


keygen = KeyGen(settings.SECRET_KEY)

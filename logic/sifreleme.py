import hashlib

def hash_sifre(sifre: str) -> str:
    return hashlib.sha256(sifre.encode('utf-8')).hexdigest()
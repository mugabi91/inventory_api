from passlib.context import CryptContext

pwd_crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pwd(password: str):
    return pwd_crypt.hash(password)

def verify_pwd(password: str, old_pwd_hash: str):
    return pwd_crypt.verify(password, old_pwd_hash)

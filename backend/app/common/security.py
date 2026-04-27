from datetime import UTC, datetime, timedelta
import hashlib
import hmac
import os

from jose import JWTError, jwt

from app.config import settings


HASH_ALGORITHM = "pbkdf2_sha256"
HASH_ITERATIONS = 260000


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        algorithm, iterations, salt, password_hash = hashed_password.split("$", 3)
    except ValueError:
        return False

    if algorithm != HASH_ALGORITHM:
        return False

    candidate_hash = _hash_password(
        plain_password,
        salt=bytes.fromhex(salt),
        iterations=int(iterations),
    )
    return hmac.compare_digest(candidate_hash, password_hash)


def get_password_hash(password: str) -> str:
    salt = os.urandom(16)
    password_hash = _hash_password(password, salt=salt, iterations=HASH_ITERATIONS)
    return f"{HASH_ALGORITHM}${HASH_ITERATIONS}${salt.hex()}${password_hash}"


def _hash_password(password: str, salt: bytes, iterations: int) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    ).hex()


def create_access_token(subject: str) -> str:
    expires_at = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes,
    )
    payload = {"sub": subject, "exp": expires_at}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict[str, str]:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError as exc:
        raise ValueError("Invalid access token") from exc
